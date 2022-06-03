###############################################################################
# FILENAME: batch.py
# CLIENT: Chainview Capital
# AUTHOR: Matt Hartigan
# DATE CREATED: 3-June-2022
# DESCRIPTION: FIXME
###############################################################################
import os
import datetime


# LOAD CREDENTIALS
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"


# CONFIG
strategy_directory = 'strategies/'
strategy_run_list = [
    'cci',
    # 'projectx'
]


# FUNCTIONS
def run_batches():
    for strategy in os.listdir(strategy_directory):
        if strategy in strategy_run_list:

            print('Running backtests for: {}'.format(strategy) + ' [' + str(datetime.datetime.utcnow()) + ']\n')
            strategy_subdirectory = strategy_directory + strategy
            # FIXME: import run_strategies and trigger it


# RUN BATCH TEST
if __name__ == '__main__':
    print('\nStarting up the CVC Offline Backtester [' + str(datetime.datetime.utcnow()) + ']\n')
    run_batches()
    print('CVC Offline Backtester is finished running! [' + str(datetime.datetime.utcnow()) + ']\n')
