from model import Rule, Strategy
from model.param import IndicatorParam, CCIParam, OpenPositionParam, ClosePositionParam
from config import CLOSE, BEARISH, TI_CCI

class CCIBearishStrategyCreator():
    
    def __init__(self, period=20, ground=-100, sky=100, stop_gain=None, stop_loss=None):
        self.period = period
        self.ground = ground
        self.sky = sky
        self.stop_gain = stop_gain
        self.stop_loss = stop_loss
    
    def create(self):
       
        rule = Rule(
            name = 'basic', 
            indicators_param = [CCIParam(self.period, 0.015)],
            ref = {TI_CCI: TI_CCI},
            f = lambda data, ref, entry_i, i: (data.at[i-1, ref[TI_CCI]] > self.sky) & (data.at[i, ref[TI_CCI]] < self.sky))

        open_position_param = OpenPositionParam(rules=[rule])

        rule = Rule(
            name = 'basic', 
            indicators_param = [CCIParam(self.period, 0.015)],
            ref = {TI_CCI: TI_CCI},
            f = lambda data, ref, entry_i, i: (data.at[i-1, ref[TI_CCI]] > self.ground) & (data.at[i, ref[TI_CCI]] < self.ground))
        
        rule_rebound_exit = Rule(
            name = 'rebound_exit',
            indicators_param = [CCIParam(self.period, 0.015)],
            ref = {TI_CCI: TI_CCI},
            f = lambda data, ref, entry_i, i: (data.at[i-1, ref[TI_CCI]] < self.sky) & (data.at[i, ref[TI_CCI]] > self.sky))

        rules = [rule, rule_rebound_exit]

        if self.stop_gain is not None:
            if abs(self.stop_gain) < 1:
                f = lambda data, ref, entry_i, i: (data.at[i, CLOSE] - data.at[entry_i, CLOSE]) / data.at[entry_i, CLOSE] < self.stop_gain
            else:
                f = lambda data, ref, entry_i, i: (data.at[i, CLOSE] - data.at[entry_i, CLOSE]) < self.stop_gain
            rule_stop_gain = Rule(
                name = 'stop_gain', 
                indicators_param = [IndicatorParam(CLOSE)], 
                ref = {CLOSE: CLOSE}, 
                f = f)
            rules.append(rule_stop_gain)

        if self.stop_loss is not None:
            if abs(self.stop_loss) < 1:
                f = lambda data, ref, entry_i, i: (data.at[i, CLOSE] - data.at[entry_i, CLOSE]) / data.at[entry_i, CLOSE] > self.stop_loss
            else:
                f = lambda data, ref, entry_i, i: (data.at[i, CLOSE] - data.at[entry_i, CLOSE]) > self.stop_loss
            rule_stop_loss = Rule(
                name = 'stop_loss', 
                indicators_param = [IndicatorParam(CLOSE)], 
                ref = {CLOSE: CLOSE}, 
                f = f)
            rules.append(rule_stop_loss)

        close_position_param = ClosePositionParam(rules=rules)

        return Strategy('CCI_bear_strategy', open_position_param, close_position_param, BEARISH)