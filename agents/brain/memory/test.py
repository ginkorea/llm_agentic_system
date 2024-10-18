import numpy as np

def memory_tests(test_memory):
    print("\n--- Running Basic Store Memory Test ---")
    # Store some memory
    test_memory.store_memory("How to bake a cake?", "Mix flour, sugar, eggs, and bake.")
    test_memory.store_memory("How to fix a car?", "Check the engine and tires.")
    test_memory.store_memory("How to ride a bike?", "Start pedaling while balancing.")

    # Verify that memory was stored
    print(f"Number of entries in long-term memory: {len(test_memory.long_term_df)}")
    assert len(test_memory.long_term_df) == 3, "Memory storage failed."

    print("\n--- Running Embedding Generation Test ---")
    # Check if embeddings were generated and stored as numpy arrays
    assert isinstance(test_memory.long_term_df.iloc[0]["embedding"], np.ndarray), "Embedding should be a numpy array."
    print(f"Shape of embedding for first entry: {test_memory.long_term_df.iloc[0]['embedding'].shape}")

    # Ensure that embeddings have the correct size
    expected_embedding_size = test_memory.embedding_size  # 8192
    print(f"Expected embedding size: {expected_embedding_size}")
    assert test_memory.long_term_df.iloc[0]["embedding"].shape[0] == expected_embedding_size, \
        f"Embedding size should be {expected_embedding_size}, got {test_memory.long_term_df.iloc[0]['embedding'].shape[0]}."

    print("\n--- Running Embedding Search Test ---")
    # Perform an embedding search
    search_results = test_memory.search_memory("bike", top_n=1)

    # Check if search results returned data
    print(f"Search results:\n{search_results}")
    assert not search_results.empty, "Search results should not be empty."

    print("\nAll tests passed successfully.")