import numpy
import math
import json
import pandas as pd


cpiData = pd.read_csv('cpi_index_all_00-25.csv', index_col='Year')


END_VALUE = 10
BEGINNING_VALUE = 100

statement1 = "Grant Lopez is 47 years old and has a budget of $2716 per year. He started investing on June 16th, 2023 and ended on October 22nd, 2023. His hobbies are painting and he avoids Crypto Assets."

T0_month = 'Jun'
T0_year = 2023
T1_month = 'Oct'
T1_year = 2023


def inflationRisk(END_VALUE, BEGINNING_VALUE, T0_month, T0_year, T1_month, T1_year):
    # The inflation rate at time 0 must be greater than the investment return
    # at time 1 for positive real returns
    
    # Calculate rate of return
    nominalStockReturn = (END_VALUE - BEGINNING_VALUE)/BEGINNING_VALUE
    
    # Consumer Price Index (CPI) data set to measure US stock inflationary risk
    endCPI = cpiData.loc[T1_year,T1_month]
    beginningCPI =cpiData.loc[T0_year,T0_month]

##
    inflationRate = (endCPI - beginningCPI) / beginningCPI
    
    # Calculate real returns
    realReturns = nominalStockReturn - inflationRate
        
    # Definition returns an index of whether or not the inflation risk is good
    # Add a function that will compare stocks real returns to one another.
    if realReturns > 0:
        return 1
    else:
        return 0

print(inflationRisk(500,499, T0_month, T0_year, T1_month, T1_year))