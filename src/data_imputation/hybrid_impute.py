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
    df_ffill = df.groupby(ID_COLS).fillna(method='ffill')

    # Use linear interpolation for any remaining missing values
    df_interpolated = df_ffill.groupby(ID_COLS).apply(lambda group: group.interpolate())

    return df_interpolated


def multiple_imputer(df):
    imputer = IterativeImputer(max_iter=10, random_state=0)
    df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns, index=df.index)

    return df_imputed


def hybrid_imputer(df, train_subj):
    # Initialize filenames
    time_imputed_filename = 'time_imputed.pkl'
    filled_filename = 'filled.pkl'
    multiple_imputed_filename = 'multiple_imputed.pkl'

    print(f"Initial shape: {df.shape}")
    if LOAD_TIME_IMPUTED and os.path.exists(time_imputed_filename):
        df_time_imputed = load_from_pickle(time_imputed_filename)
    else:
        df_time_imputed = time_series_imputer(df)
        save_to_pickle(df_time_imputed, time_imputed_filename)
    print(f"Shape after time-series imputation: {df_time_imputed.shape}")

    if LOAD_FILLED and os.path.exists(filled_filename):
        df_filled = load_from_pickle(filled_filename)
    else:
        train_mean = df_time_imputed.loc[train_subj].mean()
        df_filled = df_time_imputed.fillna(train_mean)
        save_to_pickle(df_filled, filled_filename)
    print(f"Shape after filling with mean: {df_filled.shape}")

    if LOAD_MULTIPLE_IMPUTED and os.path.exists(multiple_imputed_filename):
        df_multiple_imputed = load_from_pickle(multiple_imputed_filename)
    else:
        df_multiple_imputed = multiple_imputer(df_filled)
        save_to_pickle(df_multiple_imputed, multiple_imputed_filename)
    print(f"Shape after multiple imputation: {df_multiple_imputed.shape}")

    return df_multiple_imputed


