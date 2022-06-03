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


def sharpe_ratio(df: DataFrame, strategy_returns_header: string, trading_periods: int) -> DataFrame:
    """ Sharpe ratio evaluates the return of an investment compared to its
    risk. This function computes the Sharpe ratio of a portfolio implementing a 
    given trading strategy and one that just buys and holds Bitcoin over the
    same period of time. The trading strategy results are indicated by the 
    "strategy_returns_header" string in the input data frame. """

    # Calculate percent change between each record
    # last input price / first input price
    # btc only
    # trading strategy

    # Calculate annualized return (CAGR)

    # Assume a risk free return rate
    risk_free_rate = 2    # percent

    # Calculate annualized volatility

    # Calculate sharpe ratio


# TODO:
# SHARPE RATIO
# SORTINO RATIO
# DUMMY PORTFOLIO P&L
# WIN PERCENTAGE
# MAX WIN
# MAX LOSS
# AVERAGE WIN / LOSS
# Plots...?

