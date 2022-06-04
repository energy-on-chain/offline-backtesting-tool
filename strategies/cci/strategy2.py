###############################################################################
# FILENAME: strategy2.py
# CLIENT: Chainview Capital
# AUTHOR: Matt Hartigan
# DATE CREATED: 31 May 2022
# DESCRIPTION: Second strategy iteration for the CVC CCI bot.
###############################################################################
import datetime
import pandas as pd
import numpy as np

from utils import indicators


# CONFIG
name = 'cci_strategy2'
description = 'buy when 200 day cci threshold dips below -150'
lookback = 200    # days
threshold = -150    # cci points


def apply_strategy(input_df):

    print('Now evaluating: {} ['.format(name) + str(datetime.datetime.utcnow()) + ']')
    print('Strategy Description: {}'.format(description))

    df = input_df.copy()    # copy input data frame  

    df = indicators.cci(df, 'High', 'Low', 'Close', lookback)    # add cci

    df['action'] = np.where(df['cci'] < threshold, "Buy", "No Action")    # add action column with hold for every row that is under threshold

    print('Strategy evaluation complete! [' + str(datetime.datetime.utcnow()) + ']\n')

    return df
