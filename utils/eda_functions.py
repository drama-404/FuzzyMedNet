# eda_functions.py

import numpy as np
import pandas as pd
import seaborn as sns
import pickle
import matplotlib.pyplot as plt

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer


# Define a function to save a DataFrame to a pickle file
def save_to_pickle(df, filename):
    with open(filename, 'wb') as f:
        pickle.dump(df, f)


# Define a function to load a DataFrame from a pickle file
def load_from_pickle(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)


def plot_categorical_columns(df, categorical_columns):
    """
    Plots the distribution of specified categorical columns from a DataFrame.

    Parameters:
    df (DataFrame): the DataFrame containing the data
    categorical_columns (list of str): the names of the categorical columns to plot
    """
    for column in categorical_columns:
        if column in df.columns:
            plt.figure(figsize=(10, 6))
            sns.countplot(data=df, x=column)
            # plt.xticks(rotation=45)  # Rotate the category labels for readability if needed
            plt.title(f'Distribution of {column}')
            plt.show()
        else:
            print(f"Column {column} not found in the DataFrame")


def calculate_duration(df, start_time_col, end_time_col, unit='D'):
    """
    Calculate duration between two time columns in specified time unit.
    Default unit is days ('D'). Other options include 'h' (hours), 'm' (minutes), and 's' (seconds).
    """
    duration = (df[end_time_col] - df[start_time_col])
    days = duration.dt.days
    if unit == 'D':
        return days
    elif unit == 'h':
        return days * 24 + duration.dt.seconds / 3600
    elif unit == 'm':
        return days * 24 * 60 + duration.dt.seconds / 60
    elif unit == 's':
        return days * 24 * 60 * 60 + duration.dt.seconds
    else:
        return duration.dt.days  # default is days


def plot_time_analysis(df, time_cols):
    for col in time_cols:
        if df[col].dtype == 'datetime64[ns]':
            df[col].groupby(df[col].dt.hour).count().plot(kind="bar")
            plt.title(f'Distribution of {col} (Hourly)')
            plt.xlabel('Hour of Day')
            plt.ylabel('Frequency')
            plt.show()


def plot_hourly_distributions(df, features, valid_ranges):
    """
    Plot the hourly distributions of measurements, considering the mean of all patients.

    Parameters:
    - df: DataFrame containing the measurements and hours.
          The DataFrame is assumed to have columns 'hours_in' and feature columns.
    - features: list of measurements to plot.
    - valid_ranges: DataFrame containing 'Measurement', 'Valid Low', and 'Valid High' columns.
    """
    # # Identify the unique measurements (features) in the DataFrame
    # features = [col for col in df.columns if col != 'hours_in']

    for feature in features:
        plt.figure(figsize=(10, 5))

        # Group by 'hours_in' and calculate mean for each hour for the feature
        hourly_mean = df.groupby(['hours_in'])[feature].mean().reset_index()

        sns.lineplot(data=hourly_mean, x='hours_in', y=feature)

        # Fetch valid low and high values for the measurement
        if feature in list(valid_ranges['measurement']):
            valid_low = valid_ranges.loc[valid_ranges['measurement'] == feature, 'valid low'].values[0]
            valid_high = valid_ranges.loc[valid_ranges['measurement'] == feature, 'valid high'].values[0]

            # Add lines for valid low and high values
            plt.axhline(valid_low, color='r', linestyle='--', label=f'Valid Low ({valid_low})')
            plt.axhline(valid_high, color='g', linestyle='--', label=f'Valid High ({valid_high})')

        plt.title(f'Hourly Distribution of {feature}')
        plt.xlabel('Hours in ICU')
        plt.ylabel(f'{feature} (Mean)')
        # plt.legend()

        plt.show()


def plot_hourly_distributions(df, features, valid_ranges):
    """
    Plot the hourly distributions of measurements, considering the mean of all patients.

    Parameters:
    - df: DataFrame containing the measurements and hours.
          The DataFrame is assumed to have columns 'hours_in' and feature columns.
    - features: list of measurements to plot.
    - valid_ranges: DataFrame containing 'Measurement', 'Valid Low', and 'Valid High' columns.
    """
    # # Identify the unique measurements (features) in the DataFrame
    # features = [col for col in df.columns if col != 'hours_in']

    for feature in features:
        plt.figure(figsize=(10, 5))

        # Group by 'hours_in' and calculate mean for each hour for the feature
        hourly_mean = df.groupby(['hours_in'])[feature].mean().reset_index()

        sns.lineplot(data=hourly_mean, x='hours_in', y=feature)

        # Fetch valid low and high values for the measurement
        if feature in list(valid_ranges['measurement']):
            valid_low = valid_ranges.loc[valid_ranges['measurement'] == feature, 'valid low'].values[0]
            valid_high = valid_ranges.loc[valid_ranges['measurement'] == feature, 'valid high'].values[0]

            # Add lines for valid low and high values
            plt.axhline(valid_low, color='r', linestyle='--', label=f'Valid Low ({valid_low})')
            plt.axhline(valid_high, color='g', linestyle='--', label=f'Valid High ({valid_high})')

        plt.title(f'Hourly Distribution of {feature}')
        plt.xlabel('Hours in ICU')
        plt.ylabel(f'{feature} (Mean)')
        # plt.legend()

        plt.show()


def plot_hourly_counts(df, features):
    for feature in features:
        if feature in df.columns:
            plt.figure(figsize=(18, 5))
            df[feature].plot(kind='bar')
            plt.title(f'Total Hourly Measurements of {feature}')
            plt.xlabel('Hours in ICU')
            plt.ylabel(f'{feature} (Sum)')
            plt.show()


def pearson_correlation_among_features(df, fig_size=(20, 15)):
    corr = df.corr()  # Compute the correlation matrix
    mask = np.triu(np.ones_like(corr, dtype=bool))  # Create a mask for the upper triangle
    annot = np.around(corr, 2)  # Format the correlation matrix for 2 decimal places

    fig, ax = plt.subplots(figsize=fig_size)
    sns.heatmap(corr, mask=mask, cmap='coolwarm', vmax=1, vmin=-1, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .75}, annot=annot)
    plt.title(' Correlation Among Features')
    plt.show()


def pearson_highly_correlated_pairs(df, threshold=.7):
    # Extracting pairs without duplicates
    pairs_to_drop = set()
    corr = df.corr()
    cols = corr.columns
    for i in range(0, corr.shape[1]):
        for j in range(0, i + 1):
            pairs_to_drop.add((cols[i], cols[j]))

    # Extract the values and pairs into a DataFrame
    corr_values = []
    for i in range(corr.shape[0]):
        for j in range(corr.shape[1]):
            if np.abs(corr.iloc[i, j]) >= threshold and (cols[i], cols[j]) not in pairs_to_drop:
                corr_values.append([cols[i], cols[j], corr.iloc[i, j]])

    corr_df = pd.DataFrame(corr_values, columns=['var1', 'var2', 'corr_value'])
    return corr_df


def pearson_target_correlation(df, Ys):

    X_y = pd.merge(df, Ys[['mort_hosp']], left_index=True, right_index=True, how='left')
    corr_matrix = X_y.corr()

    fig, ax = plt.subplots(figsize=(5, 8))
    # Isolate the column corresponding to `in-hospital mortality`
    corr_target = corr_matrix[['mort_hosp']].drop(labels=['mort_hosp'])

    sns.heatmap(corr_target, annot=True, fmt='.3', cmap='RdBu_r', vmax=1, vmin=-1)
    plt.title('Pearson Target Correlation')
    plt.show()


def encoding_categorical_vars(df, categorical_cols):

    # Initialize OneHotEncoder
    onehotencoder = OneHotEncoder(drop='first')  # drop='first' to avoid dummy variable trap

    # Apply one-hot encoder to categorical columns
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', onehotencoder, categorical_cols)],
        remainder='passthrough')  # keep other columns untouched

    # Fit and transform the DataFrame
    df_encoded = preprocessor.fit_transform(df)

    # Feature names after one-hot encoding
    feature_names = preprocessor.named_transformers_['cat'].get_feature_names(categorical_cols)

    # Create a DataFrame with the new features
    df_encoded = pd.DataFrame(df_encoded,
                              columns=list(feature_names) + [col for col in df.columns if col not in categorical_cols])

    return df_encoded

