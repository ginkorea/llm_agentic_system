import json
import logging
import os
from io import BytesIO
from typing import Any, Dict, List, Optional, Tuple, Union

import torch
from torch import nn
from transformers import AutoConfig, AutoModel, AutoTokenizer

logger = logging.getLogger(__name__)


class Transformer(nn.Module):
    """Huggingface AutoModel to generate token embeddings.
    Loads the correct class, e.g. BERT / RoBERTa etc.

    Args:
        model_name_or_path: Huggingface models name
            (https://huggingface.co/models)
        max_seq_length: Truncate any inputs longer than max_seq_length
        model_args: Keyword arguments passed to the Huggingface
            Transformers model
        tokenizer_args: Keyword arguments passed to the Huggingface
            Transformers tokenizer
        config_args: Keyword arguments passed to the Huggingface
            Transformers config
        cache_dir: Cache dir for Huggingface Transformers to store/load
            models
        do_lower_case: If true, lowercases the input (independent if the
            model is cased or not)
        tokenizer_name_or_path: Name or path of the tokenizer. When
            None, then model_name_or_path is used
    """

    def __init__(
        self,
        model_name_or_path: str,
        max_seq_length: int = None,
        model_args: Dict[str, Any] = None,
        tokenizer_args: Dict[str, Any] = None,
        config_args: Dict[str, Any] = None,
        cache_dir: str = None,
        do_lower_case: bool = False,
        tokenizer_name_or_path: str = None,
        **kwargs,
    ) -> None:
        super().__init__()
        self.config_keys = ["max_seq_length", "do_lower_case"]
        self.do_lower_case = do_lower_case
        if model_args is None:
            model_args = {}
        if tokenizer_args is None:
            tokenizer_args = {}
        if config_args is None:
            config_args = {}

        if kwargs.get("backend", "torch") != "torch":
            logger.warning(
                f'"jinaai/jina-embeddings-v3" is currently not compatible with the {kwargs["backend"]} backend. '
                'Continuing with the "torch" backend.'
            )
        
        self.config = AutoConfig.from_pretrained(model_name_or_path, **config_args, cache_dir=cache_dir)

        self._lora_adaptations = self.config.lora_adaptations
        if (
            not isinstance(self._lora_adaptations, list)
            or len(self._lora_adaptations) < 1
        ):
            raise ValueError(
                f"`lora_adaptations` must be a list and contain at least one element"
            )
        self._adaptation_map = {
            name: idx for idx, name in enumerate(self._lora_adaptations)
        }

        self.default_task = model_args.pop('default_task', None)

        self.auto_model = AutoModel.from_pretrained(model_name_or_path, config=self.config, cache_dir=cache_dir, **model_args)

        if max_seq_length is not None and "model_max_length" not in tokenizer_args:
            tokenizer_args["model_max_length"] = max_seq_length
        self.tokenizer = AutoTokenizer.from_pretrained(
            tokenizer_name_or_path if tokenizer_name_or_path is not None else model_name_or_path,
            cache_dir=cache_dir,
            **tokenizer_args,
        )

        # No max_seq_length set. Try to infer from model
        if max_seq_length is None:
            if (
                hasattr(self.auto_model, "config")
                and hasattr(self.auto_model.config, "max_position_embeddings")
                and hasattr(self.tokenizer, "model_max_length")
            ):
                max_seq_length = min(self.auto_model.config.max_position_embeddings, self.tokenizer.model_max_length)

        self.max_seq_length = max_seq_length

        if tokenizer_name_or_path is not None:
            self.auto_model.config.tokenizer_class = self.tokenizer.__class__.__name__


    @property
    def default_task(self):
        return self._default_task

    @default_task.setter
    def default_task(self, task: Union[None, str]):
        self._validate_task(task)
        self._default_task = task
        

    def _validate_task(self, task: str):
        if task and task not in self._lora_adaptations:
            raise ValueError(
                f"Unsupported task '{task}'. "
                f"Supported tasks are: {', '.join(self.config.lora_adaptations)}. "
                f"Alternatively, don't pass the `task` argument to disable LoRA."
            )

    def forward(
        self, features: Dict[str, torch.Tensor], task: Optional[str] = None
    ) -> Dict[str, torch.Tensor]:
        """Returns token_embeddings, cls_token"""
        self._validate_task(task)
        task = task or self.default_task
        adapter_mask = None
        if task:
            task_id = self._adaptation_map[task]
            num_examples = features['input_ids'].size(0)
            adapter_mask = torch.full(
                (num_examples,), task_id, dtype=torch.int32, device=features['input_ids'].device
            )

        lora_arguments = (
            {"adapter_mask": adapter_mask} if adapter_mask is not None else {}
        )
        output_states = self.auto_model.forward(**features, **lora_arguments, return_dict=False)
        output_tokens = output_states[0]
        features.update({"token_embeddings": output_tokens, "attention_mask": features["attention_mask"]})
        return features

    def get_word_embedding_dimension(self) -> int:
        return self.auto_model.config.hidden_size

    def tokenize(
        self,
        texts: Union[List[str], List[dict], List[Tuple[str, str]]],
        padding: Union[str, bool] = True
    ) -> Dict[str, torch.Tensor]:
        """Tokenizes a text and maps tokens to token-ids"""
        output = {}
        if isinstance(texts[0], str):
            to_tokenize = [texts]
        elif isinstance(texts[0], dict):
            to_tokenize = []
            output["text_keys"] = []
            for lookup in texts:
                text_key, text = next(iter(lookup.items()))
                to_tokenize.append(text)
                output["text_keys"].append(text_key)
            to_tokenize = [to_tokenize]
        else:
            batch1, batch2 = [], []
            for text_tuple in texts:
                batch1.append(text_tuple[0])
                batch2.append(text_tuple[1])
            to_tokenize = [batch1, batch2]

        # strip
        to_tokenize = [[str(s).strip() for s in col] for col in to_tokenize]

        # Lowercase
        if self.do_lower_case:
            to_tokenize = [[s.lower() for s in col] for col in to_tokenize]

        output.update(
            self.tokenizer(
                *to_tokenize,
                padding=padding,
                truncation="longest_first",
                return_tensors="pt",
                max_length=self.max_seq_length,
            )
        )
        return output

    def get_config_dict(self) -> dict[str, Any]:
         return {key: self.__dict__[key] for key in self.config_keys}

    def save(self, output_path: str, safe_serialization: bool = True) -> None:
        self.auto_model.save_pretrained(output_path, safe_serialization=safe_serialization)
        self.tokenizer.save_pretrained(output_path)

        with open(os.path.join(output_path, "sentence_bert_config.json"), "w") as fOut:
            json.dump(self.get_config_dict(), fOut, indent=2)


    @classmethod
    def load(cls, input_path: str) -> "Transformer":
        # Old classes used other config names than 'sentence_bert_config.json'
        for config_name in [
            "sentence_bert_config.json",
            "sentence_roberta_config.json",
            "sentence_distilbert_config.json",
            "sentence_camembert_config.json",
            "sentence_albert_config.json",
            "sentence_xlm-roberta_config.json",
            "sentence_xlnet_config.json",
        ]:
            sbert_config_path = os.path.join(input_path, config_name)
            if os.path.exists(sbert_config_path):
                break

        with open(sbert_config_path) as fIn:
            config = json.load(fIn)
        # Don't allow configs to set trust_remote_code
        if "model_args" in config and "trust_remote_code" in config["model_args"]:
            config["model_args"].pop("trust_remote_code")
        if "tokenizer_args" in config and "trust_remote_code" in config["tokenizer_args"]:
            config["tokenizer_args"].pop("trust_remote_code")
        if "config_args" in config and "trust_remote_code" in config["config_args"]:
            config["config_args"].pop("trust_remote_code")
        return cls(model_name_or_path=input_path, **config)
