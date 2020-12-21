import pandas as pd
from typing import Tuple
import logging

from model import FieldToTune
from reports import StrategyTunerReport
from backtest import Backtest
from utilities import Timer


class StrategyTuner():
    def __init__(self, raw_data: pd.DataFrame, strategy_creator, fields_to_tune: tuple, need_recompute_ti=False):
        self.data = raw_data
        self.strategy_creator = strategy_creator
        self.fields_to_tune = fields_to_tune
        self.need_recompute_ti = need_recompute_ti
        self.strategy = None
        self.backtest = None
        self.report = None
        self.timer = Timer()

        self.initialize()

    def initialize(self):
        # strategy
        self.update_strategy_param()

        # backtest
        self.initialize_backtest()

        # report
        self.report = StrategyTunerReport(self.strategy, self.strategy_creator)

    def initialize_backtest(self):
        self.backtest = Backtest(self.data, [self.strategy])
        self.backtest.initialize()
        self.backtest.data_preprocess()
        self.backtest.compute_technical_indicator()

    def simulate(self, param_values: list):
        self.update_strategy_param(param_values)
        param_config = self.strategy_creator.__dict__
        
        if self.report.param_already_exists(param_config):
            logging.warn(f'[StrategyTuner] Skipping this param because it is already simulated: {param_config}')
            return

        self.backtest.strategies = [self.strategy]
        self.backtest.initialize()
        if self.need_recompute_ti:
            self.initialize_backtest()
        self.backtest.back_test()
        self.backtest.gen_report(only='general_report')

        self.record_simulation()
    
    def record_simulation(self):
        backtest_result = dict(self.backtest.report.general_report.df.iloc[0])
        param_config = self.strategy_creator.__dict__
        self.report.write(backtest_result, param_config)

    def update_strategy_param(self, param_values=None):
        if not param_values:
            for field in self.fields_to_tune:
                self.strategy_creator.__dict__[field.name] = field.low_bound
        else:
            for i in range(len(self.fields_to_tune)):
                field = self.fields_to_tune[i]
                self.strategy_creator.__dict__[field.name] = field.values[param_values[i]] # TO DO: param_values list

        self.strategy = self.strategy_creator.create()

    # recursion
    def do_step(self, counters, lengths, level):
        if level == len(counters):
            self.simulate(param_values=counters)
            msg = self.write_step_msg(counters)
            self.timer.time(msg)
        else:
            counters[level] = 0
            while True:
                if counters[level] >= lengths[level]:
                    break
                # do something
                self.do_step(counters, lengths, level + 1)
                counters[level] += 1

    def write_step_msg(self, param_values: list):
        d = dict()
        for i in range(len(self.fields_to_tune)):
            field = self.fields_to_tune[i]
            d[field.name] = field.values[param_values[i]]
        return str(d)

    def run(self):
        counters = [0] * len(self.fields_to_tune)
        lengths = [len(field.values) for field in self.fields_to_tune]
        self.do_step(counters, lengths, 0)