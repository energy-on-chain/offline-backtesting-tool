###############################################################################
# FILENAME: main.py
# CLIENT: Chainview Capital
# AUTHOR: Matt Hartigan
# DATE CREATED: 31 May 2022
# DESCRIPTION: FIXME
###############################################################################
import os
import importlib
import pandas as pd
import numpy as np
import datetime
import statistics as stats
import math

from google.cloud import storage

from utils import performance


# CONFIG
path = 'strategies/cci'
runfile_method = 'apply_strategy'
cutoff_string = "2020-01-01"
starting_capital = 10000    # usd
bet = 100    # usd
strategy_run_list = [
    'strategy1.py',
    'strategy2.py',
    'strategy3.py',
]


# FUNCTIONS
def run_strategies():

    print('Evaluating CCI strategy performance... [' + str(datetime.datetime.utcnow()) + ']\n')

    # LOAD DATA
    df = pd.read_csv('gs://chainview-capital-dashboard-bucket-official/bots/bot_6/finage_ohlc_BTCUSD_60minute_fast.csv')

    # CLEAN DATA
    df.columns = [ "Open", "High", "Low", "Close", "Volume", "Unix", "UTC"]    # rename columns
    df['UTC'] = df['UTC'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))    # add utc
    df = df[(df['UTC'] >= cutoff_string)]    # only take data from cutoff string onwards

    # RUN BACKTESTS
    backtest_result_dict = {}
    for strategy in os.listdir(path):

        if strategy in strategy_run_list:

            input_df = df.copy()

            # APPLY STRATEGY
            import_path = ".".join(['strategies', 'cci', strategy.replace(".py", "")])    # define the strategy module location
            module = importlib.import_module(import_path)    # import module
            method = getattr(module, runfile_method)    # extract run method
            strategy_df = method(input_df)    # execute run method

            # EVALUATE PERFORMANCE
            evaluate_df = performance.sum_capital_invested(strategy_df, bet, 'Close', 'action')
            evaluate_df = performance.sum_btc_accumulated(strategy_df, bet, 'Close', 'action')

            # SAVE RESULTS
            backtest_result_dict[strategy.replace(".py", "")] = evaluate_df
            
    print(backtest_result_dict)
