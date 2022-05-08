#import packages to create app
import dash
#from dash import dcc
#from dash import html
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

from gapminder import gapminder

import plotly.express as px
import pandas as pd
import numpy as np
import os,sys

app=dash.Dash()
server=app.server

pwd = os.getcwd()

#get unique continents
#cont_names = gapminder['continent'].unique()
#cols=list(gapminder.columns)
#data for the region plot
loc_data = px.data.gapminder()
#loc_cols=list(loc_data.columns)
#reading input csv
df_data = pd.read_csv(pwd+"//weather_final_data1.csv")
#print(df_data)
df2 = df_data.merge(loc_data[['continent','iso_alpha']], how='left', left_on='iso3', right_on='iso_alpha')
loc_data = df2.drop_duplicates()

loc_data = loc_data.dropna(subset=['continent'])
loc_cols=list(loc_data.columns)
cont_names = loc_data['continent'].unique()

#print(loc_data.isnull().sum())
#print(cont_names)
#print(loc_data)

#sys.exit()

# needed only if running this as part of a multipage app
from app import app
#app = dash.Dash(__name__)
#change background and color text
colors = {
    #background to rgb(233, 238, 245)
    'background': '#e9eef5',
    'text': '#1c1cbd'
}
color_discrete_map = {'Asia': '#636EFA', 'Africa': '#EF553B', 'Americas': '#00CC96',
    'Europe': '#AB63FA', 'Oceania': '#FFA15A'}


# change to app.layout if running as single page app instead
layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.H1('Global Weather Info',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    #Add multiple line text 
    html.Div('''
        Latitude vs Temperature for different Countries from 28-03-2022 to 01-04-2022 
    ''', style={
        'textAlign': 'center',
        'color': colors['text']}
    ),
    html.Div([
        html.Div([
            html.Label('Select Continent/Continents'),
            dcc.Dropdown(id='cont_dropdown',
                        options=[{'label': i, 'value': i}
                                for i in cont_names],
                        value=['Asia','Europe','Africa','Americas','Oceania'],
                        multi=True
            )
        ],style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            html.Label('Select Precipitation Range'),
                dcc.RangeSlider(id='pop_range',
                    min=0,
                    max=14.2,
                    value=[0,14.2],
                    step= 1,
                    marks={
                        0: '0',
                        5: '5',
                        10: '10',
                        14.2: '14.2'
                    },
                )
        ],style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
    ]),
    dcc.Graph(
        id='LifeExpVsGDP'
    ),
    html.Label('Select Variable to display on Graphs'),
        dcc.Dropdown(id='y_dropdown',
            options=[                    
                {'label': 'Pressure', 'value': 'pressure'},
                {'label': 'Precipitation', 'value': 'precipitation'},
                {'label': 'Temperature', 'value': 'temperature'}],
            value='pressure',
            style={'width':'50%'}
    ),
    html.Div([
        html.Div([
            dcc.Graph(
                id='LifeExp'
            )
        ],style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(
                id='LifeExpOverTime',
            )
        ],style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
    ])

])

@app.callback(
    Output(component_id='LifeExpVsGDP', component_property='figure'),
    [Input(component_id='cont_dropdown', component_property='value'),
    Input(component_id='pop_range', component_property='value')]
)
def update_graph(selected_cont,rangevalue):
    if not selected_cont:
        return dash.no_update
    data =[]
    d = loc_data[(loc_data['precipitation'] >= rangevalue[0]) & (loc_data['precipitation'] <= rangevalue[1])]
    for j in selected_cont:
            data.append(d[d['continent'] == j])
    df = pd.DataFrame(np.concatenate(data), columns=loc_cols)
    df=df.infer_objects()
    scat_fig = px.scatter(data_frame=df, x="latitude", y="temperature",
                size="uv_index", color="continent",hover_name="country",
                # different colour for each country
                color_discrete_map=color_discrete_map, 
               #add frame by year to create animation grouped by country
               animation_frame="observation_time",animation_group="country",
               #specify formating of markers and axes
               log_x = False, size_max=60, range_x=[-45,85], range_y=[-25,50],
                # change labels
                labels={'precipitation':'Precipitation','observation_time':'Day','continent':'Continent',
                        'country':'Country','latitude':'Latitude','temperature':"Temperature"})
    # Change the axis titles and add background colour using rgb syntax
    scat_fig.update_layout({'xaxis': {'title': {'text': 'Latitude'}},
                  'yaxis': {'title': {'text': 'Temperature'}}}, 
                  plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)')

    return scat_fig



@app.callback(
    [Output(component_id='LifeExp', component_property='figure'),
    Output(component_id='LifeExpOverTime', component_property='figure')],
    [Input(component_id='cont_dropdown', component_property='value'),
    Input(component_id='pop_range', component_property='value'),
    Input(component_id='y_dropdown', component_property='value')]
)
def update_map(selected_cont,rangevalue,yvar):
    if not (selected_cont or rangevalue or yvar):
        return dash.no_update
    d = loc_data[(loc_data['precipitation'] >= rangevalue[0]) & (loc_data['precipitation'] <= rangevalue[1])]
    data =[]
    for j in selected_cont:
            data.append(d[d['continent'] == j])
    df = pd.DataFrame(np.concatenate(data), columns=loc_cols)
    df=df.infer_objects()
    map_fig= px.choropleth(df,locations="iso3", color=df[yvar],
            hover_name="country",hover_data=['continent','precipitation'],animation_frame="observation_time",    
            color_continuous_scale='Turbo',range_color=[df[yvar].min(), df[yvar].max()],
            labels={'precipitation':'Precipitation','observation_time':'Day','continent':'Continent',
                'country':'Country','pressure':'Pressure'})
    map_fig.update_layout(plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)')

    line_fig = px.line(data_frame=df, 
                x="observation_time",  y = df[yvar] , color='continent',line_group="country", 
                hover_data=['precipitation','observation_time'],
                 # Add bold variable in hover information
                  hover_name='country',color_discrete_map=color_discrete_map,
                 # change labels
                 labels={'precipitation':'Precipitation','observation_time':'Day','continent':'Continent',
                     'country':'Country','pressure':'Pressure'})
    line_fig.update_layout(plot_bgcolor='rgb(233, 238, 245)',
        paper_bgcolor='rgb(233, 238, 245)')
        
    return [map_fig, line_fig]

# needed only if running this as a single page app
#if __name__ == '__main__':
#    app.run_server(port=8097,debug=True)
