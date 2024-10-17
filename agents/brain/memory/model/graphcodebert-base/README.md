## GraphCodeBERT model

GraphCodeBERT is a graph-based pre-trained model based on the Transformer architecture for programming language, which also considers data-flow information along with code sequences. GraphCodeBERT consists of 12 layers, 768 dimensional hidden states, and 12 attention heads. The maximum sequence length for the model is 512. The model is trained on the CodeSearchNet dataset, which includes 2.3M functions with document pairs for six programming languages. 

More details can be found in the [paper](https://arxiv.org/abs/2009.08366) by Guo et. al.

**Disclaimer:** The team releasing BERT did not write a model card for this model so this model card has been written by the Hugging Face community members.