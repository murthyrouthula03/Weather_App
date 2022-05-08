#from dash import dcc
#import dash
import dash_core_components as dcc
#from dash import html
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

# must add this line in order for the app to be deployed successfully on Heroku
#from app import server
from app import app
# import all pages in the app
from apps import world,Europe,Asia,home,Americas,Africa

#app=dash.Dash()
#server=app.server

# building the navigation bar
# https://github.com/facultyai/dash-bootstrap-components/blob/master/examples/advanced-component-usage/Navbars.py
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Home", href="/home"),
        dbc.DropdownMenuItem("Global", href="/world"),
        dbc.DropdownMenuItem("Asia&Oceania", href="/Asia"),
        dbc.DropdownMenuItem("Europe", href="/Europe"),
        dbc.DropdownMenuItem("Africa", href="/Africa"),
        dbc.DropdownMenuItem("Americas", href="/Americas"),
    ],
    nav = True,
    in_navbar = True,
    color="lightblue",
    label = "Weather Info",
    style={"color":"black","font-weight": "bold"}
    
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="/assets/weather_logo1.png", height="70px")),
                        dbc.Col(dbc.NavbarBrand("World Weather Dashboard", className="mt-3"))
                    ],
                    align="center"
                ),
                href="/home",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    # right align dropdown menu with ml-auto className
                    [dropdown], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    ),
    color="skyblue",
    dark=False,
    className="mt-3",
)

def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

# embedding the navigation bar
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/world':
        return world.layout
    elif pathname == '/Europe':
        return Europe.layout
    elif pathname == '/Asia':
        return Asia.layout
    elif pathname == '/Africa':
        return Africa.layout
    elif pathname == '/Americas':
        return Americas.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(port = 8079, debug=True)