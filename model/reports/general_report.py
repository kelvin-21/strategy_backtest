import pandas as pd
import numpy as np

from interfaces import Report
from config import STRATEGY, OCC, OCC_PROFIT, OCC_LOSS, RETURN, RETURN_STD, RETURN_AVG, RETURN_GEO, CLOSE_POSITION, EVENT, SUMMARY


class GeneralReport(Report):

    def initialize(self):
        self.df = pd.DataFrame()
        self.df[STRATEGY] = None
        self.df[OCC] = None
        self.df[OCC_PROFIT] = None
        self.df[OCC_LOSS] = None
        self.df[RETURN_AVG] = None
        self.df[RETURN_STD] = None
        self.df[RETURN_GEO] = None

    def generate(self, strategies: list, trade_summary: pd.DataFrame):
        
        for strategy in strategies:
            df = trade_summary[trade_summary[STRATEGY] == strategy.name]
                        
            new_row = {
                STRATEGY:       strategy.name,
                OCC:            df.shape[0],
                OCC_PROFIT:     df[df[RETURN] > 0].shape[0],
                OCC_LOSS:       df[df[RETURN] < 0].shape[0],
                RETURN_AVG:     df[RETURN].mean(),
                RETURN_STD:     df[RETURN].std(),
                RETURN_GEO:     np.prod(df[RETURN] + 1) - 1
            }
            self.df = self.df.append(new_row, ignore_index=True)
            
            new_row = {
                STRATEGY:       SUMMARY,
                OCC:            self.df[OCC].sum(),
                OCC_PROFIT:     self.df[OCC_PROFIT].sum(),
                OCC_LOSS:       self.df[OCC_LOSS].sum(),
                RETURN_AVG:     trade_summary[RETURN].mean(),
                RETURN_STD:     trade_summary[RETURN_STD].std(),
                RETURN_GEO:     np.prod(trade_summary[RETURN] + 1) - 1.
            }
            self.df = self.df.append(new_row, ignore_index=True)
