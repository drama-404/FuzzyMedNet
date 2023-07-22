def group_ethnicities(df):
    # Grouping white categories
    white_group = ['WHITE', 'WHITE - RUSSIAN', 'WHITE - OTHER EUROPEAN', 'WHITE - EASTERN EUROPEAN',
                   'WHITE - BRAZILIAN', 'PORTUGUESE']
    df['ethnicity'].replace(white_group, 'WHITE', inplace=True)

    # Grouping black categories
    black_group = ['BLACK/AFRICAN AMERICAN', 'BLACK/AFRICAN', 'BLACK/CAPE VERDEAN', 'BLACK/HAITIAN']
    df['ethnicity'].replace(black_group, 'BLACK', inplace=True)

    # Grouping Asian categories
    asian_group = ['ASIAN', 'ASIAN - VIETNAMESE', 'ASIAN - CHINESE', 'ASIAN - ASIAN INDIAN', 'ASIAN - FILIPINO',
                   'ASIAN - CAMBODIAN', 'ASIAN - KOREAN', 'ASIAN - JAPANESE', 'ASIAN - THAI', 'ASIAN - OTHER',
                   'MIDDLE EASTERN']
    df['ethnicity'].replace(asian_group, 'ASIAN', inplace=True)

    # Grouping Hispanic/Latino categories
    hispanic_group = ['HISPANIC OR LATINO', 'HISPANIC/LATINO - GUATEMALAN', 'HISPANIC/LATINO - PUERTO RICAN',
                      'HISPANIC/LATINO - SALVADORAN', 'HISPANIC/LATINO - DOMINICAN',
                      'HISPANIC/LATINO - CENTRAL AMERICAN (OTHER)', 'HISPANIC/LATINO - COLOMBIAN',
                      'HISPANIC/LATINO - HONDURAN', 'HISPANIC/LATINO - CUBAN', 'HISPANIC/LATINO - MEXICAN']
    df['ethnicity'].replace(hispanic_group, 'HISPANIC/LATINO', inplace=True)

    # Grouping Native categories
    native_group = ['AMERICAN INDIAN/ALASKA NATIVE', 'AMERICAN INDIAN/ALASKA NATIVE FEDERALLY RECOGNIZED TRIBE']
    df['ethnicity'].replace(native_group, 'NATIVE AMERICAN', inplace=True)

    # Grouping Islander categories
    islander_group = ['NATIVE HAWAIIAN OR OTHER PACIFIC ISLANDER', 'CARIBBEAN ISLAND', 'SOUTH AMERICAN']
    df['ethnicity'].replace(islander_group, 'ISLANDER', inplace=True)

    # Grouping others and unknown categories
    unknown_group = ['UNKNOWN/NOT SPECIFIED', 'PATIENT DECLINED TO ANSWER', 'UNABLE TO OBTAIN', 'OTHER']
    df['ethnicity'].replace(unknown_group, 'OTHER/UNKNOWN', inplace=True)

    return df


def group_admission_location(df):
    # Grouping all types of TRANSFER categories into one
    df['admission_location'] = df['admission_location'].apply(lambda x: 'TRANSFER' if ('TRANSFER' in x) or ('TRSF' in x) else x)

    return df


def group_admission_type(df):
    # Grouping the URGENT & EMERGENCY type into a single category
    df['admission_type'].replace(['URGENT'], 'EMERGENCY', inplace=True)

    return df


def clean_df(df):
    # Drop irrelevant columns
    columns_to_drop = ['row_id', 'dischtime', 'deathtime', 'insurance', 'language', 'religion',
                       'marital_status', 'edregtime', 'edouttime', 'discharge_location', 'has_chartevents_data']
    return df.drop(columns=columns_to_drop)


def calc_age(df):
    df['age_at_admission'] = df['admittime'].dt.year - df['dob'].dt.year
    df['age_at_admission'] = df['age_at_admission'].apply(lambda x: 89 if x > 89 else x)

    return df