import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from preprocessing import process_diagnoses


def replace_vital_labels(df):
    labels = {
        1: 'heart_rate',
        2: 'systolic_blood_pressure',
        3: 'diastolic_blood_pressure',
        4: 'mean_blood_pressure',
        5: 'respiratory_rate',
        6: 'temperature',
        7: 'oxygen_saturation',
        8: 'glucose',
        9: 'weight'
    }

    df['vital_sign'] = df['vitalid'].apply(lambda x: labels[int(x)])

    return df


def define_limits():
    vital_signs_limits = {
        'heart_rate': [0, 300],
        'systolic_blood_pressure': [0, 400],
        'diastolic_blood_pressure': [0, 300],
        'mean_blood_pressure': [0, 300],
        'respiratory_rate': [0, 70],
        'temperature': [10, 50],
        'oxygen_saturation': [0, 100],
        'glucose': [0, 4000],
        'weight': [0, 300]
    }

    return vital_signs_limits


def visualize_signs(df, diagnosis):
    df_filtered = df[df[diagnosis] == 1]  # change to fit the structure of your DataFrame
    vital_signs = df['vital_sign'].unique()

    fig, ax = plt.subplots(4, 3, figsize=(15, 20))
    ax = ax.flatten()

    fig.suptitle('Diagnosis: {}'.format(diagnosis), fontsize=20, fontweight='bold')

    for i, vital_sign in enumerate(vital_signs):
        df_filtered_vital = df_filtered[df_filtered['vital_sign'] == vital_sign]
        sns.boxplot(x=diagnosis, y='valuenum', hue='hospital_expire_flag', data=df_filtered_vital, ax=ax[i])
        ax[i].set_title('Values of {}'.format(vital_sign, diagnosis))

    for i in range(len(vital_signs), len(ax)):
        fig.delaxes(ax[i])

    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    plt.show()


def visualize_over_time(df, vital_sign, limits=None):
    df = df[df['vital_sign'] == vital_sign]
    grouped_df = df.groupby(['hospital_expire_flag', 'hours_since_admission'])['valuenum'].mean().reset_index()

    plt.figure(figsize=(12, 8))

    for label, group in grouped_df.groupby('hospital_expire_flag'):
        plt.plot(group['hours_since_admission'], group['valuenum'], label=f'Expired: {label}')

    plt.xlabel('Hours Since Admission')
    plt.ylabel(f'Average {vital_sign}')
    plt.title(f"Average {vital_sign} over Time by Patient Outcome")
    plt.legend(title='Patient Status')
    if limits:
        plt.xlim(limits)

    plt.show()

