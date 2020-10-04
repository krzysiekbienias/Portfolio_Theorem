import numpy as np

from utils.dataProvider.get_data import QuandlProvider

class RatesFromQuantLib(QuandlProvider):
    def __init__(self,tickers,startDate,endDate,dateFormat,ratesType,weights=None):
        QuandlProvider.__init__(self,tickers,startDate,endDate,dateFormat)

        self._ratesType=ratesType
        self._weights=weights

        self.df_fromQuantLib=self.getDataFrame()
        self.df_companiesClosePrice=self.convert_data_frame()
        self.a_logRates=self.calculateReturnRates()
        self.a_covOfReturns=self.covarianceOfReturn()
        ################################----Portfolio Performance-----#################################
        self.f_portfStdDev=self.portfolioStd()
        self.f_portfolioMean=self.portfolioMean()
        ################################----Portfolio Performance-----#################################
        

    def convert_data_frame(self):
        rawData=self.df_fromQuantLib.pivot(columns='ticker', index='date', values='adj_close')
        withoutNAs=rawData.dropna()
        return withoutNAs



    def calculateReturnRates(self):
        arr = np.array(self.df_companiesClosePrice)
        return_all = np.zeros((np.shape(arr)[0], np.shape(arr)[1]))
        if self._ratesType == 'continious':

            for i in range(1, len(arr)):
                return_all[i] = np.log(arr[i] / arr[i - 1])
        if self._ratesType == 'simple':

            for i in range(1, len(arr)):
                return_all[i] = (arr[i] - arr[i - 1]) / arr[i - 1]

        return return_all[1:]

    def covarianceOfReturn(self):
        return np.cov(self.a_logRates.T)


    def portfolioStd(self):
        if self._weights is None:
            return None

        if self._weights is None :
           return None # you deal with benchmark and you don't need

        else:
            omTsigmaom= np.dot(self._weights.T,np.dot(self.a_covOfReturns,self._weights.T))
            return np.sqrt(omTsigmaom)

    def portfolioMean(self):
        if self._weights is None:
            return None
        else:
            mu_i=self.a_logRates.mean(axis=0)
            mu=sum(np.dot(self._weights.T,mu_i))
            return mu




if __name__ == "__main__":
    benchmark=RatesFromQuantLib(tickers=['SPX'],startDate='2017-01-01',
                                  endDate='2019-08-31',dateFormat='%Y-%m-%d',ratesType='continious')

    portfolio = RatesFromQuantLib(tickers=['AAPL', 'MSFT', 'GOOG', 'WMT','AMZN'],startDate='2017-01-01',
                                  endDate='2019-08-31',dateFormat='%Y-%m-%d',ratesType='continious',
                              weights=np.array([0.2,0.2,0.2,0.2,0.2]))




print('THE END')