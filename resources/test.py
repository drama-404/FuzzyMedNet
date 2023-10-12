import pandas as pd

if __name__ == '__main__':
    file = pd.read_csv('variable_ranges.csv')
    file = file[file['LEVEL1'].isnull()]
    file = file[file['VALID LOW'].notnull()]
    file['LEVEL2'] = file['LEVEL2'].str.lower()
    file.drop(columns=['LEVEL1'], inplace=True)
    file.rename(columns={'LEVEL2': 'MEASUREMENT'}, inplace=True)
    file.reset_index(drop=True, inplace=True)
    file.to_csv('vitals_labs_ranges.csv')
