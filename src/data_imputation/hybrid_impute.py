import numpy as np
import pandas as pd
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from config import *

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
    # Step 1: Time-series imputation
    df_time_imputed = time_series_imputer(df)

    # Step 2: Compute mean for training subjects and fill remaining NaNs
    train_mean = df_time_imputed.loc[train_subj].mean()
    df_filled = df_time_imputed.fillna(train_mean)

    # Step 3: Multiple imputation for any remaining missing values
    df_multiple_imputed = multiple_imputer(df_filled)

    return df_multiple_imputed

