import pandas as pd # For data manipulation and analysis
import numpy as np # For numerical computations
from lets_plot import * # For advanced and interactive plots
from statsmodels.api import OLS, add_constant # For advanced and interactive plots
from statsmodels.stats.sandwich_covariance import cov_hac, cov_white_simple  # For robust standard errors
from statsmodels.tsa.stattools import adfuller  # For Augmented Dickey-Fuller tests
import requests  # For making HTTP requests to web servers for data retrieval
from io import StringIO  # For creating in-memory text streams which behave like 
import yfinance as yf
import scipy.optimize as opt
import requests
import json
from typing import Dict, Optional

LetsPlot.setup_html()

cpiData = pd.read_csv('cpi_index_all_00-25.csv', skiprows = 12, names = ['Year', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'Half1', 'Half2'])
cpiData.set_index('Year', inplace = True)

# 2000
tickers00 = [
    "SCCO", "VALE", "GGB", "MO", "BOOM", "BPT", "DECK", "BBD", "AMED",
    "CLH", "BRFS", "MNST", "MED", "BWEN", "HUSA", "SID", "AIMD", "CIG",
]

tickers07 = ["UAVS"]

tickers08 = ["AIMD", "NIXX", "TOMZ"]

tickers10s = [
    "BLNE", "IMTX", "ALAR", "FERG", "ALBT", "XPEL", "AQB", "PAYS", "APTO", "BLBX",
    "NHTC", "CRON", "CZR", "CCRD", "EVI", "NFLX", "PARR", "DPZ", "NUTX", "NBIX",
    "TREE", "NOVT", "NXST", "ACAD", "MKTX"
]

tickers10 = ["ARMN"]

tickers13 = ["NUTX"]

tickers14 = ["PETV"]

tickers15 = [
    "BLNE", "AIMD", "GRNQ", "FNGR", "PNBK", "AVXL", "ENVB", "DLPN",
    "WKHS", "AUID", "AMBO", "THTX"
]

tickers17 = ["AQB", "FRHC", "HIVE"]

tickers18 = ["ALAR", "ALBT"]

tickers19 = [
    "AXSM", "FTLF", "SOBR", "TNK", "NCRA", "OXBRW", "KOD", "QIPT", "SBEV", "RLMD",
    "EVER", "RCEL", "DRRX", "IVDA", "CTM", "NCPL", "NISN", "BATL", "MBOT", "SAVA",
    "OESX", "CDLX", "NGNE", "ENPH", "PNTG"
]

tickers20 = ["FFIE"]

tickers21 = ["GFRX"]

tickers22 = ["APCXM"]

tickers23 = ["AZTR", "MDXH"]

tickers24 = [
    "WLDSW", "MTEKW", "NXLIW", "RGTIW", "TSSI", "SNYR", "RZLVW", "GRRRW",
    "AISPW", "SOUNW", "WGS", "DRUG", "ILLRW", "KULR", "QUBT", "LENZ", "PDYN",
    "FLDDW", "WGSWW", "ZIVO", "RVSNW", "RGTI", "RCAT", "PSIX", "MNPR"
]

# Indexes
tickersIndexes = [
    "DGNX", "AIMAW", "MGAM", "AREBW", "DATSW", "RGC", "GATEW", "HONDW",
    "YOSH", "WLDSW", "LXEH", "MNDR", "FTFT", "CRVO", "TOI", "TWNPV", "MLGO",
    "GITS", "DOMH", "TWNP", "GATE", "NMAX", "ABTS", "SKBL", "GSPC", "MSCI", "AAPL", "DJI"
]

def stockPrice(stockName, T0, T1):
    # For old stocks
    data = yf.download(stockName, start=T0, end=T1)

    if data.empty:
        return None, None
    
    startPrice = round(stockName["Adj Close"].iloc[0], 2)
    endPrice = round(stockName["Adj Close"].iloc[-1], 2)

    return startPrice, endPrice

def stockIndustry(stockName):
    industry = yf.Ticker(stockName).info.get("industry", None)

    return industry

def stockSector(stockName):
    sector = yf.Ticker(stockName).info.get("sector", None)

    return sector

def systematicRisk(stockName):
    beta = yf.Ticker(stockName).info.get("beta", None)
    
    return beta

def inflationRisk(stockName, T0, T1):
    # The inflation rate at time 0 must be greater than the investment return
    # at time 1 for positive real returns
    startPrice = stockPrice(stockName, T0, T1)
    endPrice = stockPrice(stockName, T0, T1)
    
    # Calculate rate of return
    nominalStockReturn = (endPrice - startPrice)/startPrice

    # Formatting time variables
    yearStart, monthStart = T0
    yearEnd, monthEnd = T1

    # Consumer Price Index (CPI) data set to measure US stock inflationary risk
    endCPI = cpiData.loc[yearStart, monthStart]
    beginningCPI = cpiData.loc[yearEnd, monthEnd]

    inflationRate = (endCPI - beginningCPI) / beginningCPI

    # Calculate real returns
    realReturns = nominalStockReturn - inflationRate
        
    # Definition returns an index of whether or not the inflation risk is good
    # Add a function that will compare stocks real returns to one another.
    if realReturns > 0:
        return 1
    else:
        return 0

def liquidityRisk(stockName):
    try:
        info = yf.Ticker(stockName).info
        avg_volume = info.get("averageVolume", 0)
        market_cap = info.get("marketCap", 0)

        if avg_volume < 100000 and market_cap < 500_000_000:
            return 0
        else:
            return 1
        
    except Exception:
        return 0

def getTickerGroup(T0, T1):
    year = int(T1.split("-")[0])  # Extract year from date string

    tickerList = []

    # Always include index tickers after 2010
    if year <= 2010:
        tickerList.extend(tickers00 + tickersIndexes)
    elif 2010 <= year < 2020:
        tickerList.extend(tickers10s + tickersIndexes)
    elif year > 2020:
        tickerList.extend(tickersIndexes)


    # Add specific year-based tickers
    year_specific = {
        2007: tickers07,
        2008: tickers08,
        2010: tickers10,
        2013: tickers13,
        2014: tickers14,
        2015: tickers15,
        2017: tickers17,
        2018: tickers18,
        2019: tickers19,
        2020: tickers20,
        2021: tickers21,
        2022: tickers22,
        2023: tickers23,
        2024: tickers24
    }

    if year in year_specific:
        tickerList.extend(year_specific[year])

    return list(set(tickerList))

def choosingStocks(tickerList, T0, T1, avoid_sectors=[]):
    stockList = []

    for ticker in tickerList:
        flag = 0

        # Liquidity filter
        if liquidityRisk(ticker) == 1:
            continue
        else:
            flag += 1

        # Inflation-adjusted return filter
        if inflationRisk(ticker, T0, T1) == 1:
            continue
        else:
            flag += 1

        # Sector exclusion filter
        sector = stockSector(ticker)
        if sector not in avoid_sectors or flag < 2:

            # Price availability check
            startPrice = stockPrice(ticker, T0, T1)
            if startPrice is None:
                break
            else: 
                # Passed all checks
                stockList.append(ticker)

    return stockList

def calculate_risk_tolerance_score(age, salary, budget):
    """
    Calculate the Risk Tolerance Score (RTS) for an investor.
    
    Args:
        age (int): Investor's age
        salary (float): Annual salary
        budget (float): Investment budget
    
    Returns:
        float: Risk Tolerance Score between 0 (conservative) and 1 (aggressive)
    """
    # Calculate components
    age_factor = 1 - (age / 100)
    salary_factor = min(salary / 200000, 1)
    budget_factor = min(budget / 50000, 1)
    
    # Calculate RTS with weighted components
    rts = (0.4 * age_factor) + (0.3 * salary_factor) + (0.3 * budget_factor)
    
    return rts

def interpret_risk_score(rts):
    """
    Interpret the Risk Tolerance Score into a risk category.
    
    Args:
        rts (float): Risk Tolerance Score
    
    Returns:
        str: Risk category description
    """
    if rts < 0.3:
        return "Conservative (e.g., dividend stocks, low-volatility sectors)"
    elif 0.3 <= rts < 0.6:
        return "Moderate (e.g., blended growth/value stocks)"
    else:
        return "Aggressive (e.g., tech/growth stocks, higher beta)"



