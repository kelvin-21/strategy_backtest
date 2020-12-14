import pandas as pd
import numpy as np

from interfaces import Report
from config import STRATEGY, OCC, OCC_PROFIT, OCC_LOSS, RETURN, RETURN_STD, RETURN_AVG, RETURN_GEO, CLOSE_POSITION, EVENT, SUMMARY


class ReturnReport(Report):

    def initialize(self):
        self.df = pd.DataFrame()
        # will define the columns in run time

    def generate(self, strategies: list, trade_summary: pd.DataFrame):
        # define columns
        self.df[SUMMARY] = None
        for strategy in strategies:
            self.df[strategy.name] = None
        for strategy in strategies:
            for rule in strategy.close_position.rules:
                col = '{}-{}'.format(strategy.name, rule.name)
                self.df[col] = None