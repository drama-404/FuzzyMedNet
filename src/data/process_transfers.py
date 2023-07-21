def clean_icu(df):
    columns_to_drop = ['row_id', 'subject_id', 'dbsource', 'first_wardid', 'last_wardid', 'intime', 'outtime', 'last_careunit']
    df = df.drop(columns=columns_to_drop)
    df = df.rename(columns={'los': 'icu_los'})

    return df

