import pandas as pd
import numpy as np

from config import CLOSE_POSITION

class BacktestReport():
    def __init__(self):
        self.general_report = None
        self.return_report = None
        self.occurrence_report = None

    def initialize(self, strategies):
        self.initialize_general_report()
        self.initialize_return_report()
        self.initialize_occurrence_report()

    def generate_report(self, strategies: list, trade_record: pd.DataFrame):
        self.generate_general_report(strategies, trade_record)
        self.generate_return_report(strategies, trade_record)
        self.generate_occurrence_report(strategies, trade_record)

    def generate_general_report(self, strategies: list, trade_record: pd.DataFrame):
        for strategy in strategies:
            df = trade_record[trade_record['strategy_name'] == strategy.name]
                        
            new_row = {
                'strategy_name': strategy.name,
                'occurrence': df[df['event'] == CLOSE_POSITION].shape[0],
                'occ_profit': df[df['trade_return'] > 0].shape[0],
                'occ_loss': df[df['trade_return'] < 0].shape[0],
                'return_average': df['trade_return'].mean(),
                'return_average_geo': np.prod(df['trade_return'] + 1) - 1,
                'return_std': df['trade_return'].std()}
            self.general_report = self.general_report.append(new_row, ignore_index=True)
            
        self.add_summary_row(trade_record)

    def add_summary_row(self, trade_record: pd.DataFrame):
        new_row = {
            'strategy_name': 'summary',
            'occurrence': self.general_report['occurrence'].sum(),
            'occ_profit': self.general_report['occ_profit'].sum(),
            'occ_loss': self.general_report['occ_loss'].sum(),
            'return_average': trade_record['trade_return'].mean(),
            'return_average_geo': np.prod(trade_record['trade_return'] + 1) - 1,
            'return_std': trade_record['trade_return'].std()}
        self.general_report = self.general_report.append(new_row, ignore_index=True)

    def generate_return_report(self, strategies, trade_record):
        pass

    def generate_occurrence_report(self, strategies, trade_record):
        pass

    def initialize_general_report(self):
        self.general_report = pd.DataFrame()
        self.general_report['strategy_name'] = None
        self.general_report['occurrence'] = None
        self.general_report['occ_profit'] = None
        self.general_report['occ_loss'] = None
        self.general_report['return_average'] = None
        self.general_report['return_std'] = None

    def initialize_return_report(self):
        self.return_report = pd.DataFrame()
        pass

    def initialize_occurrence_report(self):
        pass