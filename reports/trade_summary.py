import pandas as pd
import numpy as np

from interfaces import Report
from utilities import str_time_diff_in_days
from service import CalenderService
from config import ENTRY_T, EXIT_T, DURATION, STRATEGY, RULE, ENTRY_PRICE, EXIT_PRICE, RETURN, OPEN_POSITION, CLOSE_POSITION, DATE_TIME, EVENT, PRICE


class TradeSummary(Report):
    def __init__(self):
        super(TradeSummary, self).__init__()
        self.calendar_service = CalenderService()

    def initialize(self):
        self.df = pd.DataFrame()
        self.df[ENTRY_T] = None
        self.df[EXIT_T] = None
        self.df[DURATION] = None
        self.df[STRATEGY] = None
        self.df[RULE] = None
        self.df[ENTRY_PRICE] = None
        self.df[EXIT_PRICE] = None
        self.df[RETURN] = None

    def generate(self, strategies: list, trade_record: pd.DataFrame):

        for strategy in strategies:

            df = trade_record[trade_record[STRATEGY] == strategy.name]
            df['original_ix'] = df.index.copy()
            df = df.reset_index(drop=True)

            for i in df.index:

                if df.at[i, EVENT] == OPEN_POSITION:
                    
                    close_pos = df[i:][df[EVENT] == CLOSE_POSITION].reset_index(drop=True)

                    if len(close_pos) > 0:
                        new_row = {
                            ENTRY_T:        df.at[i, DATE_TIME],
                            EXIT_T:         close_pos.at[0, DATE_TIME],
                            DURATION:       self.calendar_service.time_diff_market_days(df.at[i, DATE_TIME], close_pos.at[0, DATE_TIME]),
                            STRATEGY:       strategy.name,
                            RULE:           close_pos.at[0, RULE],
                            ENTRY_PRICE:    df.at[i, PRICE],
                            EXIT_PRICE:     close_pos.at[0, PRICE],
                            RETURN:         close_pos.at[0, RETURN]
                        }
                        self.df = self.df.append(new_row, ignore_index=True)

        self.df = self.df.sort_values(by=ENTRY_T)
        self.df = self.df.reset_index(drop=True)
                    