import pandas as pd
from constants import CANTONS

def add_diff_col(df, col, new_col):
    df[new_col] = df[col].diff()
    return df

def get_CH_data_total():
    # where to find the data files
    folder_v2 = '/Users/eandreas/projects/dev/covid-19/openZH_covid-19/fallzahlen_kanton_total_csv_v2'
    prefix_c_fn = 'COVID19_Fallzahlen_Kanton'
    prefix_fn = 'COVID19_Fallzahlen'
    postfix_fn = 'total.csv'

    dfs = []

    for c in CANTONS.values():
    
        #c = 'ZH'
    
        if (c == "FL"):
            file = f'{folder_v2}/{prefix_fn}_{c}_{postfix_fn}'
        else:
            file = f'{folder_v2}/{prefix_c_fn}_{c}_{postfix_fn}'
    
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
    
        # append the dataframe and go on with the next canton
        dfs.append(dfc)
    
        #break

    # sum up all the cantons dataframes
    df_ch = pd.concat(dfs, sort=False)
    df_ch = df_ch.groupby('date').sum()
    df_ch.index.name = 'date'
    df_ch.reset_index(level=0, inplace=True)
    return df_ch