import pandas as pd

def yyyymmdd2ns(date_string):
    return pd.to_datetime(date_string, format='%Y%m%d').value
