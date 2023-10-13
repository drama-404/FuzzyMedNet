# eda_functions.py

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


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
