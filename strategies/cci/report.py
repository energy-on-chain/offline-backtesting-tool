###############################################################################
# FILENAME: report.py
# CLIENT: Chainview Capital
# AUTHOR: Matt Hartigan
# DATE CREATED: 31 May 2022
# DESCRIPTION: FIXME
###############################################################################
import datetime
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from fpdf import FPDF
from sklearn.datasets import load_iris


# CLASSES
class PDF(FPDF):
    def header(self):
        # Logo
        self.image('assets/logo_dark.jpg', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(55)
        # Title
        self.cell(90, 10, 'CVC Offline Backtest Report - CCI Threshold Bot', 0, 0, 'C')
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


# FUNCTIONS
def generate_btc_time_history_plot(input_df, name):
    
    # Add traces
    fig, ax1 = plt.subplots()
    ax1.plot(input_df['UTC'], input_df['Close'], color='orange')
    ax2 = ax1.twinx()
    ax2.plot(input_df['UTC'], input_df['rolling_btc_received'], color='black')

    # Format y axes
    ax1.set_ylabel('Close Price', color='orange')
    ax2.set_ylabel('BTC Stack', color='black')

    ax1.tick_params(axis='y', colors='orange')
    ax1.tick_params(axis='x', rotation=45)
    ax2.tick_params(axis='y', colors='black')
    ax2.tick_params(axis='x', rotation=45)

    ax1.spines['left'].set_color('orange')
    ax2.spines['right'].set_color('black')

    # Format rest of plot
    plt.title('BTC Stack Time History: ' + name)
    plt.xlabel("Time (UTC)")
    plt.legend()

    plt.savefig('output/' + name + '_btc_time_history_plot.png')

    return fig


def generate_cci_time_history_plot(input_df, name, threshold):
    
    # Add traces
    fig, ax1 = plt.subplots()
    ax1.plot(input_df['UTC'], input_df['Close'], color='orange')
    ax2 = ax1.twinx()
    ax2.plot(input_df['UTC'], input_df['cci'], color='cyan')
    ax2.axhline(y=threshold, color='r', linestyle='--')

    # Format y axes
    ax1.set_ylabel('Close Price', color='orange')
    ax2.set_ylabel('CCI', color='cyan')

    ax1.tick_params(axis='y', colors='orange')
    ax1.tick_params(axis='x', rotation=45)
    ax2.tick_params(axis='y', colors='cyan')
    ax2.tick_params(axis='x', rotation=45)

    ax1.spines['left'].set_color('orange')
    ax2.spines['right'].set_color('cyan')

    # Format rest of plot
    plt.title('CCI Time History: ' + name)
    plt.xlabel("Time (UTC)")
    plt.legend()

    plt.savefig('output/' + name + '_cci_time_history_plot.png')

    return fig


def generate_report(general_params, strategy_summary_dict, strategy_results_dict):
    
    # INITIALIZE REPORT
    pdf = PDF()
    pdf.alias_nb_pages()

    # ADD SUMMARY PAGE
    pdf.add_page()
    pdf.set_font('Times', '', 12)
    pdf.cell(60)
    pdf.cell(75, 10,'General Results Summary', 0, 2, 'C')    # page title
    pdf.cell(90, 10, '', 0, 2, 'C')
    pdf.cell(-60)

    # General info listed
    pdf.cell(0, 10, 'Date of Run:       ' + str(datetime.datetime.utcnow()), 0, 1)
    pdf.cell(0, 10, 'Time History Covered:      ' + general_params['time_history'] + ' to Present', 0, 1)
    pdf.cell(0, 10, 'Num. Strategies Tested:        ' + str(len(strategy_results_dict)), 0, 1)
    pdf.cell(0, 10, 'Dummy Portfolio Starting Capital (usd):        $' + str(general_params['starting_capital']), 0, 1)
    pdf.cell(0, 10, 'Bet Size (usd):        $' + str(general_params['bet']), 0, 1)
    pdf.cell(90, 10, '', 0, 2, 'C')

    # Summary table
    for header in general_params['table_headers'][:-1]:
        pdf.cell(35, 10, header, 1, 0 , 'C')
    pdf.cell(35, 10, general_params['table_headers'][-1], 1, 2, 'C')
    pdf.cell(-140)
    pdf.set_font('arial', '', 11)
    for key, value in strategy_summary_dict.items():
        pdf.cell(35, 10, str(value['name']), 1, 0, 'C')
        pdf.cell(35, 10, str(value['lookback']), 1, 0, 'C')
        pdf.cell(35, 10, str(value['threshold']), 1, 0, 'C')
        pdf.cell(35, 10, str(value['num_triggers']), 1, 0, 'C')
        pdf.cell(35, 10, str(value['final_btc_balance']), 1, 2, 'C')
        pdf.cell(-140)

    # ADD DETAILED PAGES
    for key, value in strategy_results_dict.items():
        pdf.add_page()
        pdf.set_font('Times', '', 12)
        pdf.cell(60)
        pdf.cell(75, 10,'Detailed Results Summary: {}'.format(key), 0, 2, 'C')    # page title
        # pdf.cell(-60)
        pdf.cell(75, 10, 'Strategy Description: ' + strategy_summary_dict[key]['description'], 0, 1, 'C')

        generate_btc_time_history_plot(value, key)
        pdf.image('output/' + key + '_btc_time_history_plot.png', x = 40, y = None, w = 0, h = 100, type = '', link = '')

        generate_cci_time_history_plot(value, key, strategy_summary_dict[key]['threshold'])
        pdf.image('output/' + key + '_cci_time_history_plot.png', x = 40, y = None, w = 0, h = 100, type = '', link = '')


    # OUTPUT REPORT
    pdf.output('output/CCI_Report_' + str(datetime.datetime.today().strftime('%Y-%m-%d')) + '.pdf', 'F')



if __name__ == '__main__':
    summary_params = {
        'time_history': '',
        'starting_capital': '',
        'bet': '',
    }

    generate_report()


# TODO:
#
