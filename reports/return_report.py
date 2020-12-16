import pandas as pd
import numpy as np

from config import RETURN, GEO_RETURN_SIG
from .year_month_report import YearMonthReport


class ReturnReport(YearMonthReport):
    def __init__(self):
        super(ReturnReport, self).__init__(GEO_RETURN_SIG)

    @staticmethod
    def compute(trade_summary: pd.DataFrame) -> float:
        return np.prod(trade_summary[RETURN] + 1) - 1