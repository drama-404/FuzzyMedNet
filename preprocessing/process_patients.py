import pandas as pd


def add_first_admission(patients, admissions):
    # Find the first admission time for each patient
    first_admission_time = admissions.groupby('subject_id')['admittime'].min().reset_index()

    # Rename the column
    first_admission_time.rename(columns={'admittime': 'first_admittime'}, inplace=True)
    first_admission_time['first_admittime'] = first_admission_time['first_admittime'].dt.floor('D')

    # Merge this back into the patients DataFrame
    patients = pd.merge(patients, first_admission_time, on='subject_id', how='left')

    return patients


def calc_age_at_admission(df):
    # Calculate the age at the time of admission
    df['age_at_admission'] = df['first_admittime'].dt.year - df['dob'].dt.year

    # For those older than 89 at their first admission, set their age to be 89
    df['age_at_admission'] = df['age_at_admission'].apply(lambda age: 89 if age > 89 else age)

    return df


def clean_df(df):
    # Drop irrelevant columns
    columns_to_drop = ['row_id', 'dob', 'dod', 'dod_hosp', 'dod_ssn']
    return df.drop(columns=columns_to_drop)
