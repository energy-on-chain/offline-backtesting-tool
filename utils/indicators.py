###############################################################################
# PROJECT: CVC Trading Bot
# AUTHOR: Matt Hartigan
# DATE: 4-Jan-2022
# FILENAME: indicators.py
# DESCRIPTION: Library of indicator functions for CVC trading bots.
###############################################################################
import statistics
import pandas as pd
import numpy as np


def bollinger_band_width(input_df, column_label, rolling_window, standard_deviation):
    """ Classic bollinger band width calculation. Takes an input pandas data 
    frame, computes the bollinger band width for the input column at the input
    rolling window using the input standard deviation, then returns the original
    input data frame with the bollinger band results columns appended. """

    df = input_df.copy()    # make copy of input df

    df['std'] = df[column_label].rolling(rolling_window).std()    # calc rolling standard deviation

    df['bb_mid'] = df[column_label].rolling(rolling_window).mean()    # calculate rolling mean (BB midpoint)
    df['bb_top'] = df['bb_mid'] + (standard_deviation * df['std'])    # create top band    
    df['bb_bot'] = df['bb_mid'] - (standard_deviation * df['std'])    # create bottom band
    df['bb_width'] = (df['bb_top'] - df['bb_bot']) / df['bb_mid']    # calculate (normalized) width

    df.drop('std', axis=1, inplace=True)    # drop unnecessary columns from output
    
    return df


def cci(input_df, high_label, low_label, close_label, rolling_window):
    """ Classic commodity channel index (CCI) indicator. CCI is a momentum based oscillator that
    is used to help assess whether an asset is overbought or oversold. This function takes an 
    input pandas data frame, computes rolling CCI based on the given input values, then returns the
    original input data frame with the cci value column appended.
    
    Formula:
    CCI = (Typical Price - Moving Average) / (CCI Factor * Mean Deviation)
    ...where Typical Price = (High + Low + Close) / 3

    source: https://www.investopedia.com/terms/c/commoditychannelindex.asp
    """

    df = input_df.copy()    # make copy of input df

    lambert_constant = 0.015

    df['typical_price'] = (df[high_label] + df[low_label] + df[close_label]) / 3    # calculate typical price
    df['typical_price_sma'] = df['typical_price'].rolling(rolling_window).mean()    # calculate typical price rolling sma

    for x in range(0, rolling_window):    # add a shifted typical price column for each sma period
        col_name = 'tp_shift_' + str(x)
        df[col_name] = df['typical_price'].shift(periods=x) 

    df['mean_deviation'] = 0    # initialize mean_deviation col
    for x in range(0, rolling_window):    # sum the abs difference between sma and prev [rolling window] typical prices
        col_name = 'tp_shift_' + str(x)
        df['mean_deviation'] = df['mean_deviation'] + abs(df['typical_price_sma'] - df[col_name])

    df['mean_deviation_adj'] = df['mean_deviation'] / rolling_window    # normalize by size of rolling window

    df['cci'] = (df['typical_price'] - df['typical_price_sma']) / (lambert_constant * df['mean_deviation_adj'])    # calculate cci

    df.drop('typical_price', axis=1, inplace=True)    # drop unnecessary columns from output
    df.drop('typical_price_sma', axis=1, inplace=True)
    df.drop('mean_deviation', axis=1, inplace=True)
    df.drop('mean_deviation_adj', axis=1, inplace=True)
    for x in range(0, rolling_window):    
        col_name = 'tp_shift_' + str(x)
        df.drop(col_name, axis=1, inplace=True) 

    return df


def rsi(input_df, close_label, rolling_window):
    """ Classic Wilder's relative strength index (RSI) indicator. Measures the momentum of an asset by comparing
    how quickly people are bidding the price up or down. 30 is typically considered oversold, 70 is typically 
    considered overbought.
    
        source: https://www.alpharithms.com/relative-strength-index-rsi-in-python-470209/
        source: https://school.stockcharts.com/doku.php?id=technical_indicators:relative_strength_index_rsi
    """
    df = input_df.copy()

    df['previous_close'] = df[close_label].shift(periods=1)    # calcluate price change
    df['change'] = df[close_label] - df['previous_close']

    df['gain'] = df['change'].clip(lower=0)
    df['loss'] = abs(df['change'].clip(upper=0))

    df['avg_gain'] = df['gain'].rolling(window=rolling_window, min_periods=rolling_window).mean()[:rolling_window+1]    # get regular sma for gains
    df['avg_loss'] = df['loss'].rolling(window=rolling_window, min_periods=rolling_window).mean()[:rolling_window+1]    # get regular sma for losses

    for i, row in enumerate(df['avg_gain'].iloc[rolling_window+1:]):    # calculate Wilder-method-specific moving averages
        df['avg_gain'].iloc[i + rolling_window + 1] = (df['avg_gain'].iloc[i + rolling_window] * (rolling_window - 1) + df['gain'].iloc[i + rolling_window + 1]) / rolling_window

    for i, row in enumerate(df['avg_loss'].iloc[rolling_window+1:]):    # calculate Wilder-method-specific moving averages
        df['avg_loss'].iloc[i + rolling_window + 1] = (df['avg_loss'].iloc[i + rolling_window] * (rolling_window - 1) + df['loss'].iloc[i + rolling_window + 1]) / rolling_window

    df['rs'] = df['avg_gain'] / df['avg_loss']    # calculate rs
    df['rsi'] = 100 - (100 / (1 + df['rs']))    # calculate rsi

    df.drop('previous_close', axis=1, inplace=True)    # drop unnecessary columns from output
    df.drop('change', axis=1, inplace=True)
    df.drop('gain', axis=1, inplace=True)
    df.drop('loss', axis=1, inplace=True)
    df.drop('avg_gain', axis=1, inplace=True)
    df.drop('avg_loss', axis=1, inplace=True)
    df.drop('rs', axis=1, inplace=True)

    return df


# TODO:
# volatility
# zlema
# vwap
# mfi
# roc
# momentume
# cmo
