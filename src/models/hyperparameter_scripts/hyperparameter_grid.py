from itertools import product


def grid():
    # Define the parameter grid
    hidden_sizes = [32, 64, 128, 256]
    learning_rates = [0.0001, 0.0005, 0.001]
    batch_sizes = [32, 64, 128, 256, 512]

    # Placeholder for storing the results
    GRU_D_hyperparams_list = []

    # The fixed number of epochs for training
    num_epochs = 100
    patience = 10

    # Iterate over all combinations of hyperparameters
    for batch_size, hidden_size, learning_rate in product(batch_sizes, hidden_sizes, learning_rates):
        GRU_D_hyperparams_list.append({
            'hidden_size': int(hidden_size),
            'learning_rate': learning_rate,
            'batch_size': int(batch_size),
            'patience': int(patience),
            'num_epochs': int(num_epochs)
        })
    return GRU_D_hyperparams_list
