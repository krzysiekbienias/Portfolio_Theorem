import mysql.connector
import numpy as np
import pandas as pd
import pymysql
import sqlalchemy
from os import listdir
import os
from typing import List


from get_data import QuandlProvider

class RatesFromQuantLib(QuandlProvider):
    def __init__(self,tickers,startDate,endDate,dateFormat,ratesType):
        QuandlProvider.__init__(self,tickers,startDate,endDate,dateFormat)

        self._ratesType=ratesType

        self.df_fromQuantLib=self.getDataFrame()
        self.df_companiesClosePrice=self.convert_data_frame()
        self.a_logRates=self.calculateReturnRates()

    def convert_data_frame(self):
        return self.df_fromQuantLib.pivot(columns='ticker',index='date',values='adj_close')

    def calculateReturnRates(self):
        arr = np.array(self.df_companiesClosePrice)
        return_all = np.zeros((np.shape(arr)[0], np.shape(arr)[1]))
        if self._ratesType == 'continious':

            for i in range(1, len(arr)):
                return_all[i] = np.log(arr[i] / arr[i - 1])
        if self._ratesType == 'simple':

            for i in range(1, len(arr)):
                return_all[i] = (arr[i] - arr[i - 1]) / arr[i - 1]

        return return_all[1:]
    #
    # def todays_portfolio(self):
    #     return self.adjusted_query[:-1]


if __name__ == "__main__":
    rates = RatesFromQuantLib(tickers=['AAPL', 'MSFT', 'GOOG', 'WMT'],startDate='2018-01-01',
                                  endDate='2019-08-31',dateFormat='%Y-%m-%d',ratesType='continious')


print('THE END')