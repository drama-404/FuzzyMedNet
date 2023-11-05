"""
split_dataset.py

- Function that performs the data splitting operation.
It takes three dataframes (`patients`, `vitals_labs`, and `interventions`)
and returns a dictionary containing the train, dev, and test splits for each dataframe.

Steps:
**Filter Targets**: Only consider patients with sufficient data for the target variables `mort_hosp` and `mort_icu`.
**Extract Static Features**: Remove the target variables and other non-static features from the `patients` dataframe.
**Filter Time-Series Data**: Trim the time-series data to only include instances within a specified observation window.
**Subject ID Validation**: Check that the subject IDs are consistent across all dataframes.
**Random Split**: Randomly shuffle the subject IDs and allocate them into train, dev, and test sets based on predefined fractions.
**Dataframe Splits**: Create train, dev, and test dataframes for each of the input dataframes (`patients`, `vitals_labs`, `interventions`), based on the shuffled subject IDs.
**Return Data**: A dictionary containing the train, dev, and test splits for each dataframe is returned.
"""

import numpy as np
from config import *
from sklearn.model_selection import train_test_split

GAP_TIME = 0  # Time gap in hours
WINDOW_SIZE = 48  # Observation window in hours
ID_COLS = ['subject_id', 'hadm_id', 'icustay_id']  # Identifying columns
TRAIN_FRAC, DEV_FRAC, TEST_FRAC = 0.7, 0.1, 0.2  # Data split fractions
SEED = 1  # Seed for reproducibility
RANDOM = 0


def train_test_dev_split(patients, vitals_labs, interventions , Ys):
    # Filter out patients with insufficient data and extract target labels
    # Ys = patients[patients['max_hours'] > WINDOW_SIZE + GAP_TIME][['mort_hosp', 'mort_icu']]
    # Ys = patients[['mort_hosp']]
    # Ys.astype(float)  # Convert to float type

    # Extract static features
    statics = patients.drop(columns=['mort_hosp', 'max_hours'])

    # Filter time-series data to only include instances within the observation window
    # lvl2, interv = [
    #     df[
    #         (df.index.get_level_values('icustay_id').isin(set(Ys.index.get_level_values('icustay_id')))) &
    #         (df.index.get_level_values('hours_in') < WINDOW_SIZE)
    #     ] for df in (vitals_labs, interventions)
    # ]
    lvl2 = vitals_labs
    interv = interventions

    # Validate that the subject IDs match across all dataframes
    lvl2_subj_idx, interv_subj_idx, Ys_subj_idx = [
        df.index.get_level_values('subject_id') for df in (lvl2, interv, Ys)
    ]
    lvl2_subjects = set(lvl2_subj_idx)
    assert lvl2_subjects == set(Ys_subj_idx), "Subject ID pools differ!"
    assert lvl2_subjects == set(interv_subj_idx), "Subject ID pools differ!"

    # # Randomly shuffle the subject IDs and split them into train, dev, and test sets
    # np.random.seed(SEED)
    # subjects, N = np.random.permutation(list(lvl2_subjects)), len(lvl2_subjects)
    # N_train, N_dev, N_test = int(TRAIN_FRAC * N), int(DEV_FRAC * N), int(TEST_FRAC * N)
    # train_subj, dev_subj, test_subj = subjects[:N_train], subjects[N_train:N_train + N_dev], subjects[N_train + N_dev:]

    full_set = patients.loc[Ys_subj_idx]
    train_set, test_set = train_test_split(full_set.reset_index(), test_size=0.2,
                                           random_state=RANDOM, stratify=full_set['mort_hosp'])
    split_train_set, dev_set = train_test_split(train_set, test_size=0.125,
                                                random_state=RANDOM, stratify=train_set['mort_hosp'])
    train_subj = split_train_set['subject_id']
    dev_subj = dev_set['subject_id']
    test_subj = test_set['subject_id']

    # Create train, dev, and test sets for each dataframe based on the shuffled subject IDs
    datasets = {
        key: [df[df.index.get_level_values('subject_id').isin(s)] for s in (train_subj, dev_subj, test_subj)]
        for key, df in zip(['patients', 'vitals', 'interv', 'Ys'], [statics, lvl2, interv, Ys])
    }

    return datasets
