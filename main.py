import pandas as pd

from preset_strategy import CCIBullishStrategyCreator, CCIBearishStrategyCreator
from backtest import Backtest
from utilities import write_new_sheet


def main():

    cci_bullish_strategy_creator = CCIBullishStrategyCreator(
        period = 30,
        ground = -170, 
        sky = 100, 
        stop_gain = None, 
        stop_loss = -300,
        rebound_channel = (0.8, 0.5)
    )
    CCI_bull_strategy = cci_bullish_strategy_creator.create()

    cci_bearish_strategy_creator = CCIBearishStrategyCreator(
        period = 30,
        ground = -170, 
        sky = 100, 
        stop_gain = None, 
        stop_loss = 300,
        rebound_channel = (0.2, 0.5)
    )
    CCI_bear_strategy = cci_bearish_strategy_creator.create()

    raw_data = pd.read_csv('data/hsi_hourly.csv')
    strategies = [CCI_bull_strategy, CCI_bear_strategy]
    backtest = Backtest(raw_data, strategies)
    backtest.run()

    file_name = 'output.xlsx'
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter') # pylint: disable=abstract-class-instantiated

    write_new_sheet(writer, backtest.report.general_report, 'general_report')
    write_new_sheet(writer, backtest.trade_summary.df, 'trade_summary')
    write_new_sheet(writer, backtest.trade_record.df, 'trade_record')
    write_new_sheet(writer, backtest.data, 'data')
    writer.save()
    writer.close()


if __name__ == '__main__':
    main()