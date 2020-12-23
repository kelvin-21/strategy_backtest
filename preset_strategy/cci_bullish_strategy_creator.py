from model import Rule, Strategy
from model.param import IndicatorParam, CCIParam, OpenPositionParam, ClosePositionParam
from config import CLOSE, BULLISH, TI_CCI

class CCIBullishStrategyCreator():
    
    def __init__(self, period=20, ground=-100, sky=100, stop_gain=None, stop_loss=None, rebound_channel=None):
        self.period = period
        self.ground = ground
        self.sky = sky
        self.stop_gain = stop_gain
        self.stop_loss = stop_loss
        self.rebound_channel = rebound_channel
    
    def create(self):
       
        basic_open_rule = self.basic_open_rule()
        open_position_param = OpenPositionParam(rules=[basic_open_rule])

        close_position_rules = []

        close_position_rules.append(self.basic_close_rule())
        close_position_rules.append(self.rebound_ground_exit_rule())
        if self.stop_gain:
            close_position_rules.append(self.stop_gain_rule())
        if self.stop_loss:
            close_position_rules.append(self.stop_loss_rule())
        if self.rebound_channel:
            close_position_rules.append(self.rebound_channel_rule())

        close_position_param = ClosePositionParam(rules=close_position_rules)

        return Strategy('CCI_bull_strategy', open_position_param, close_position_param, BULLISH)

    def basic_open_rule(self):
        rule = Rule(
            name = 'basic_open_pos', 
            indicators_param = [CCIParam(self.period, 0.015)],
            ref = {TI_CCI: TI_CCI},
            f = lambda data, ref, entry_i, i: (data.at[i-1, ref[TI_CCI]] < self.ground) & (data.at[i, ref[TI_CCI]] > self.ground)
        )
        return rule

    def basic_close_rule(self):
        rule = Rule(
            name = 'basic_close_pos', 
            indicators_param = [CCIParam(self.period, 0.015)],
            ref = {TI_CCI: TI_CCI},
            f = lambda data, ref, entry_i, i: (data.at[i-1, ref[TI_CCI]] < self.sky) & (data.at[i, ref[TI_CCI]] > self.sky)
        )
        return rule

    def rebound_ground_exit_rule(self):
        rule = Rule(
            name = 'rebound_ground_exit',
            indicators_param = [CCIParam(self.period, 0.015)],
            ref = {TI_CCI: TI_CCI},
            f = lambda data, ref, entry_i, i: (data.at[i-1, ref[TI_CCI]] > self.ground) & (data.at[i, ref[TI_CCI]] < self.ground)
        )
        return rule

    def stop_gain_rule(self):
        if abs(self.stop_gain) < 1:
            f = lambda data, ref, entry_i, i: (data.at[i, CLOSE] - data.at[entry_i, CLOSE]) / data.at[entry_i, CLOSE] > self.stop_gain
        else:
            f = lambda data, ref, entry_i, i: (data.at[i, CLOSE] - data.at[entry_i, CLOSE]) > self.stop_gain
        rule = Rule(
            name = 'stop_gain', 
            indicators_param = [IndicatorParam(CLOSE)], 
            ref = {CLOSE: CLOSE}, 
            f = f
        )
        return rule

    def stop_loss_rule(self):
        if abs(self.stop_loss) < 1:
            f = lambda data, ref, entry_i, i: (data.at[i, CLOSE] - data.at[entry_i, CLOSE]) / data.at[entry_i, CLOSE] < self.stop_loss
        else:
            f = lambda data, ref, entry_i, i: (data.at[i, CLOSE] - data.at[entry_i, CLOSE]) < self.stop_loss
        rule = Rule(
            name = 'stop_loss', 
            indicators_param = [IndicatorParam(CLOSE)], 
            ref = {CLOSE: CLOSE}, 
            f = f
        )
        return rule

    def rebound_channel_rule(self):
        first_gate = self.ground + (self.sky - self.ground) * self.rebound_channel[0]
        second_gate = self.ground + (self.sky - self.ground) * self.rebound_channel[1]
        rule = Rule(
            name = 'rebound_channel_exit',
            indicators_param = [CCIParam(self.period, 0.015)],
            ref = {TI_CCI: TI_CCI},
            f = lambda data, ref, entry_i, i: ((data[entry_i:i][data[ref[TI_CCI]] > first_gate].shape[0] > 0) & (data.at[i, ref[TI_CCI]] < second_gate))
        )
        return rule