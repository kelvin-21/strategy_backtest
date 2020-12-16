import pandas as  pd
import numpy as np

from service import DataCleaner, TechIndicatorEngine, CCI, SMA
from config import DATE_TIME, CLOSE, OPEN_POSITION, CLOSE_POSITION, NO_EVENT, BULLISH, BEARISH
from utilities import object_list_contains_object
from backtest_report import BacktestReport
from backtest_trade_record import BacktestTradeRecord

class Backtest():
    
    def __init__(self, raw_data, strategies):
        
        # class data
        self.data = raw_data
        self.trade_record = BacktestTradeRecord()
        self.report = BacktestReport()
        self.strategies = strategies
        self.all_ti_param = list()
        
        # service
        self.cleaner = DataCleaner()
        self.ti_engine = TechIndicatorEngine()
        
    def initialize(self):
        self.trade_record.initialize()
        self.report.initialize(self.strategies)
        self.initialize_all_ti_param()
        print('[BACKTEST] Initializated')
        
    def initialize_all_ti_param(self):
        for strategy in self.strategies:
            for rule in (strategy.open_position.rules + strategy.close_position.rules):
                for param in rule.indicators_param:
                    
                    if param.name not in self.data.columns:
                        if not object_list_contains_object(self.all_ti_param, param):
                            
                            name = self.make_name([i.name for i in self.all_ti_param], param.name)
                            rule.ref[param.name] = name
                            param.name = name
                            self.all_ti_param.append(param)
                           
    @staticmethod
    def make_name(name_list, target):
        if target not in name_list:
            return target
        i = 2
        while(True):
            new_name = target + '_{}'.format(i)
            if new_name not in name_list:
                return new_name
            i += 1
    
    def data_preprocess(self):
        self.data = self.cleaner.clean(self.data)
        print('[BACKTEST] Finished data pre-process')
        
    def compute_technical_indicator(self):
        for param in self.all_ti_param:
            self.data = self.ti_engine.compute(self.data, param)
        print('[BACKTEST] Finished computation on technical indicators')
        
    def back_test(self):
        for i in self.data.index:
            for strategy in self.strategies:
                event, rule = strategy.check_event(self.data, i)
                if event is not NO_EVENT:
                    date_time = self.data.at[i, DATE_TIME]
                    price = self.data.at[i, CLOSE]
                    self.trade_record.record_event(date_time, strategy, event, rule, price)
        self.trade_record.calculate_return(self.strategies)
        print('[BACKTEST] Finished all backtest')
    
    def gen_report(self):
        self.report.generate_report(self.strategies, self.trade_record.df)
        print('[BACKTEST] Generated all reports')
    
    def run(self):
        self.initialize()
        self.data_preprocess()
        self.compute_technical_indicator()
        self.back_test()
        self.gen_report()
        return