###############################################################################
# FILENAME: batch.py
# CLIENT: Chainview Capital
# AUTHOR: Matt Hartigan
# DATE CREATED: 3-June-2022
# DESCRIPTION: FIXME
###############################################################################
import os
import datetime
import importlib


# LOAD CREDENTIALS
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"


# CONFIG
strategy_directory = 'strategies'
strategy_runfile_name = 'main'
strategy_runfile_method = 'run_strategies'
strategy_run_list = [
    'cci',
    # 'projectx'
]


# FUNCTIONS
def run_batches():

    for strategy in os.listdir(strategy_directory):    # find every available strategy for testing

        if strategy in strategy_run_list:    # confirm whether we want to run it

            print('Running batch backtest for: {}'.format(strategy) + ' [' + str(datetime.datetime.utcnow()) + ']')
            import_path = ".".join([strategy_directory, strategy, strategy_runfile_name])    # define the strategy module location
            module = importlib.import_module(import_path)    # import module
            method = getattr(module, strategy_runfile_method)    # extract run method
            method()    # execute run method


# RUN BATCH TEST
if __name__ == '__main__':
    print('\nStarting up the CVC Offline Backtester [' + str(datetime.datetime.utcnow()) + ']\n')
    run_batches()
    print('\nCVC Offline Backtester is finished running! [' + str(datetime.datetime.utcnow()) + ']\n')
