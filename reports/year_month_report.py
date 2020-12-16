import pandas as pd
import numpy as np
from typing import List

from interfaces import Report
from model import Strategy
from utilities import dtStr_to_dt
from config import STRATEGY, RULE, RETURN, RETURN_GEO, CLOSE_POSITION, EVENT, SUMMARY, TOTAL, MONTHS, DATE_TIME, THIS_YEAR, ALL, YEAR, MONTH, ENTRY_T


class YearMonthReport(Report):
    def __init__(self, col_signature=''):
        super(YearMonthReport, self).__init__()
        self.year_col = None
        self.month_col = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        self.col_signature = col_signature

    def initialize(self):
        self.df = pd.DataFrame()
        self.df[STRATEGY] = None
        self.df[RULE] = None
        self.df[TOTAL] = None
        # will define time frame columns in run time

    def generate(self, strategies: list, trade_summary: pd.DataFrame):
        
        start_year = dtStr_to_dt(trade_summary.at[0, ENTRY_T]).year
        self.year_col = range(start_year, THIS_YEAR+1)

        # define columns
        for i in range(start_year, THIS_YEAR+1):
            self.df[str(i)] = None
        for i in range(1, 12+1):
            self.df[MONTHS[i]] = None

        # calculation - all
        new_row = self.get_return(trade_summary, ALL, ALL)
        self.df = self.df.append(new_row, ignore_index=True)

        # calculation - strategy
        for strategy in strategies:
            new_row = self.get_return(trade_summary, strategy.name, ALL)
            self.df = self.df.append(new_row, ignore_index=True)

        # calculation - rule
        for strategy in strategies:
            for rule in strategy.close_position.rules:
                new_row = self.get_return(trade_summary, strategy.name, rule.name)
                self.df = self.df.append(new_row, ignore_index=True)

        self.add_col_signature()

    def get_return(self, trade_summary: pd.DataFrame, strategy: str, rule: str) -> dict:
        if strategy == ALL and rule == ALL:
            return self.get_all_return(trade_summary)
        elif rule == ALL:
            return self.get_strategy_return(trade_summary, strategy)
        else:
            return self.get_rule_return(trade_summary, strategy, rule)

    def get_all_return(self, trade_summary: pd.DataFrame) -> dict:
        new_row = {
            STRATEGY:   ALL,
            RULE:       ALL
        }
        calculation = self.calculate_by_year_month(trade_summary)
        new_row.update(calculation)
        return new_row
    
    def get_strategy_return(self, trade_summary: pd.DataFrame, strategy: str) -> dict:
        new_row = {
            STRATEGY:   strategy,
            RULE:       ALL
        }
        calculation = self.calculate_by_year_month(trade_summary[trade_summary[STRATEGY] == strategy])
        new_row.update(calculation)
        return new_row

    def get_rule_return(self, trade_summary: pd.DataFrame, strategy: str, rule: str) -> dict:
        new_row = {
            STRATEGY:   strategy,
            RULE:       rule
        }
        calculation = self.calculate_by_year_month(trade_summary[(trade_summary[STRATEGY] == strategy) & (trade_summary[RULE] == rule)])
        new_row.update(calculation)
        return new_row

    def calculate_by_year_month(self, trade_summary: pd.DataFrame) -> dict:
        calculation = {}
        df = trade_summary
        df[YEAR] = df[ENTRY_T].apply(lambda dt: dtStr_to_dt(dt).year)
        df[MONTH] = df[ENTRY_T].apply(lambda dt: dtStr_to_dt(dt).month)

        # total
        calculation[TOTAL] = self.compute(df)
        # by year
        for year in self.year_col:
            calculation[str(year)] = self.compute(df[df[YEAR] == year])
        # by month
        for month in self.month_col:
            calculation[MONTHS[month]] = self.compute(df[df[MONTH] == month])
        
        return calculation

    @staticmethod
    def compute(trade_summary: pd.DataFrame):
        raise NotImplementedError

    def add_col_signature(self):
        self.update_col_signature(TOTAL)
        for year in self.year_col:
            self.update_col_signature(str(year))
        for month in self.month_col:
            self.update_col_signature(MONTHS[month])

    def update_col_signature(self, old_col_name):
        new_col_name = '{}_{}'.format(old_col_name, self.col_signature)
        self.df[new_col_name] = self.df[old_col_name]
        self.df = self.df.drop(columns=[old_col_name])