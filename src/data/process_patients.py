def categorize_ethnicity(ethnicity):
    white_group = ['WHITE', 'WHITE - RUSSIAN', 'WHITE - OTHER EUROPEAN', 'WHITE - EASTERN EUROPEAN',
                   'WHITE - BRAZILIAN', 'PORTUGUESE']
    black_group = ['BLACK/AFRICAN AMERICAN', 'BLACK/AFRICAN', 'BLACK/CAPE VERDEAN', 'BLACK/HAITIAN']
    asian_group = ['ASIAN', 'ASIAN - VIETNAMESE', 'ASIAN - CHINESE', 'ASIAN - ASIAN INDIAN', 'ASIAN - FILIPINO',
                   'ASIAN - CAMBODIAN', 'ASIAN - KOREAN', 'ASIAN - JAPANESE', 'ASIAN - THAI', 'ASIAN - OTHER',
                   'MIDDLE EASTERN']
    hispanic_group = ['HISPANIC OR LATINO', 'HISPANIC/LATINO - GUATEMALAN', 'HISPANIC/LATINO - PUERTO RICAN',
                      'HISPANIC/LATINO - SALVADORAN', 'HISPANIC/LATINO - DOMINICAN',
                      'HISPANIC/LATINO - CENTRAL AMERICAN (OTHER)', 'HISPANIC/LATINO - COLOMBIAN',
                      'HISPANIC/LATINO - HONDURAN', 'HISPANIC/LATINO - CUBAN', 'HISPANIC/LATINO - MEXICAN']
    native_group = ['AMERICAN INDIAN/ALASKA NATIVE', 'AMERICAN INDIAN/ALASKA NATIVE FEDERALLY RECOGNIZED TRIBE']
    islander_group = ['NATIVE HAWAIIAN OR OTHER PACIFIC ISLANDER', 'CARIBBEAN ISLAND', 'SOUTH AMERICAN']
    unknown_group = ['UNKNOWN/NOT SPECIFIED', 'PATIENT DECLINED TO ANSWER', 'UNABLE TO OBTAIN', 'OTHER']

    if ethnicity in white_group:
        return 'WHITE'
    elif ethnicity in black_group:
        return 'BLACK'
    elif ethnicity in asian_group:
        return 'ASIAN'
    elif ethnicity in hispanic_group:
        return 'HISPANIC'
    elif ethnicity in native_group:
        return 'NATIVE AMERICAN'
    elif ethnicity in islander_group:
        return 'ISLANDER'
    else:
        return 'OTHER/UNKNOWN'


def group_admission_location(location):
    # Grouping all types of TRANSFER categories into one
    if 'TRANSFER' in location or 'TRSF' in location:
        return 'TRANSFER'
    else:
        return location


def group_admission_type(adm_type):
    # Grouping the URGENT & EMERGENCY type into a single category
    return 'EMERGENCY' if adm_type == 'URGENT' else adm_type


def calc_age(df):
    df['age_at_admission'] = df['admittime'].dt.year - df['dob'].dt.year
    df['age_at_admission'] = df['age_at_admission'].apply(lambda x: 89 if x > 89 else x)

    return df


def categorize_age(age):
    if 10 < age <= 30:
        cat = '<31'
    elif 30 < age <= 50:
        cat = '31-50'
    elif 50 < age <= 70:
        cat = '51-70'
    else:
        cat = '>70'
    return cat

