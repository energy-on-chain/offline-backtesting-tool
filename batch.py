###############################################################################
# FILENAME: batch.py
# PROJECT: EOC Offline Backtesting Tool
# CLIENT: 
# AUTHOR: Matt Hartigan
# DATE CREATED: 31 May 2022
# DESCRIPTION: Defines what batch of trading strategies get run with what
# parameters in a given session.
###############################################################################
import os
import datetime
import importlib
import smtplib
from email.mime.base import MIMEBase
from email import encoders

from utils import autoemail


# LOAD CREDENTIALS
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""    # FIXME: add cloud credentials here


# CONFIG
strategy_directory = 'strategies'
output_directory = 'output'
strategy_runfile_name = 'main'
strategy_runfile_method = 'run_strategies'
strategy_run_list = [
    'example1',
    'example2',
    # FIXME: Add other strategy types here. These need to match the subfolder names in the "strategies" directory to be recognized.
]


# FUNCTIONS
def email_results():
""" Takes the output from the batch run, generates the appropriate pdf report with results, then emails it out to
the recipient list defined in the project config file. """

    for strategy in os.listdir(strategy_directory):    # find every available strategy for testing

        if strategy in strategy_run_list:    # confirm whether we want to run it

                print('Emailing results report for: {}'.format(strategy) + ' [' + str(datetime.datetime.utcnow()) + ']')

                # Write message
                subject = 'EOC Offline Bactest Results: ' + strategy + ' strategy'
                message = 'See attached pdf for backtest results summary.\n'
                footer = '\nThis email was sent automatically via the Energy On Chain Offline Backtesting system.'

                # Get attachment
                file_list = os.listdir(os.path.join(output_directory, strategy))
                pdf_name = None
                for file in file_list:
                    if 'pdf' in file:
                        pdf_name = os.path.join(output_directory, strategy, file)

                binary_pdf = open(pdf_name, 'rb')    # open in binary
                payload = MIMEBase('application', 'octate-stream', Name=pdf_name)
                payload.set_payload((binary_pdf).read())
                encoders.encode_base64(payload)    # encode binary to base 64
                payload.add_header('Content-Decomposition', 'attachment', filename=pdf_name)    # add header with pdf name
                attachment = payload

                autoemail.send_email_with_attachment(subject, message, footer, attachment)    # send the email


def run_batches():
"""" Finds and executes the 'run()' method for every strategy in the user-defined run list at the top of this file. """

    for strategy in os.listdir(strategy_directory):    # find every available strategy for testing

        if strategy in strategy_run_list:    # confirm whether we want to run it

            print('Running batch backtest for: {}'.format(strategy) + ' [' + str(datetime.datetime.utcnow()) + ']')
            import_path = ".".join([strategy_directory, strategy, strategy_runfile_name])    # define the strategy module location
            module = importlib.import_module(import_path)    # import module
            method = getattr(module, strategy_runfile_method)    # extract run method
            method()    # execute run method


# RUN BATCH TEST
if __name__ == '__main__':
    print('\nStarting up the EOC Offline Backtester [' + str(datetime.datetime.utcnow()) + ']\n')
    run_batches()
    email_results()
    print('\nEOC Offline Backtester is finished running! [' + str(datetime.datetime.utcnow()) + ']\n')
