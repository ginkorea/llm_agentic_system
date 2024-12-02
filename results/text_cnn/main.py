from workbench.textcnn_project import TextCNNModel, DataProcessor, TrainingLogger, ModelEvaluator

def main():
    # Initialize components
    data_processor = DataProcessor()
    train_dataset, test_dataset = data_processor.preprocess_data(data_processor.load_dataset())
    
    model = TextCNNModel(embedding_dim=300, kernel_sizes=[3, 4, 5], max_length=50)
    logger = TrainingLogger()
    evaluator = ModelEvaluator()

    # Train the model
    model.train_model(train_dataset, learning_rate=0.01, batch_size=16, num_epochs=10)

    # Evaluate the model
    accuracy = model.evaluate()
    logger.log_accuracy(epoch=10, accuracy=accuracy)

    # Save a checkpoint
    model.save_checkpoint(epoch=10)

if __name__ == "__main__":
    main()