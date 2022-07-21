###############################################################################
# FILENAME: strategy1.py
# PROJECT: EOC Offline Backtesting Tool
# CLIENT: 
# AUTHOR: Matt Hartigan
# DATE CREATED: 31 May 2022
# DESCRIPTION: First strategy iteration for the EOC Example #1 strategy.
###############################################################################
import datetime
import pandas as pd
import numpy as np

from utils import indicators


# CONFIG
name = 'example1_strategy1'
description = 'buy when 200 day cci threshold dips below -100'
lookback = 200    # days
threshold = -100    # cci points


def get_attributes():
    return {
        'name': name,
        'description': description,
        'lookback': lookback,
        'threshold': threshold
    }


def apply_strategy(input_df):

    print('Now evaluating: {} ['.format(name) + str(datetime.datetime.utcnow()) + ']')
    print('Strategy Description: {}'.format(description))

    df = input_df.copy()    # copy input data frame  

    df = indicators.cci(df, 'High', 'Low', 'Close', lookback)    # add cci

    df['action'] = np.where(df['cci'] < threshold, "Buy", "No Action")    # add action column with hold for every row that is under threshold

    print('Strategy evaluation complete! [' + str(datetime.datetime.utcnow()) + ']\n')

    return df
