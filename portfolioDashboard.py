import dash
import dash_core_components as dcc
import dash_table as dt
import dash_html_components as html
import QuantLib as ql
import datetime

from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate

from get_data import QuandlProvider


external_stylesheets = ['https://codepen.io/chridyp/pen/bWLgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([dcc.Textarea(value='Data Provider',
                                    style={'width': '100%', 'color': 'green', 'fontSize': 18,
                                           'background-color': 'yellow', 'border-style': 'dashed',
                                           'text-align': 'center'}),
                                    html.Label('Place provide the begining of period'),
                                    html.Br(),
                                    dcc.DatePickerSingle(id='beginOfPeriod', date=datetime.datetime(2015, 1, 25),
                                            display_format='YYYY-MM-DD'),
                                    html.Br(),
                                    html.Label('Place provide the end of period'),
                                    html.Br(),
                                    dcc.DatePickerSingle(id='endOfPeriod', date=datetime.datetime(2019, 8, 31),
                                            display_format='YYYY-MM-DD'),
                                    html.Br(),
                                    html.Label('Place provide the company for your portfoliio'),
                                    dcc.Checklist(id='tickers',
                                                  options=[
                                                      {'label':'Apple','value':'AAPL'},
                                                      {'label':'MIcrosoft','value':'MSFT'},
                                                      {'label':'Google','value':'GOOG'},
                                                           ],
                                                  value=['APPL','MSFT']
                                                  ),
                                    html.Div(id='portfolioInfo',children='')


                       ])

@app.callback(
    Output('portfolioInfo','children'),

    [
        Input('beginOfPeriod','date'),
        Input('endOfPeriod','date'),
        Input('tickers','value')
    ]
)

def getPortfolioInfo(bDate,eDate,tickers):
    chosenStocks=QuandlProvider(tickers=tickers,startDate=bDate,endDate=eDate,dateFormat='%Y-%m-%d')
    closePrice=chosenStocks.mdfEquities
    return html.Div([dcc.Textarea(value=f'Number of Records from Quandl library {closePrice.shape}',
                                  style={'width': '100%', 'color': 'red', 'fontSize': 18,
                                         'background-color': 'blue', 'border-style': 'dashed',
                                         'text-align': 'center'})
                     ]
                    )

if __name__ == '__main__':
    app.run_server(debug=True)