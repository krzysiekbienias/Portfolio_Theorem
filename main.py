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



sys.path.append('../PythonandSQL')
from kb_sql_class import SQLConnector

from get_data import QuandlProvider

if __name__ == "__main__":
    quandConnector=QuandlProvider(tickers=['AAPL', 'MSFT', 'GOOG', 'WMT'],startDate='2015-01-01',
                                  endDate='2019-08-31',dateFormat='%Y-%m-%d')
    dc_check = SQLConnector()
    #export_data_frame(self, data_frame: pd.DataFrame, table_name: str):
    dc_check.export_data_frame(data_frame=quandConnector.mdfEquities,table_name='equity')

    dc_check.close_conection()
    print('The END')

