import sys
import utils.logging_util as l_util
from apps.app_config import AppConfig
from utils.dataProvider.get_data import QuandlProvider
from utils import common_util as c_util



sys.path.append('../PythonandSQL')

l_util.config()
logger=l_util.get_logger(__name__)


@c_util.time_elapsed
def main (arg_app_name):
    if arg_app_name:
        logger.info('Triggering App: {}'.format(arg_app_name))
        app_cls=AppConfig().get_app(arg_app_name)
        app_cls(**user_opts.app_params).run()

if __name__=="__main__":
    logger.info('Initializing Test Case')
    user_opts=c_util.UserOpts()
    main(user_opts.app_name)

"""
--APP_NAME=VALUE_AT_RISK
--APP_PARAMS
RUN_CFG=/Users/krzysiekbienias/Documents/GitHub/Portfolio_Theorem/run_cfg/valueAtRisk.yaml
"""

    # # quandConnector=QuandlProvider(tickers=['AAPL', 'MSFT', 'GOOG', 'WMT'],startDate='2015-01-01',
    # #                               endDate='2019-08-31',dateFormat='%Y-%m-%d')
    # # #dc_check = SQLConnector()
    # # #export_data_frame(self, data_frame: pd.DataFrame, table_name: str):
    # # #dc_check.export_data_frame(data_frame=quandConnector.mdfEquities,table_name='equity')
    # #
    # # #dc_check.close_conection()
    # print('The END')
    #
