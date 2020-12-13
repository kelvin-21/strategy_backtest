import pandas as pd

from preset_strategy import CCIBullishStrategyCreator, CCIBearishStrategyCreator
from backtest import Backtest


def main():
    
    cci_bullish_strategy_creator = CCIBullishStrategyCreator(
        period = 30,
        ground = -170, 
        sky = 100, 
        stop_gain = None, 
        stop_loss = -300)
    CCI_bull_strategy = cci_bullish_strategy_creator.create()

    cci_bearish_strategy_creator = CCIBearishStrategyCreator(
        period = 30,
        ground = -170, 
        sky = 100, 
        stop_gain = None, 
        stop_loss = 300)
    CCI_bear_strategy = cci_bearish_strategy_creator.create()

    df = pd.read_csv('data/hsi_hourly.csv')
    strategies = [CCI_bull_strategy, CCI_bear_strategy]
    backtest = Backtest(df, strategies)
    backtest.run()


if __name__ == '__main__':
    main()