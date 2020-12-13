from model.param import IndicatorParam
from config import TI_SMA

class SMAParam(IndicatorParam):
    def __init__(self, period, on):
        super().__init__(TI_SMA)
        self.period = period
        self.on = on