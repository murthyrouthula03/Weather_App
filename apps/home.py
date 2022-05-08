import dash
#from dash import html
import dash_html_components as html
import dash_bootstrap_components as dbc

# needed only if running this as a single page app
#external_stylesheets = [dbc.themes.LUX]
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

from app import app

app=dash.Dash()
server=app.server

# change to app.layout if running as single page app instead
layout = html.Div([
    dbc.Container([
        dbc.Row([
            #Header span the whole row
            #className: Often used with CSS to style elements with common properties.
            dbc.Col(html.H1("World Wide Weather Information Dashboard", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col(html.P(children='This Dashboard was mainly developed using open-source technologies like Python Dash, Plotly and Bootstrap.',
                            className="text-center",style={"font-style": "italic","color":"black","font-weight": "bold"})
                    , className="mb-4")
            ]),

        dbc.Row([
            dbc.Col(html.P(children='Pages of this Dashboard are mainly divided into Global and continent wise weather information. '
                            'This Dashboard contains the weather information of different countries from 28/03/2022 to 01/04/2022. '
                            'You can download the data and check the code developed from below links. '
                            'Please make sure to cite when using this dataset or code. You can download the graphs and hover through '
                            'them. Weather Info includes Temperature, Wind Speed, Wind Degree, UV Index, Humidity, Precipitation, '
                            'Feels Like Temperature. This Project is only intended for study purpose and data scraped by signing up for API.', 
                            className="text-justify", style={"color":"black"}
                            ))
                    
        ]),

        dbc.Row([
            # 2 columns of width 6 with a border
            dbc.Col(dbc.Card(children=[html.H3(children='Click below to download world weather data',
                                               className="text-center"),
                                       dbc.Button("Weather Data",
                                                  href="https://www.gapminder.org/data/",
                                                  color="primary",
                                                  className="mt-3 btn btn-info"),
                                       ],
                             body=True, color="dark", outline=True)
                    , width=6, className="mb-4"),

            dbc.Col(dbc.Card(children=[html.H3(children='Click below for the code of this dashboard',
                                               className="text-center"),
                                       dbc.Button("GitHub",
                                                  href="https://github.com/JackLinusMcDonnell/DashAppTeaching",
                                                  color="primary",
                                                  className="mt-3 btn btn-info"),
                                       ],
                             body=True, color="dark", outline=True)
                    , width=6, className="mb-4"),

        ], className="mb-5"),
        dbc.Row([
            dbc.Col(html.Img(src=app.get_asset_url('weather_conditions.jpg')), 
            width={"size": 6, "offset": 4})
        ],align="center"),
        html.A(children="Check here to check into the weatherstack website to scrap the data by signing up for API Access. Only 250 requests allowed for free.", 
               href="https://weatherstack.com/login?u=https%3A%2F%2Fweatherstack.com%2Fquickstart", 
               style={"color":"black","text-align":"center"}),
        html.P("Developer Info - Murthy Routhula (d00243413@student.dkit.ie), Dundalk Institute of Technology, Ireland", 
                style={"background-color":"DodgerBlue","text-align":"center","color":"black"})
    

    ])

])

# needed only if running this as a single page app
#if __name__ == '__main__':
#    app.run_server(port=8098,debug=True)