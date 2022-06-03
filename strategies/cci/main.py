###############################################################################
# FILENAME: main.py
# CLIENT: Chainview Capital
# AUTHOR: Matt Hartigan
# DATE CREATED: 31 May 2022
# DESCRIPTION: This is the main file for the CVC Offline Backtesting System.
# By configuring and running it, you can coordinate which strategies get 
# executed / tested.
###############################################################################
import os
import pandas as pd
import numpy as np
import datetime
import statistics as stats
import math

from google.cloud import storage

from reports import header, footer


# CONFIG
cutoff_string = "01/01/2020"


# FUNCTIONS
def run_strategies():

    # LOAD DATA
    df = pd.read_csv('gs://chainview-capital-dashboard-bucket-official/bots/bot_6/finage_ohlc_BTCUSD_60minute_fast.csv')


    # CLEAN DATA
    df = input_df.copy()
    df.columns = [ "Open", "High", "Low", "Close", "Volume", "Unix", "UTC"]    # rename columns
    df['UTC'] = df['UTC'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))    # add utc
    df = df[(df['UTC'] >= cutoff_string)]    # only take data from cutoff string onwards


    # RUN BACKTESTS
    # create list of strategy filenames 
    # for every strategy in list

        # APPLY STRATEGY
        # import run and trigger it

        # EVALUATE PERFORMANCE

        # OUTPUT RESULTS
        # 

