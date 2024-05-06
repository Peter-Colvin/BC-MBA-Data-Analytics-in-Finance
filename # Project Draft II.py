# Project Draft II
import datetime as dt
import pandas as pd
import numpy as np
import math as ma
import yfinance as yf

# Read excel file, make da ticker list
ticker_list = pd.read_csv('projectb.csv',sheet_name='Ticker', index_col=0)

# Initial Hard-coded factors
initial_dollars = 10000
start_date = '2020-12-31'
altz_investments = {}
m2b_investments = {}
altz_portfolio_shares= {}
m2v_portfolio_shares= {}

annual_return_altz = []
annual_return_m2b = []
# Calculate Modified Altman Z-score
def mod_alt_z(ticker, start_date):
    end_date = start_date.replace(start_date=start_date.year + 1)

    #calculations for the A factor
    current_assets = yf.download(ticker,start_date, end_date)['Adj Close']
    current_liabilities = yf.download(ticker,start_date, end_date).balance_sheet.loc['Total Current Liabilities']
    total_assets = yf.download(ticker,start_date, end_date).balance_sheet.loc['Total Assets']
    A_var = (current_assets - current_liabilities)/total_assets
    
    # calculations for the B factor
    retained_earnings = yf.download(ticker,start_date, end_date).balance_sheet.loc['Retained Earnings']
    B_var = retained_earnings / total_assets

    # calculate the c factor
    EBIT = yf.download(ticker,start_date, end_date).financials.loc['EBIT']
    C_var = EBIT / total_assets

    # calculated D factor
    book_equity = yf.download(ticker,start_date, end_date).balance_sheet.loc['Total Equity']
    total_liabilities = yf.download(ticker,start_date, end_date).balance_sheet.loc['Total Liabilities']
    D_var = book_equity / total_liabilities

    z_score = 3.25 + 3.25 + 6.56*A_var + 3.26*B_var + 6.72*C_var + 1.05*D_var

    return z_score

# Calculate M2B ratio
def m2b_ratio(ticker, start_date):
    end_date = start_date.replace(start_date=start_date.year + 1)
    data = yf.download(ticker,start_date, end_date).company.info
    book_value = data['bookValue']
    market_price = data['previousClose'] 
    P2B_ratio = market_price / book_value
    return P2B_ratio

# calculate the average of values in a dictionary
def dict_avg(dict_var):
    total = sum(dict_var.values())
    average = total / len(dict_var)
    return average

# count values greater than average
def count_greater(dict_var):
    avg = dict_avg(dict_var)
    count = sum(1 for value in dict_var.values() if value > avg)
    return count

# count values less than average
def count_less(dict_var):
    avg = dict_avg(dict_var)
    count = sum(1 for value in dict_var.values() if value < avg)
    return count

# make initial list of values
for i in ticker_list:
    altz_investments[i] = mod_alt_z(i, start_date)
    m2b_investments[i] = m2b_ratio(i, start_date)
# set initial values

date = start_date
altz_port_value = initial_dollars
m2b_port_value = initial_dollars
for j in range(3):
# do Z-score and m2b calcsset amount invested per chosen stock
    for i in ticker_list:
        altz_investments[i] = mod_alt_z(i, date)
        m2b_investments[i] = m2b_ratio(i, date)
    invest_ea_altz = altz_port_value/count_greater(altz_investments)
    invest_ea_m2b = m2b_port_value/count_less(m2b_investments)
# set number of shares invested in each stock
    for i in ticker_list:
        if  altz_investments[i] > dict_avg(altz_investments):
            altz_portfolio_shares[i] = invest_ea_altz / yf.download(i, date)['Adj Close']
        else:
            altz_portfolio_shares[i] = 0
        if  m2b_investments[i] < dict_avg(m2b_investments):
            m2v_portfolio_shares[i] = invest_ea_m2b/yf.download(i, date)['Adj Close']
        else:
            m2v_portfolio_shares[i] = 0
# update the date for the next iteration
    date = date.replace(year=date.year + 1)
# calcaculate the portfolios' values and annual return
    altz_port_value_new = 0
    m2b_port_value_new = 0
    for i in ticker_list: 
        altz_port_value_new += altz_portfolio_shares[i] * yf.download(i, date)['Adj Close']
        m2b_port_value_new +=  m2v_portfolio_shares[i] * yf.download(i, date)['Adj Close']
    annual_return_altz[j] = (altz_port_value_new - altz_port_value)/altz_port_value
    annual_return_m2b[j] = (m2b_port_value_new - m2b_port_value)/m2b_port_value
# set portfolio value to new value
    altz_port_value = altz_port_value_new
    m2b_port_value = m2b_port_value_new




total_return_altz = (((1 + annual_return_altz[0])*(annual_return_altz[1])*(annual_return_altz[2]))**(1/3)) -1

total_return_m2b = (((1 + annual_return_m2b[0])*(annual_return_m2b[1])*(annual_return_m2b[2]))**(1/3)) -1
# reports investment returns of both portfolios
print("Total Alt-Z Porfolio return = " + total_return_altz + "  Total m2b Portfolio Retunr =" + total_return_m2b)