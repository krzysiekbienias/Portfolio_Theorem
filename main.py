import sys
import utils.logging_util as l_util
from apps.app_config import AppConfig
from utils.dataProvider.get_data import QuandlProvider


sys.path.append('../PythonandSQL')

l_util.config()
logger=l_util.get_logger(__name__)

if __name__ == "__main__":
    quandConnector=QuandlProvider(tickers=['AAPL', 'MSFT', 'GOOG', 'WMT'],startDate='2015-01-01',
                                  endDate='2019-08-31',dateFormat='%Y-%m-%d')
    #dc_check = SQLConnector()
    #export_data_frame(self, data_frame: pd.DataFrame, table_name: str):
    #dc_check.export_data_frame(data_frame=quandConnector.mdfEquities,table_name='equity')

    #dc_check.close_conection()
    print('The END')

