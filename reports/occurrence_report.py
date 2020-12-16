import pandas as pd
import numpy as np

from config import RETURN, OCC_SIG
from .year_month_report import YearMonthReport


class OccurrenceReport(YearMonthReport):
    def __init__(self):
        super(OccurrenceReport, self).__init__(OCC_SIG)

    def generate(self, strategies: list, trade_summary: pd.DataFrame):
        super(OccurrenceReport, self).generate(strategies, trade_summary)
        self.df = self.df.fillna(0)

    @staticmethod
    def compute(trade_summary: pd.DataFrame) -> int:
        return len(trade_summary)