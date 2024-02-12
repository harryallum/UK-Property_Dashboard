from dash import Dash, dcc, html, Input, Output, register_page, callback
import dash_bootstrap_components as dbc
from config import app_config
from helpers import fastest_growing_map_figure,fastest_declining_map_figure

# regiter page
register_page(__name__,name="Growth", path='/growth')

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
                    html.H5('Filter by top:', className='slider-h5'),
                    width=1,
                    style={'display': 'flex', 'align-items': 'center', 'height': '50px'}
                ),
                dbc.Col(
                    dcc.Slider(
                        id='slider',
                        min=0,
                        max=100,
                        step=10,
                        value=50, # default value
                        tooltip={'placement': 'bottom', 'always_visible': True},
                    ),
                    width=4,
                    style={'height': '50px'}
                ),
            ],
            className='mb-4 top-x-slider',
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id='plot5',
                        style={'height': '60vh'},
                    ),
                    width=6
                ),
                dbc.Col(
                    dcc.Graph(
                        id='plot6',
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
    [Output('plot5', 'figure'),
     Output('plot6', 'figure')],
     [Input('region-dropdown', 'value'),
      Input('year-dropdown', 'value'),
      Input('slider', 'value')]
)

def update_plots(selected_region,selected_year, slider_value):
    fig1 = fastest_growing_map_figure(selected_region, selected_year, slider_value)
    fig2 = fastest_declining_map_figure(selected_region, selected_year, slider_value)
    return fig1, fig2