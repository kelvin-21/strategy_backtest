import logging

from config.const import TI_CCI, TI_SMA
from .cci import CCI
from .sma import SMA

class TechIndicatorEngine():
    def __init__(self):
        pass
    
    def compute(self, data, ti_param):
        if self.extract_alphabet(ti_param.name) == TI_CCI:
            cci = CCI(ti_param)
            data = cci.compute(data)
        elif self.extract_alphabet(ti_param.name) == TI_SMA:
            sma = SMA(ti_param)
            data = sma.compute(data)
        else:
            raise ValueError('[ERROR] Unknown technical indicator: {}'.format(ti_param.name))
        
        logging.info('[TechIndicatorEngine] Finished computation of {}'.format(ti_param.name))
        return data
    
    @staticmethod
    def extract_alphabet(s):
        return ''.join(x for x in s if x.isalpha())