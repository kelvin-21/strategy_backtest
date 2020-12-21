import pandas as pd
import numpy as np
import logging

from config.const import DATE_TIME

class DataCleaner():
    
    def __init__(self):
        self.dropna_method = 'all'
        self.is_fill_missing = True
        self.is_drop_repeat_col = True
    
    def clean(self, raw_data):
        raw_data = raw_data.dropna(how=self.dropna_method)
        if self.is_fill_missing:
            raw_data = self.fill_missing_date_time(raw_data)
        if self.is_drop_repeat_col:
            raw_data = self.drop_repeat_col(raw_data)
        return raw_data
    
    @staticmethod
    def fill_missing_date_time(raw_data: pd.DataFrame) -> pd.DataFrame:
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
        logging.info('[CLEAN] {} data items are filled'.format(count))
    
        return raw_data

    @staticmethod
    def drop_repeat_col(raw_data: pd.DataFrame) -> pd.DataFrame:
        original_len = len(raw_data)
        raw_data = raw_data.drop_duplicates(subset=DATE_TIME).reset_index(drop=True)
        logging.info('[CLEAN] {} duplicate row(s) are dropped'.format(original_len - len(raw_data)))
        return raw_data