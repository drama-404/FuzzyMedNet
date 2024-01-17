from src.models.grud_model import *
from utils.eda import (load_from_pickle, save_to_pickle, append_results)
from config import (DATA_DIR)

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


if __name__ == "__main__":
    X_train = load_from_pickle(f'{DATA_DIR}vitals_train.pkl')
    X_dev = load_from_pickle(f'{DATA_DIR}vitals_dev.pkl')
    X_test = load_from_pickle(f'{DATA_DIR}vitals_test.pkl')

    Ys_train = load_from_pickle(f'{DATA_DIR}Ys_train.pkl')
    Ys_dev = load_from_pickle(f'{DATA_DIR}Ys_dev.pkl')
    Ys_test = load_from_pickle(f'{DATA_DIR}Ys_test.pkl')

    full_results = []

    model_name = 'GRU-D'
    tasks = ['mort_hosp']
    hyperparams_list = grid()
    RERUN = False

    if model_name not in full_results: full_results[model_name] = {}

    t = 'mort_hosp'
    if t not in full_results[model_name]: full_results[model_name][t] = {}
    n, X_train, X_dev, X_test = ('full_X', X_train, X_dev, X_test)
    print("Running model %s on target %s with representation %s" % (model_name, t, n))
    X_mean = np.nanmean(
        to_3D_tensor(
            X_train.loc[:, pd.IndexSlice[:, 'mean']] *
            np.where((X_train.loc[:, pd.IndexSlice[:, 'mask']] == 1).values, 1, np.NaN)
        ),
        axis=0, keepdims=True
    ).transpose([0, 2, 1])
    base_params = {'X_mean': X_mean, 'output_last': True, 'input_size': X_mean.shape[2]}

    best_s, best_hyperparams = -np.Inf, None
    for i, hyperparams in enumerate(hyperparams_list):
        hyperparams_print = "On sample %d / %d (hyperparams = %s)\n" % (
        i + 1, len(hyperparams_list), repr((hyperparams)))
        print(hyperparams_print)
        append_results("training_results2.txt", hyperparams_print)
        batch_size = hyperparams['batch_size']

        np.random.seed(SEED)
        all_train_subjects = list(
            np.random.permutation(Ys_train.index.get_level_values('subject_id').values)
        )
        N_early_stop = int(len(all_train_subjects) * EARLY_STOP_FRAC)
        train_subjects = all_train_subjects[:-N_early_stop]
        early_stop_subjects = all_train_subjects[-N_early_stop:]
        X_train_obs = X_train[X_train.index.get_level_values('subject_id').isin(train_subjects)]
        Ys_train_obs = Ys_train[Ys_train.index.get_level_values('subject_id').isin(train_subjects)]

        X_train_early_stop = X_train[X_train.index.get_level_values('subject_id').isin(early_stop_subjects)]
        Ys_train_early_stop = Ys_train[
            Ys_train.index.get_level_values('subject_id').isin(early_stop_subjects)
        ]

        train_dataloader = prepare_dataloader(X_train_obs, Ys_train_obs[t], batch_size=batch_size)
        early_stop_dataloader = prepare_dataloader(
            X_train_early_stop, Ys_train_early_stop[t], batch_size=batch_size
        )
        dev_dataloader = prepare_dataloader(X_dev, Ys_dev[t], batch_size=batch_size)
        test_dataloader = prepare_dataloader(X_test, Ys_test[t], batch_size=batch_size)

        model_hyperparams = copy.copy(base_params)
        model_hyperparams.update(
            {k: v for k, v in hyperparams.items() if k in ('hidden_size', 'batch_size')}  # removed cell_size
        )

        model = GRUD(**model_hyperparams)

        best_model, _ = Train_Model(
            model, train_dataloader, early_stop_dataloader,
            **{k: v for k, v in hyperparams.items() if k in (
                'num_epochs', 'patience', 'learning_rate', 'batch_size'
            )}
        )

        probabilities_dev, labels_dev = predict_proba(best_model, dev_dataloader)
        probabilities_dev = np.concatenate(probabilities_dev)[:, 1]
        labels_dev = np.concatenate(labels_dev)
        s = roc_auc_score(labels_dev, probabilities_dev)
        if s > best_s:
            best_s, best_hyperparams = s, hyperparams
            print("New Best Score: %.2f @ hyperparams = %s" % (100 * best_s, repr((best_hyperparams))))
        append_results("training_results.txt", "\n")
