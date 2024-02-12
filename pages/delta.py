from dash import Dash, dcc, html, Input, Output, register_page, callback
from config import app_config
from helpers import delta_box_plot_figure, delta_map_figure

#register page
register_page(__name__,name='Price Change', path='/delta')

# define app layout
layout = html.Div([
    dcc.Dropdown(
        id='region-dropdown',
        options=[{'label': region, 'value': region} for region in app_config['regions']],
        value="South East"
    ),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': year, 'value': year} for year in app_config['years']],
        value="2022"
    ),
    html.Div([
        dcc.Graph(id='plot3'),
        dcc.Graph(id='plot4'),
    ])
])

# define callbacks
@callback(
    [Output('plot3', 'figure'),
     Output('plot4', 'figure')],
     [Input('region-dropdown', 'value'),
      Input('year-dropdown', 'value')]
)

def update_plots(selected_region,selected_year):
    fig1 = delta_box_plot_figure(selected_region, selected_year)
    fig2 = delta_map_figure(selected_region, selected_year)
    return fig1, fig2