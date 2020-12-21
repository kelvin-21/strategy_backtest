import pandas as pd
import numpy as np

from config import OPEN_POSITION, CLOSE_POSITION, BULLISH, BEARISH, DATE_TIME, STRATEGY, POSITION, EVENT, RULE, PRICE, RETURN

pd.options.mode.chained_assignment = None  # default='warn'


class BacktestTradeRecord():
    def __init__(self):
        self.df = None

    def initialize(self):
        self.df = pd.DataFrame()
        self.df[DATE_TIME] = None
        self.df[STRATEGY] = None
        self.df[POSITION] = None
        self.df[EVENT] = None
        self.df[RULE] = None
        self.df[PRICE] = None
        self.df[RETURN] = None

    def record_event(self, date_time, strategy, event, rule, price):
        new_row = {
            DATE_TIME:  date_time,
            STRATEGY:   strategy.name,
            POSITION:   strategy.position,
            EVENT:      event,
            RULE:       rule,
            PRICE:      price
        }
        self.df = self.df.append(new_row, ignore_index=True)

    def calculate_return(self, strategies):
        self.df.loc[self.df[EVENT] == OPEN_POSITION, RETURN] == np.NaN

        for strategy in strategies:

            strategy_trade_record = self.df[self.df[STRATEGY] == strategy.name]
            strategy_trade_record['original_ix'] = strategy_trade_record.index.copy()
            strategy_trade_record = strategy_trade_record.reset_index(drop=True)

            for i in strategy_trade_record.index:

                if strategy_trade_record.at[i, EVENT] == CLOSE_POSITION:
                    entry_price = strategy_trade_record.at[i-1, PRICE]
                    exit_price = strategy_trade_record.at[i, PRICE]
                    trade_return = self.compute_return(entry_price, exit_price, strategy.position)
                    original_ix = strategy_trade_record.at[i, 'original_ix']
                    self.df.at[original_ix, RETURN] = trade_return

    @staticmethod
    def compute_return(entry_price, exit_price, position):
        if position == BULLISH:
            return (exit_price - entry_price) / entry_price
        elif position == BEARISH:
            return -1 * (exit_price - entry_price) / entry_price
        else:
            raise ValueError('[ERROR] Unknown Position')
        