import quandl

import mysql.connector
import numpy as np
import pandas as pd
import pymysql
import sqlalchemy
from os import listdir
import os
from typing import List
import quandl
import sys

quandl.ApiConfig.api_key = 'Xe4jzKF63kor6sD767uV'

# https://www.quandl.com/api/v3/databases/WIKI/metadata?api_key=<Xe4jzKF63kor6sD767uV>

sys.path.append('../PythonandSQL')
from kb_sql_class import SQLConnector


class QuandlProvider:
    def __init__(self, tickers, startDate, endDate,dateFormat,index=None):
        self._lsTickers = tickers
        self._sStartDate = startDate
        self._sEndDate = endDate
        self._sindex=index
        self._dateFormat=dateFormat
        self.mdfEquities = self.getDataFrame()
        #self.mdfSplitbyTickers = self.getByTickers()

    # good for insert do tb
    def getDataFrame(self):
        df = quandl.get_table('WIKI/PRICES', paginate=True,
                              ticker=self._lsTickers,
                              date={'gte': self._sStartDate, 'lte': self._sEndDate},
                              qopts={'columns': ['ticker', 'date', 'adj_close']})
        if(self._sindex!=None):
            dfUpdated = df.set_index('date')
        else:
            dfUpdated=df
            dfUpdated['date']=pd.to_datetime(dfUpdated.date)
            dfUpdated['date']=dfUpdated['date'].dt.strftime(self._dateFormat)
        return dfUpdated

    # use pandas pivot function to sort adj_close by tickers

    def getByTickers(self):
        splite = self.mdfEquities.pivot(columns='ticker')
        splite.index = pd.to_datetime(splite.index, format='%m/%d/%Y')
        splite.index = splite.index.strftime('%Y-%m-%d')

        return splite



if __name__ == "__main__":
    pass

    print('the end')
