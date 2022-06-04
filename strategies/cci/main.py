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
from strategies.cci import report


# CONFIG
path = 'strategies/cci'
runfile_method = 'apply_strategy'
attribute_method = 'get_attributes'
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
    strategy_results_dict = {}
    strategy_summary_dict = {}
    for strategy in os.listdir(path):

        if strategy in strategy_run_list:

            input_df = df.copy()

            # APPLY STRATEGY
            import_path = ".".join(['strategies', 'cci', strategy.replace(".py", "")])    # define the strategy module location
            module = importlib.import_module(import_path)    # import module
            run_method = getattr(module, runfile_method)    # extract run method
            attr_method = getattr(module, attribute_method)
            strategy_df = run_method(input_df)    # execute run method

            # EVALUATE PERFORMANCE
            evaluate_df = performance.sum_capital_invested(strategy_df, bet, 'Close', 'action')
            evaluate_df = performance.sum_btc_accumulated(strategy_df, bet, 'Close', 'action')

            # SAVE RESULTS
            strategy_results_dict['cci_' + strategy.replace(".py", "")] = evaluate_df
            strategy_summary_dict['cci_' + strategy.replace(".py", "")] = attr_method()
            strategy_summary_dict['cci_' + strategy.replace(".py", "")]['num_triggers'] = evaluate_df['action'].value_counts().Buy
            strategy_summary_dict['cci_' + strategy.replace(".py", "")]['final_btc_balance'] = round(evaluate_df['rolling_btc_received'].iloc[-1], 3)

    # GENERATE REPORT
    general_params = {
        'time_history': cutoff_string,
        'starting_capital': starting_capital,
        'bet': bet,
        'table_headers': ['Name', 'Lookback (days)', 'Threshold', 'Num. Triggers', 'Final BTC Balance']
    }
    report.generate_report(general_params, strategy_summary_dict, strategy_results_dict)

    

