from dash import Dash, dcc, html, Input, Output, register_page, callback
import dash_bootstrap_components as dbc
from config import app_config
from helpers import avg_price_map_fig, avg_price_bar_fig

# regiter page
register_page(__name__,name="Average Price", path='/')

# define app layout
layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Div('Select region:', className="dropdown-label"),
                    width=1,
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='region-dropdown',
                        options = [
                            {'label': region, 'value': region} for region in app_config['regions']
                        ],
                        value = 'South East' # default dropdown value
                    ),
                    width=2
                ),
                dbc.Col(
                    html.Div('Select year:', className='dropdown-label'),
                    width=1,
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='year-dropdown',
                        options =[{'label': year, 'value': year} for year in app_config['years']],
                        value = '2022', # default year selection
                    ),
                    width = 2,
                ),
            ],
            className='dropdown-row'
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id='plot1',
                        style={'height': '60vh'},
                    ),
                    width=6
                ),
                dbc.Col(
                    dcc.Graph(
                        id='plot2',
                        style={'height': '60vh'}
                    ),
                    width=6
                ),
            ],
            className='mb-4'
        ),
    ],
    fluid=True
)

# define callbacks
@callback(
    [Output('plot1', 'figure'),
     Output('plot2', 'figure')],
     [Input('region-dropdown', 'value'),
      Input('year-dropdown', 'value')]
)

def update_plots(selected_region,selected_year):
    fig1 = avg_price_map_fig(selected_region, selected_year)
    fig2 = avg_price_bar_fig(selected_region, selected_year)
    return fig1, fig2