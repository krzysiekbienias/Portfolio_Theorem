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

df_fb_close=fb_connector.execute_query()
fb_connector.close_conection()

print('THE END')

