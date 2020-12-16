import pandas as pd
import numpy as np

from config import OPEN_POSITION, CLOSE_POSITION, DATE_TIME
from reports import TradeSummary, GeneralReport, ReturnReport, OccurrenceReport

class BacktestReport():
    def __init__(self):
        self.trade_summary = TradeSummary()
        self.general_report = GeneralReport()
        self.return_report = ReturnReport()
        self.occurrence_report = OccurrenceReport()

    def initialize(self, strategies):
        self.trade_summary.initialize()
        self.general_report.initialize()
        self.return_report.initialize()
        self.occurrence_report.initialize()

    def generate_report(self, strategies: list, trade_record: pd.DataFrame):
        self.trade_summary.generate(strategies, trade_record)
        self.general_report.generate(strategies, self.trade_summary.df)
        self.return_report.generate(strategies, self.trade_summary.df)
        self.occurrence_report.generate(strategies, self.trade_summary.df)