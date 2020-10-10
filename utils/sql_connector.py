import mysql.connector
import numpy as np
import pandas as pd
import pymysql
import sqlalchemy
from os import listdir
import os
from typing import List
from six import string_types

from utils.common_util import load_cfg
import utils.os_util as o_util
import utils.logging_util as l_util

curr_file_path=os.path.abspath(os.path.dirname(__file__))
logger=l_util.get_logger(__name__)

class SQLConnector:
    def __init__(self):
        cfg_file = os.path.join(curr_file_path+'/config/', 'db_cfg.yaml')
        self.cfg_object = load_cfg('yaml', cfg_file)
        self.connDetails=self.get_conn_str()

        self.my_sql_conn = self.set_connection_details()
        #self.m_db_cursor = self.m_connection_details.cursor()
        # self.mdf_from_query = self.execute_query()
        #self.engine = sqlalchemy.create_engine('mysql+pymysql://root:Numeraire2019@127.0.0.1:3306/sql_store')
        #self.df = self.testQuery(date='2014-05-19')

    def get_conn_str(self):
        ret_dict = {}
        ret_dict['HOST']=self.cfg_object['HOST']
        ret_dict['DATABASE']=self.cfg_object['DATABASE']

        credentials_file=self.cfg_object['CREDENTIALS']
        if os.path.exists(credentials_file):
            with open(credentials_file,'r') as f:
                cred_info=f.read().split('::')
                if len(cred_info)>1:
                    ret_dict['USER_ID']=cred_info[0]
                    ret_dict['PASSWORD']=cred_info[1]
                else:
                    raise Exception('Credentials not in the expected.'\
                                    'Please have it as user_id::password in the credentils file')
        else:
            raise Exception('Credentils file not found. Please configure in the yaml cfg file')


        return ret_dict



    def set_connection_details(self):
        return mysql.connector.connect(host=self.connDetails['HOST'],
                                       user=self.connDetails['USER_ID'],
                                       passwd=self.connDetails['PASSWORD'],
                                       database=self.connDetails['DATABASE'])



    # def quote_sql_string(self, value):
    #     '''
    #     If `value` is a string type, escapes single quotes in the string
    #     and returns the string enclosed in single quotes.
    #     '''
    #     if isinstance(value, string_types):
    #         new_value = str(value)
    #         new_value = new_value.replace("'", "''")
    #         return "'{}'".format(new_value)
    #     return value
    #
    # def testQuery(self, date=None):  # example of dynamic query with fstrings
    #     query = f'''SELECT * FROM sql_store.usd3mlibor
    #             where observation_date='{date}' '''
    #     df = pd.read_sql(query, con=self.m_connection_details)
    #     return df
    #
    # def export_data_frame(self, data_frame: pd.DataFrame, table_name: str):
    #     return data_frame.to_sql(name=table_name, con=self.engine, index=True, if_exists='append')
    #
    # def close_conection(self):
    #     self.m_connection_details.close()
    #
