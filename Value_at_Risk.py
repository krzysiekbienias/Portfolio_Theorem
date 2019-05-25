import mysql.connector
import numpy as np
import pandas as pd
import pymysql
import sqlalchemy
from os import listdir
import os
from typing import List

from kb_sql_class import SQLConnector


fb_connector = SQLConnector(as_index='Date',
                            query='''
                                    SELECT  Date,`Company Name`,`Adj Close`

                                    from all_stock
                                    where `Company Name`='fb' ''')

aapl_connector = SQLConnector(as_index='Date',
                            query='''
                                    SELECT  Date,`Company Name`,`Adj Close`

                                    from all_stock
                                    where `Company Name`='aapl' ''')

goog_connector = SQLConnector(as_index='Date',
                            query='''
                                    SELECT  Date,`Company Name`,`Adj Close`

                                    from all_stock
                                    where `Company Name`='goog' ''')

df_fb_close=fb_connector.execute_query()
fb_connector.close_conection()

class CalculateRates():
    all_price=pd.concat(fb_connector.mdf_from_query,aapl_connector.mdf_from_query)




print('THE END')

