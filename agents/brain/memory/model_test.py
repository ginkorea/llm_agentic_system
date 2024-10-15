def test_memory_system(memory_class):
    """Generic test function to test memory systems (either CUDA or OpenVINO)."""
    # Initialize the memory system with the provided class
    memory = memory_class(forget_threshold=10)
    print(f"{memory_class.__name__} Memory System initialized successfully.")

    # Test memory storage
    print("Storing memory entries...")
    memory.store_memory("What is the capital of France?", "The capital of France is Paris.")
    memory.store_memory("What is quantum physics?", "Quantum physics studies matter at atomic scales.")
    memory.store_memory("How does gravity work?", "Gravity is a force that attracts objects towards one another.")
    memory.store_memory("Explain thermodynamics laws.", "The laws of thermodynamics deal with energy and heat.")
    print("Memory entries stored.")

    # Test memory search
    print("Performing searches...")

    query_1 = "capital city of France"
    query_2 = "gravity"
    query_3 = "thermodynamics laws"

    result_1 = memory.search_memory(query_1)
    result_2 = memory.search_memory(query_2)
    result_3 = memory.search_memory(query_3)

    # Display search results
    print(f"Search results for '{query_1}': {result_1}")
    print(f"Search results for '{query_2}': {result_2}")
    print(f"Search results for '{query_3}': {result_3}")

    # Check if search returns correct results (you can adjust these assertions based on your memory content)
    assert result_1, f"Search for '{query_1}' failed!"
    assert result_2, f"Search for '{query_2}' failed!"
    assert result_3, f"Search for '{query_3}' failed!"

    print(f"All tests passed successfully for {memory_class.__name__}!\n")


if __name__ == "__main__":
    from agents.brain.memory.cuda_embedded import CudaMemoryWithEmbeddings
    from agents.brain.memory.ov_embedded import OpenvinoMemoryWithEmbeddings

    # Test both CUDA and OpenVINO memory systems
    print("Testing CUDA Memory System")
    test_memory_system(CudaMemoryWithEmbeddings)

    print("Testing OpenVINO Memory System")
    test_memory_system(OpenvinoMemoryWithEmbeddings)
