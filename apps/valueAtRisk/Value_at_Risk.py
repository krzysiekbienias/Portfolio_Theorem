import numpy as np
import pandas as pd

from utils.sql_connector import SQLConnector
from utils.dataProvider.get_data import QuandlProvider

from apps.base_app import BaseApp
from utils.ExcelUtils.excelUtils import ExcelFilesDetails,CreateDataFrame,OutputInExcel

import utils.logging_util as l_util
from utils.PlotKit.plotCreator import PlotFinanceGraphs



sqlConn=SQLConnector()

class DataBaseExtractor():
    def __init__(self, compounding,weigths):
        self._compunding = compounding
        self._weights=weigths

        self.mdfshareQuotations = self.getShareQuatations()
        # self.adjusted_query = self.convert_data_frame()
        # self.m_arr_rates = self.calculate_rate()
        # self.m_todays_portfolio_value=self.todays_portfolio()

    def getShareQuatations(self):
        query='''select * 
                from all_stock; '''
        df = pd.read_sql(query, con=sqlConn.my_sql_conn)
        return df

    # def convert_data_frame(self):
    #     return self.mdf_from_query.pivot(columns='Company Name')
    #
    # def calculate_rate(self):
    #     arr = np.array(self.adjusted_query)
    #     return_all = np.zeros((np.shape(arr)[0], np.shape(arr)[1]))
    #     if self._compunding == 'continious':
    #
    #         for i in range(1, len(arr)):
    #             return_all[i] = np.log(arr[i] / arr[i - 1])
    #     if self._compunding == 'simple':
    #
    #         for i in range(1, len(arr)):
    #             return_all[i] = (arr[i] - arr[i - 1]) / arr[i - 1]
    #
    #     return return_all[1:]
    #
    # def todays_portfolio(self):
    #     return self.adjusted_query[:-1]

# class RatesFromQuantLib(QuandlProvider):
#     def __init__(self,tickers,startDate,endDate,dateFormat,ratesType):
#         QuandlProvider.__init__(self,tickers,startDate,endDate,dateFormat)
#         self._ratesType=ratesType
#
#
#
#     def calculate_rate(self):
#         arr = np.array(self.adjusted_query)
#         return_all = np.zeros((np.shape(arr)[0], np.shape(arr)[1]))
#         if self._compunding == 'continious':
#
#             for i in range(1, len(arr)):
#                 return_all[i] = np.log(arr[i] / arr[i - 1])
#         if self._compunding == 'simple':
#
#             for i in range(1, len(arr)):
#                 return_all[i] = (arr[i] - arr[i - 1]) / arr[i - 1]
#
#         return return_all[1:]
#
#     def todays_portfolio(self):
#         return self.adjusted_query[:-1]


class VaRRun(BaseApp):
    def __init__(self, **app_params):
        app_name='value_at_risk'
        self._weights=''
        self._compound=''
        super().__init__(app_name, app_params)

    def run(self):
        rates=DataBaseExtractor(compounding=self,weigths=self._weights)
        data=rates.getShareQuatations()





print('THE END')
