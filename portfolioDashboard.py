import dash
import dash_core_components as dcc
import dash_table as dt
import dash_html_components as html
import datetime

from dash.dependencies import Output, Input

from utils.dataProvider.get_data import QuandlProvider
from dash.exceptions import PreventUpdate
from utilities import RatesFromQuantLib


external_stylesheets = ['https://codepen.io/chridyp/pen/bWLgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([dcc.Textarea(value='Data Provider',
                                    style={'width': '100%', 'color': 'green', 'fontSize': 18,
                                           'background-color': 'yellow', 'border-style': 'dashed',
                                           'text-align': 'center'}),
                                    html.Label('Place provide the begining of period'),
                                    html.Br(),
                                    dcc.DatePickerSingle(id='beginOfPeriod', date=datetime.datetime(2018, 1, 2),
                                            display_format='YYYY-MM-DD'),
                                    html.Br(),
                                    html.Label('Place provide the end of period'),
                                    html.Br(),
                                    dcc.DatePickerSingle(id='endOfPeriod', date=datetime.datetime(2018, 12, 31),
                                            display_format='YYYY-MM-DD'),
                                    html.Br(),
                                    html.Label('Place provide the company for your portfoliio'),

                                    dcc.Checklist(id='tickers',
                                                  options=[
                                                      {'label':'Apple','value':'AAPL'},
                                                      {'label':'MIcrosoft','value':'MSFT'},
                                                      {'label':'Google','value':'GOOG'},
                                                           ],
                                                  #value=['AAPL','MSFT']
                                                  ),
                                    html.Button(id='setOfCompaniesButton',children='Submit Here',style={'fontSize':24}),
                                    html.Div(id='portfolioScrapping',children=''),
                                    html.Label('Chose rates of retuns'),
                                    dcc.RadioItems(id='rateOfReturns',
                                      options=[{'label': 'Continious', 'value': 'continious'}, {'label': 'Simple', 'value': 'simple'}],
                                                   value='continious'),
                                    html.Button(id='choosePortfolioButton',children='Get Close Price',style={'fontSize':24}),
                                    html.Div(id='portfolioSetup',children=''),
                                    html.Div(id='plotPrice', children='')
                       ])


@app.callback(
    Output('portfolioScrapping','children'),

    [
        Input('beginOfPeriod','date'),
        Input('endOfPeriod','date'),
        Input('tickers','value'),
        Input('setOfCompaniesButton','n_clicks'),



    ]
)

def getPortfolioInfo(bDate,eDate,tickers,click):
    chosenStocks=QuandlProvider(tickers=tickers,startDate=bDate,endDate=eDate,dateFormat='%Y-%m-%d')
    closePrice=chosenStocks.mdfEquities

    if click is None:
        raise PreventUpdate
    else:

        return dt.DataTable(data=closePrice.to_dict('records'),
                            columns=[{'id':c,'name':c,"selectable":True} for c in closePrice.columns],
                            column_selectable='multi',
                            style_header={'backgroundColor':'rgb(30,30,30)','text-align':'center'},
                            style_cell={
                                'backgroundColor':'rgb(50,50,50)',
                                'color':'white',
                                'text-align':'center'},
                            export_format='xlsx',
                            export_headers='display')

@app.callback(
    Output('portfolioSetup','children'),

    [
        Input('beginOfPeriod','date'),
        Input('endOfPeriod','date'),
        Input('tickers','value'),

        Input('rateOfReturns', 'value'),
        Input('choosePortfolioButton', 'n_clicks')
    ]
)

def getPortfolioClosePrice(bDate,eDate,tickers,returnsType,click):
    chosenStocks=RatesFromQuantLib(tickers=tickers,startDate=bDate,
                                  endDate=eDate,dateFormat='%Y-%m-%d',ratesType=returnsType)
    closePrice=chosenStocks.df_companiesClosePrice



    if click is None:
        raise PreventUpdate
    else:

        return dt.DataTable(data=closePrice.to_dict('records'),
                            columns=[{'id':c,'name':c,"selectable":True} for c in closePrice.columns],
                            column_selectable='multi',
                            style_header={'backgroundColor':'rgb(30,30,30)','text-align':'center'},
                            style_cell={
                                'backgroundColor':'rgb(50,50,50)',
                                'color':'white',
                                'text-align':'center'},
                            export_format='xlsx',
                            export_headers='display')


@app.callback(
    Output('plotPrice','children'),

    [
        Input('beginOfPeriod','date'),
        Input('endOfPeriod','date'),
        Input('tickers','value'),
        Input('rateOfReturns', 'value')


    ]
)

def drawEquity(bDate,eDate,tickers,returnsType):
    chosenStocks=RatesFromQuantLib(tickers=tickers,startDate=bDate,
                                  endDate=eDate,dateFormat='%Y-%m-%d',ratesType=returnsType)

    closePrice=chosenStocks.df_companiesClosePrice
    numbOfColl=[]
    for i in range(closePrice.shape[1]):
        numbOfColl.append(i)

    chosenToPlot=closePrice[closePrice.columns[numbOfColl]].values
    aa=len(chosenToPlot[0])
    dates = list(closePrice.index)
    return html.Div([
            dcc.Graph(figure=dict(data=
                                  [dict(x=dates,
                                        y=chosenToPlot[:, i],
                                        name=f'Path{i}',
                                        marker=dict(color='')) for i in range(aa)],
                                  layout=dict(
                                      xaxis={'title': 'Dates'},
                                      yaxis={'title': 'Equity Price'},
                                      title='Equity Price for fixed company',
                                      showlegend=True,
                                      legend=dict(x=0,
                                                  y=1.0),
                                      margin=dict(l=40, r=0, t=40, b=30))


                                  ),
                      style={'height': 300} )])



if __name__ == '__main__':
    app.run_server(debug=True)