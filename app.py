from dash import Dash, dcc, html, page_registry, page_container
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SLATE, '/assets/custom.css'])

# define navigation bar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink('Average Price', href='/')),
        dbc.NavItem(dbc.NavLink('Price Change', href='/delta')),
        dbc.NavItem(dbc.NavLink('Growth', href='/growth')),
    ],
    brand="Property Dashboard",
    brand_href='/',
    color='dark',
    dark=True
)

#define footer
footer = dbc.Container(
    dbc.Row(
        [
            dbc.Col(html.A("Harry Allum | GitHub", href='/'), align='left'),
        ],
    ),
    className='footer',
    fluid=True,
)

# define layout
app.layout = html.Div([
    navbar,
    page_container,
    footer,
])

if __name__ == '__main__':
    app.run_server(debug=True)

