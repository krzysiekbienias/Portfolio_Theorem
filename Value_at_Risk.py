import mysql.connector
import numpy as np
import pandas as pd
import pymysql
import sqlalchemy
from os import listdir
import os
from typing import List

from kb_sql_class import SQLConnector

all_price_connector = SQLConnector(as_index='Date',
                                   query='''SELECT  Date,`Company Name`,`Adj Close`
                                       from all_stock ''')


class Rates():
    def __init__(self, compounding,weigths):
        self._compunding = compounding
        self._weights=weigths

        self.mdf_from_query = all_price_connector.mdf_from_query
        self.adjusted_query = self.convert_data_frame()
        self.m_arr_rates = self.calculate_rate()
        self.m_todays_portfolio_value=self.todays_portfolio()

    def convert_data_frame(self):
        return self.mdf_from_query.pivot(columns='Company Name')

    def calculate_rate(self):
        arr = np.array(self.adjusted_query)
        return_all = np.zeros((np.shape(arr)[0], np.shape(arr)[1]))
        if self._compunding == 'continious':

            for i in range(1, len(arr)):
                return_all[i] = np.log(arr[i] / arr[i - 1])
        if self._compunding == 'simple':

            for i in range(1, len(arr)):
                return_all[i] = (arr[i] - arr[i - 1]) / arr[i - 1]

        return return_all[1:]

    def todays_portfolio(self):
        return self.adjusted_query[:-1]



if __name__ == "__main__":
    rates = Rates(compounding='continious',
                  weigths=[0.3,0.5,0.2])
    all_price_connector.close_conection()

print('THE END')
