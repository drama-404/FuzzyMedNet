"""
simple_impute.py

- Function that handles missing data.
    - Missing values are forward-filled (propagated last valid observation forward).
    - If any missing values remain, they are filled with the mean for that `icustay_id` group.
    - Any remaining missing values are filled with 0.
    - A mask indicating where data is present is created.
    - The time since the last measurement is calculated for each column.
"""

import copy, math, os, pickle, time, pandas as pd, numpy as np

ID_COLS = ['subject_id', 'hadm_id', 'icustay_id']


def simple_imputer(df, global_means, icustay_means):
    """Impute missing values in the data"""
    idx = pd.IndexSlice         # helper object for slicing on multi-index levels
    df = df.copy()              # ensure that changes within the function do not affect the original data

    # Select mean and count columns
    df_out = df.loc[:, idx[:, ['mean', 'count']]]

    # This is a multistep imputation:
    # First, fill NaN values with the preceding value in the group using `forward fill`.
    # Next, fill any remaining NaNs with the mean value of the corresponding 'icustay_id' group.
    # Finally, if there are still any NaN values, replace with 0.
    df_out.loc[:, idx[:, 'mean']] = df_out.loc[:, idx[:, 'mean']].groupby(ID_COLS).fillna(
        method='ffill'
    ).groupby(ID_COLS).fillna(icustay_means).fillna(global_means)

    # Create a mask to indicate the presence of data
    df_out.loc[:, idx[:, 'count']] = (df.loc[:, idx[:, 'count']] > 0).astype(float)
    df_out.rename(columns={'count': 'mask'}, level='Aggregation Function', inplace=True)

    # Compute time since last measurement
    is_absent = (1 - df_out.loc[:, idx[:, 'mask']])
    hours_of_absence = is_absent.cumsum()
    time_since_measured = hours_of_absence - hours_of_absence[is_absent == 0].fillna(method='ffill')
    time_since_measured.rename(columns={'mask': 'time_since_measured'}, level='Aggregation Function', inplace=True)

    # Concatenate and final adjustments
    df_out = pd.concat((df_out, time_since_measured), axis=1)
    df_out.loc[:, idx[:, 'time_since_measured']] = df_out.loc[:, idx[:, 'time_since_measured']].fillna(100)

    df_out.sort_index(axis=1, inplace=True)
    return df_out


def calculate_impute_values(train_df):
    idx = pd.IndexSlice
    # Compute mean for each icustay
    icustay_means = train_df.loc[:, idx[:, 'mean']].groupby(ID_COLS).mean()
    global_means = train_df.loc[:, idx[:, 'mean']].mean(axis=0)

    return global_means, icustay_means
