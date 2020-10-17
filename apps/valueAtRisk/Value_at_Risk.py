import numpy as np
import pandas as pd

from utils.sql_connector import SQLConnector
from utils.dataProvider.get_data import QuandlProvider

from apps.base_app import BaseApp
from utils.ExcelUtils.excelUtils import ExcelFilesDetails,CreateDataFrame,OutputInExcel
from apps.PortfolioUtilities.portfolioFunctions import portfolioValue
from utils.common_util import str_to_numb


import utils.logging_util as l_util
from utils.PlotKit.plotCreator import PlotFinanceGraphs


logger=l_util.get_logger(__name__)

sqlConn=SQLConnector()

class DataBaseExtractor():
    def __init__(self, compounding,weigths):
        self._compunding = compounding
        self._weights=weigths

        self.mdfshareQuotations = self.getShareQuatations()
        self.close_price = self.processing_data_frame()
        self.m_arr_rates = self.calculate_rate()
        # self.m_todays_portfolio_value=self.todays_portfolio()

    def getShareQuatations(self):
        query='''select * 
                from all_stock; '''
        df = pd.read_sql(query, con=sqlConn.my_sql_conn)
        logger.info('Extract Quatations from Data Base')
        return df

    def processing_data_frame(self):
        subdf=self.mdfshareQuotations[['Date','Adj Close','Company Name']]
        return subdf.pivot(index='Date',columns='Company Name',values='Adj Close')
    #
    def calculate_rate(self):
        if self._compunding not in ['continious','simple']:
            raise Exception("Rates type not defined properly")
            logger.info('Please provide corrct rates type')
        else:
            logger.info(f'You have defined {self._compunding} rates' )
            arr = np.array(self.close_price)
            return_all = np.zeros((np.shape(arr)[0], np.shape(arr)[1]))
            if self._compunding == 'continious':

                for i in range(1, len(arr)):
                    return_all[i] = np.log(arr[i] / arr[i - 1])
            if self._compunding == 'simple':

                for i in range(1, len(arr)):
                    return_all[i] = (arr[i] - arr[i - 1]) / arr[i - 1]

            return return_all[1:]



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
        self._excel_location=''
        self._excel_name=''
        super().__init__(app_name, app_params)

    def run(self):
        num_weights=str_to_numb(self._weights)
        results_monitoring_obj=OutputInExcel(FileName=self._excel_name,Path=self._excel_location)
        data_obj=DataBaseExtractor(compounding=self._compound,weigths=self._weights)
        df_rates=pd.DataFrame(data_obj.m_arr_rates)
        portfolioValue(num_weights, positions=data_obj.close_price[-1:].values.tolist()[0])

        logger.info(f'Current value of Portfolio: {portfolioValue(num_weights,positions=data_obj.close_price[-1:].values.tolist()[0])}')

        results_monitoring_obj.insertWholeDataFrame(filename=self._excel_name,fileLocation=self._excel_location,
                                                    sheet_name='close price',
                                                    df=data_obj.close_price,startcol=0,startrow=0,
                                                    include_index=True,include_header=True)

        results_monitoring_obj.insertWholeDataFrame(filename=self._excel_name, fileLocation=self._excel_location,
                                                    sheet_name='rates',
                                                    df=df_rates, startcol=0, startrow=0,
                                                    include_index=True, include_header=True)






print('THE END')
