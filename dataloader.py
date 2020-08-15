import pandas as pd
import requests
from constants import CANTONS, URLs, FOLDERS

def add_diff_col(df, col, new_col):
    df[new_col] = df[col].diff()
    return df

def get_data():
    df_ch = get_CH_data_total()

    # DON'T DO THAT --> Fills SMA7-NaN wiht 0 too
    #df_bag = get_BAG_data()
    #df_ch.merge(right=df_bag, how='left', on='date')
    #df_ch.fillna(value=0, inplace=True)
    return df_ch

def download_openZH_data():
    base_url = 'https://github.com/openZH/covid_19/raw/master/fallzahlen_kanton_total_csv_v2'
    prefix_c_fn = 'COVID19_Fallzahlen_Kanton'
    prefix_fn = 'COVID19_Fallzahlen'
    postfix_fn = 'total.csv'

    for c in CANTONS.values():
        if (c == "FL"):
            url = f'{base_url}/{prefix_fn}_{c}_{postfix_fn}'
        else:
            url = f'{base_url}/{prefix_c_fn}_{c}_{postfix_fn}'

        r = requests.get(url, allow_redirects=True)
        fname = url.split('/')[-1]
        open(FOLDERS['openZH_data'] + fname, 'wb').write(r.content)

def get_CH_data_total():
    
    # FIXME - remove before going productive and update the files separately
    download_openZH_data()
    
    # where to find the data files
    folder_v2 = FOLDERS['openZH_data']
    prefix_c_fn = 'COVID19_Fallzahlen_Kanton'
    prefix_fn = 'COVID19_Fallzahlen'
    postfix_fn = 'total.csv'

    dfs = []

    for c in CANTONS.values():
    
        if (c == "FL"):
            file = f'{folder_v2}{prefix_fn}_{c}_{postfix_fn}'
        else:
            file = f'{folder_v2}{prefix_c_fn}_{c}_{postfix_fn}'
    
        dfc = pd.read_csv(file)
        dfc['date'] = pd.to_datetime(dfc['date'], dayfirst=True)
    
        # mark current rows as reported by cantons
        dfc['reported'] = True
    
        # add rows for missing (unreported) days
        idx = pd.date_range(dfc.date.min(), dfc.date.max())
        dfc = dfc.set_index('date')
        dfc = dfc.reindex(idx)
        dfc.index.name = 'date'
        dfc.reset_index(level=0, inplace=True)

        # flag added rows as 'reported = False'
        dfc.loc[dfc['reported'] != True, 'reported'] = False
    
        # fill unreported numbers (NaN) with number of last reported
        dfc.fillna(method='ffill', inplace=True)
    
        # fill missing values at the beginning with zero
        dfc.fillna(value=0, inplace=True)
    
        # add some columns with calculated values of interest
        add_diff_col(dfc, 'ncumul_tested', 'new_tested')
        add_diff_col(dfc, 'ncumul_conf', 'new_conf')
        add_diff_col(dfc, 'ncumul_deceased', 'new_deceased')
        add_diff_col(dfc, 'current_hosp', 'delta_hosp')
        add_diff_col(dfc, 'current_icu', 'delta_icu')
        add_diff_col(dfc, 'current_vent', 'delta_vent')
        add_diff_col(dfc, 'current_isolated', 'delta_isolated')
        add_diff_col(dfc, 'current_quarantined', 'delta_quarantined')
        add_diff_col(dfc, 'ncumul_released', 'new_released')

        # add 7-day simple mean averages
        dfc['new_conf_SMA7'] = round(dfc['new_conf'].rolling(window=7, center=True).mean(), 1)
        dfc['current_hosp_SMA7'] = round(dfc['current_hosp'].rolling(window=7, center=True).mean(), 1)
    
        # append the dataframe and go on with the next canton
        dfs.append(dfc)

    # sum up all the cantons dataframes
    df_ch = pd.concat(dfs, sort=False)
    df_ch = df_ch.groupby('date').sum(min_count=1)
    df_ch.index.name = 'date'
    df_ch.reset_index(level=0, inplace=True)
    # the SMA7 gets broken for incomplete data (missing cantons) when summing up, so let's recalculate
    df_ch['new_conf_SMA7'] = round(df_ch['new_conf'].rolling(window=7, center=True).mean(), 1)
    df_ch['current_hosp_SMA7'] = round(df_ch['current_hosp'].rolling(window=7, center=True).mean(), 1)

    return df_ch

def get_BAG_data():
    df_bag = pd.read_csv('/Users/eandreas/projects/dev/covid-19/bag_data/bag_data.csv')

    # split datetime column into a date and a time column
    time_list = pd.to_datetime(df_bag['date'], dayfirst=True).dt.time
    df_bag.insert(loc=1, column='time', value=time_list)                 
    df_bag['date'] = pd.to_datetime(df_bag['date'], dayfirst=True).dt.date
    df_bag['date'] = pd.to_datetime(df_bag['date'])

    # remove the rows without information (NaN for total_number_of_tests)
    df_bag[df_bag['total_number_of_tests'].notnull()]
    
    # calculate and add a column wit newly tested cases per day
    add_diff_col(df_bag, 'total_number_of_tests', 'new_tested')

    return df_bag

def download_BAG_test_data():
    r = requests.get(URLs['BAG_test_data'], allow_redirects=True)
    fname = URLs['BAG_test_data'].split('/')[-1]
    open(FOLDERS['BAG_data'] + fname, 'wb').write(r.content)

def get_BAG_test_data():

    # FIXME - remove before going productive and update the files separately
    download_BAG_test_data()

    df_bag_test = pd.read_excel(FOLDERS['BAG_data'] + 'Dashboard_3_COVID19_labtests_positivity.xlsx')
    df_bag_test = df_bag_test.drop('Replikation_dt', axis=1)
    df_bag_test_pos = df_bag_test[df_bag_test['Outcome_tests'] == 'Positive']
    df_bag_test_pos = df_bag_test_pos.drop('Outcome_tests', axis=1)
    df_bag_test_neg = df_bag_test[df_bag_test['Outcome_tests'] == 'Negative']
    df_bag_test_neg = df_bag_test_neg.drop('Outcome_tests', axis=1)
    df_bag_test = df_bag_test_pos.merge(right=df_bag_test_neg, on='Datum')
    df_bag_test = df_bag_test.rename(columns={"Datum": "date", "Number_of_tests_x": "positive", "Number_of_tests_y": "negative"})
    df_bag_test['pos_rate'] = round(100 * df_bag_test['positive'] / (df_bag_test['positive'] + df_bag_test['negative']), 1)
    df_bag_test['pos_rate_SMA7'] = round(df_bag_test['pos_rate'].rolling(window=7, center=True).mean(), 1)
    df_bag_test['new_tests'] = df_bag_test['positive'] + df_bag_test['negative']
    df_bag_test['new_tests_SMA7'] = round(df_bag_test['new_tests'].rolling(window=7, center=True).mean(), 1)
    return df_bag_test

def stretch_data_frames(dfs):
    # initialize min and max date
    min_date = dfs[0].date.min()
    max_date = dfs[0].date.max()
    # loop over all data frames and find the global min and max date
    for df in dfs:
        if (df.date.min() < min_date):
            min_date = df.date.min()
        if (df.date.max() > max_date):
            max_date = df.date.max()
    # add missing rows (dates) in each data frame
    idx = pd.date_range(min_date, max_date)
    for i in range(len(dfs)):
        dfs[i] = dfs[i].set_index('date')
        dfs[i] = dfs[i].reindex(idx)
        dfs[i].index.name = 'date'
        dfs[i].reset_index(level=0, inplace=True)
    # return the tuple of data frames for reassigning (make the added rows persistent)
    return tuple(dfs)