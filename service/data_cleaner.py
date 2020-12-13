import numpy as np

from config.const import DATE_TIME

class DataCleaner():
    
    def __init__(self):
        self.dropna_method = 'all'
        self.is_fill_missing = True
    
    def clean(self, raw_data):
        raw_data = raw_data.dropna(how=self.dropna_method)
        if self.is_fill_missing:
            raw_data = self.fill_missing_date_time(raw_data)
        return raw_data
    
    @staticmethod
    def fill_missing_date_time(raw_data):
        count = 0
        cols = list(raw_data.columns)
        cols.remove(DATE_TIME)
        for col in cols:
            for i in raw_data.index:
                element = raw_data.at[i, col]
                if np.isnan(element) or element == 0:
                    raw_data.at[i, col] = raw_data.at[i-1, col]
                    count += 1

                    # missing_data_date = raw_data.at[i, DATE_TIME]
                    # ref_data_date = raw_data.at[i-1, DATE_TIME]
                    # print('[CLEAN] Copy data ({}, {}) to ({}, {}))'
                    #       .format(ref_data_date, col, missing_data_date, col))
        print('[CLEAN] {} data items are filled'.format(count))
    
        return raw_data