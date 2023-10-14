import numpy as np
import pandas as pd
import pickle
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from config import *


# Define a function to save a DataFrame to a pickle file
def save_to_pickle(df, filename):
    with open(filename, 'wb') as f:
        pickle.dump(df, f)


# Define a function to load a DataFrame from a pickle file
def load_from_pickle(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)


# Flags to control whether to load intermediate results from disk
LOAD_TIME_IMPUTED = False
LOAD_FILLED = False
LOAD_MULTIPLE_IMPUTED = False


def time_series_imputer(df):
    # Forward fill to propagate the last valid observation forward
    idx = pd.IndexSlice
    df.loc[:, idx[:, 'mean']] = df.loc[:, idx[:, 'mean']].groupby(ID_COLS).fillna(
        method='ffill'
    )

    # Use linear interpolation for any remaining missing values
    df.loc[:, idx[:, 'mean']] = df.loc[:, idx[:, 'mean']].groupby(ID_COLS).apply(lambda group: group.interpolate())

    return df


def multiple_imputer(df):
    imputer = IterativeImputer(max_iter=10, random_state=0)
    df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns, index=df.index)

    return df_imputed


def hybrid_imputer(df, global_means, icustay_means):
    # Initialize filenames
    time_imputed_filename = 'time_imputed.pkl'
    filled_filename = 'filled.pkl'
    multiple_imputed_filename = 'multiple_imputed.pkl'

    idx = pd.IndexSlice         # helper object for slicing on multi-index levels
    df = df.copy()              # ensure that changes within the function do not affect the original data
    df = df.loc[:, idx[:, ['mean', 'count']]]

    print(f"Initial shape: {df.shape}")
    if LOAD_TIME_IMPUTED and os.path.exists(time_imputed_filename):
        df = load_from_pickle(time_imputed_filename)
    else:
        df = time_series_imputer(df)
        save_to_pickle(df, time_imputed_filename)
    print(f"Shape after time-series imputation: {df.shape}")

    if LOAD_FILLED and os.path.exists(filled_filename):
        df = load_from_pickle(filled_filename)
    else:
        df.loc[:, idx[:, 'mean']] = df.loc[:, idx[:, 'mean']].groupby(ID_COLS).fillna(icustay_means).fillna(global_means)
        save_to_pickle(df, filled_filename)
    print(f"Shape after filling with mean: {df.shape}")

    # if LOAD_MULTIPLE_IMPUTED and os.path.exists(multiple_imputed_filename):
    #     df_multiple_imputed = load_from_pickle(multiple_imputed_filename)
    # else:
    #     df_multiple_imputed = multiple_imputer(df_filled)
    #     save_to_pickle(df_multiple_imputed, multiple_imputed_filename)
    # print(f"Shape after multiple imputation: {df_multiple_imputed.shape}")

    # Create a mask to indicate the presence of data
    df.loc[:, idx[:, 'count']] = (df.loc[:, idx[:, 'count']] > 0).astype(float)
    df.rename(columns={'count': 'mask'}, level='Aggregation Function', inplace=True)

    # Compute time since last measurement
    is_absent = (1 - df.loc[:, idx[:, 'mask']])
    hours_of_absence = is_absent.cumsum()
    time_since_measured = hours_of_absence - hours_of_absence[is_absent == 0].fillna(method='ffill')
    time_since_measured.rename(columns={'mask': 'time_since_measured'}, level='Aggregation Function', inplace=True)

    # Concatenate and final adjustments
    df = pd.concat((df, time_since_measured), axis=1)
    df.loc[:, idx[:, 'time_since_measured']] = df.loc[:, idx[:, 'time_since_measured']].fillna(100)

    df.sort_index(axis=1, inplace=True)

    return df



