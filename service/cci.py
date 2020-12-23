import numpy as np

from model.param import CCIParam
from config import HIGH, LOW, CLOSE

class CCI():
    
    def __init__(self, param: CCIParam):
        self.param = param
        
    def compute(self, data):
        
        # typical price
        data['typical'] = data[[HIGH, LOW, CLOSE]].apply(lambda row: self.typical_price(row), axis=1)
        
        # moving average of typical price
        data['MA'] = data['typical'].rolling(window=self.param.period).mean()
        
        # absolute difference between typical price and MA
        data['abs_diff'] = data[['typical', 'MA']].apply(lambda row: abs(row['typical'] - row['MA']), axis=1)
        
        # mean deviation
        data['MD'] = None
        for i in range(len(data)):
            if i - self.param.period + 1 < 0:
                data.at[i, 'MD'] = np.NaN
            else:
                s = 0
                for j in range(self.param.period):
                    s += abs(data.at[i-j, 'typical'] - data.at[i, 'MA'])
                data.at[i, 'MD'] = s / self.param.period
        
        # CCI
        data[self.param.name] = data[['typical', 'MA', 'MD']].apply(lambda row: self.cci_formula(row), axis=1)
        
        # drop columns for intermediate steps
        data = data.drop(columns=['typical', 'MA', 'abs_diff', 'MD'])
        
        return data
        
    @staticmethod
    def typical_price(row):
        return (row[HIGH] + row[LOW] + row[CLOSE]) / 3
    
    def cci_formula(self, row):
        return (row['typical'] - row['MA']) / (self.param.coeff * row['MD'])