import pandas as pd
import numpy as np
from pathlib import Path

# TODO: remove constatns where data available on github
data_dir = Path('../bag_data_download/downloads').resolve()
cases_dir = data_dir / 'cases_data'
report_dir = data_dir / 'report_data'
test_dir = data_dir / 'test_data'


def get_latest(directory, prefix = '', suffix='', n = 1):
    time, latest = sorted((f.stat().st_mtime, f) for f in directory.glob(prefix + '*' + suffix))[-n]
    return latest


def load_data(nn = 1):
    # create DataFrame from Excel
    xlsx = get_latest(cases_dir, prefix='2020', suffix='.xlsx', n = nn)
    print(xlsx)
    df = pd.read_excel(xlsx)
    
    renames = {
        'replikation_dt': 'date',
        'fall_dt' : 'case_date',
        'ktn': 'canton',
        'akl': 'age_class',
        'fallklasse_3': 'new_conf',
        'pttod_1': 'new_deceased',
        'pttoddat': 'date_deceased'
    }
    
    # rename columns
    df.rename(columns = renames,inplace=True)
    
    # split datetime column into a date and a time column
    time_list = pd.to_datetime(df['date'], dayfirst=True).dt.time
    df.insert(loc=1, column='time', value=time_list)                 
    df['date'] = pd.to_datetime(df['date'], dayfirst=True).dt.date
    df['date'] = pd.to_datetime(df['date'], dayfirst=True)
    df['case_date'] = pd.to_datetime(df['case_date'], dayfirst=True).dt.date
    df['case_date'] = pd.to_datetime(df['case_date'], dayfirst=True)
    df['date_deceased'] = pd.to_datetime(df['date_deceased'], dayfirst=True).dt.date
    df['date_deceased'] = pd.to_datetime(df['date_deceased'], dayfirst=True)

    # clean up
    df.loc[:,'sex'] = np.where(df['sex'] == 1, 'm', np.where(df['sex'] == 2, 'f', 'n/a'))
    df.drop('Geschlecht', axis=1, inplace=True)
    df.drop('Sexe', axis=1, inplace=True)

    # insert column for country
    df.insert(loc=3, column='country', value=np.where(df['canton'] == 'FL', 'FL', 'CH'))

    return df