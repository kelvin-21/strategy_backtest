import pandas as pd
import logging
import sys

from preset_strategy import CCIBullishStrategyCreator, CCIBearishStrategyCreator
from backtest import Backtest
from strategy_tuner import StrategyTuner
from model import FieldToTune
from utilities import write_new_sheet, Timer
from config import DATE_TIME

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

root = logging.getLogger()
root.setLevel(logging.DEBUG)

fh = logging.FileHandler('logs/backtest.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.INFO)
sh.setFormatter(formatter)

root.addHandler(fh)
root.addHandler(sh)


def run_backtest():

    timer = Timer()

    cci_bullish_strategy_creator = CCIBullishStrategyCreator(
        period = 20,
        ground = -75,
        sky = 180,
        stop_gain = None,
        stop_loss = -300,
        rebound_channel = (0.8, 0.5)
    )
    
    cci_bearish_strategy_creator = CCIBearishStrategyCreator(
        period = 20,
        ground = -105, 
        sky = 50, 
        stop_gain = -950, 
        stop_loss = 400,
        rebound_channel = (0.2, 0.5)
    )

    CCI_bull_strategy = cci_bullish_strategy_creator.create()
    CCI_bear_strategy = cci_bearish_strategy_creator.create()

    hsi_hourly = 'data/hsi_hourly.csv'
    hsi_hourly_cleaned_computed = 'data/hsi_hourly_cleaned_computed.csv'

    raw_data = pd.read_csv(hsi_hourly)
    # strategies = [CCI_bull_strategy, CCI_bear_strategy]
    strategies = [CCI_bear_strategy]
    backtest = Backtest(raw_data, strategies)

    backtest.initialize()
    timer.time('backtest.initialize()')

    backtest.data_preprocess()
    timer.time('backtest.data_preprocess()')
    
    backtest.compute_technical_indicator()
    timer.time('backtest.compute_technical_indicator()')

    backtest.back_test()
    timer.time('backtest.back_test()')

    backtest.gen_report()
    timer.time('backtest.gen_report()')

    file_name = 'output.xlsx'
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter') # pylint: disable=abstract-class-instantiated

    write_new_sheet(writer, backtest.report.general_report.df, 'general_report')
    write_new_sheet(writer, backtest.report.return_report.df, 'return_report')
    write_new_sheet(writer, backtest.report.occurrence_report.df, 'occurrence_report')
    write_new_sheet(writer, backtest.report.trade_summary.df, 'trade_summary')
    write_new_sheet(writer, backtest.trade_record.df, 'trade_record')
    write_new_sheet(writer, backtest.data, 'data')
    write_new_sheet(writer, pd.DataFrame(cci_bullish_strategy_creator.__dict__), 'param')
    writer.save()
    writer.close()
    print('[OUTPUT] Completed')

    timer.time('ExcelWriter')


def run_tuner():

    raw_data = pd.read_csv('data/hsi_hourly.csv')

    # cci_bull_strategy_creator = CCIBullishStrategyCreator(
    #     period = 20,
    #     ground = -150,
    #     sky = 190,
    #     rebound_channel = (0.8, 0.5)
    # )
    # fields_to_tune = (
    #     FieldToTune(name='stop_gain', low_bound=300, up_bound=1000+1, step=50, extra_values=[99999]),
    #     FieldToTune(name='stop_loss', low_bound=-300, up_bound=-1000-1, step=-50, extra_values=[-99999])
    # )

    cci_bear_strategy_creator = CCIBearishStrategyCreator(
        period = 20,
        ground = -105,
        sky = 50,
        rebound_channel = (0.2, 0.5)
    )
    fields_to_tune = (
        FieldToTune(name='stop_loss', low_bound=300, up_bound=1000+1, step=50, extra_values=[99999]),
        FieldToTune(name='stop_gain', low_bound=-300, up_bound=-1000-1, step=-50, extra_values=[-99999])
    )

    strategy_tuner = StrategyTuner(raw_data, cci_bear_strategy_creator, fields_to_tune)
    strategy_tuner.run()

def main():
    run_backtest()
    # run_tuner()


if __name__ == '__main__':
    main()