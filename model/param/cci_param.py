from model.param import IndicatorParam
from config import TI_CCI

class CCIParam(IndicatorParam):
    def __init__(self, period, coeff):
        super().__init__(TI_CCI)
        self.period = period
        self.coeff = coeff