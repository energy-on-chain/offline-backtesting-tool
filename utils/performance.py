###############################################################################
# FILENAME: performance.py
# CLIENT: Chainview Capital
# AUTHOR: Matt Hartigan
# DATE CREATED: 31 May 2022
# DESCRIPTION: Library of performance evaluation functions for CVC backtester.
# Pick any one of them off the shelf, plug in the appropriate inputs, and get 
# the specified return value(s). All functions in the production version of 
# this library have been QA'd.
###############################################################################
import pandas as pd
import numpy as np


def sum_capital_invested(input_df, bet, price_label, action_label):
    """ Logs the input bet amount every time a "Buy" action occurs in the input action
    column. Then performs a cumulative sum on those bets to determine how much capital was
    invested over the full time history. Returns the input data frame with these two 
    columns appended. """

    df = input_df.copy()

    df['capital_invested'] = np.where(df[action_label] == 'Buy', bet, 0)    # log a bet every time the buy signal occurs
    df['rolling_capital_invested'] = df['capital_invested'].cumsum()    # sum those bets over the full time history

    return(df)


def sum_btc_accumulated(input_df, bet, price_label, action_label):
    """ Logs the BTC received every time a "Buy" action occurs in the input action
    column. Then performs a cumulative sum on those BTC to determine how much was
    accumulated over the full time history. Returns the input data frame with these two 
    columns appended. """

    df = input_df.copy()

    df['btc_received'] = np.where(df[action_label] == 'Buy', bet / df['Close'], 0)    # tally the btc received every time a buy is made
    df['rolling_btc_received'] = df['btc_received'].cumsum()    # sum that btc over the full time history

    return(df)


# TODO:
# SHARPE RATIO
# SORTINO RATIO
# DUMMY PORTFOLIO P&L
# WIN PERCENTAGE
# MAX WIN
# MAX LOSS
# AVERAGE WIN / LOSS
# Plots...?

