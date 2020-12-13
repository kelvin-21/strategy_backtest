from config import OPEN_POSITION, CLOSE_POSITION, BULLISH, BEARISH

import pandas as pd
import numpy as np

pd.options.mode.chained_assignment = None  # default='warn'

class BacktestTradeRecord():
    def __init__(self):
        self.df = None

    def initialize(self):
        self.df = pd.DataFrame()
        self.df['date_time'] = None
        self.df['strategy_name'] = None
        self.df['position'] = None
        self.df['event'] = None
        self.df['rule'] = None
        self.df['price'] = None
        self.df['trade_return'] = None

    def record_event(self, date_time, strategy, event, rule, price):
        new_row = {'date_time': date_time,
            'strategy_name': strategy.name,
            'position': strategy.position,
            'event': event,
            'rule': rule,
            'price': price}
        self.df = self.df.append(new_row, ignore_index=True)

    def calculate_return(self, strategies):
        self.df.loc[self.df['event'] == OPEN_POSITION, 'trade_return'] == np.NaN

        for strategy in strategies:

            strategy_trade_record = self.df[self.df['strategy_name'] == strategy.name]
            strategy_trade_record['original_ix'] = strategy_trade_record.index.copy()
            strategy_trade_record = strategy_trade_record.reset_index()

            for i in strategy_trade_record.index:

                if strategy_trade_record.at[i, 'event'] == CLOSE_POSITION:
                    entry_price = strategy_trade_record.at[i-1, 'price']
                    exit_price = strategy_trade_record.at[i, 'price']
                    trade_return = self.compute_return(entry_price, exit_price, strategy.position)
                    original_ix = strategy_trade_record.at[i, 'original_ix']
                    self.df.at[original_ix, 'trade_return'] = trade_return

    @staticmethod
    def compute_return(entry_price, exit_price, position):
        if position == BULLISH:
            return (exit_price - entry_price) / entry_price
        elif position == BEARISH:
            return -1 * (exit_price - entry_price) / entry_price
        else:
            raise ValueError('[ERROR] Unknown Position')
        