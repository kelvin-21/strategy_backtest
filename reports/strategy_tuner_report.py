import pandas as pd
import os
from datetime import datetime
import logging

from interfaces import Report
from .general_report import GeneralReport
from model import Strategy
from utilities import df_contains_dict
from config import STRATEGY, RETURN_GEO, OCC, OCC_PROFIT, OCC_LOSS


class StrategyTunerReport(Report):

    def __init__(self, strategy: Strategy, strategy_creator):
        super(StrategyTunerReport, self).__init__()
        self.file_path = f'data/{strategy.name}_param_tune_result.csv'
        self.write_batch_size = 1 # save to csv per {batch_size} results
        self.initialize(strategy_creator)

    def initialize(self, strategy_creator):
        if os.path.isfile(self.file_path):
            self.df = pd.read_csv(self.file_path)
            logging.debug(f'[StrategyTunerReport] File found: {self.file_path}')
        else:
            self.df = pd.DataFrame()

            general_report = GeneralReport()
            general_report.initialize()
            for col in general_report.df.columns:
                self.df[col] = None
            
            for key in list(strategy_creator.__dict__.keys()):
                self.df[key] = None

            self.df['simulation_timestamp'] = None

            logging.debug(f'[StrategyTunerReport] File not found: {self.file_path}. Created new file.')


    def write(self, backtest_result: dict, param_config: dict):
        new_row = dict()
        new_row.update(backtest_result)
        new_row.update(param_config)
        new_row['simulation_timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.df = self.df.append(new_row, ignore_index=True)
        self.df = self.df.sort_values(by=RETURN_GEO, ascending=False).reset_index(drop=True)
        if len(self.df) % self.write_batch_size == 0:
            self.df.to_csv(self.file_path, index=False)
            logging.info('[StrategyTunerReport] Batch saved')

    def param_already_exists(self, param_config: dict):
        return df_contains_dict(self.df, param_config)