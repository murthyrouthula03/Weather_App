#import packages to create app
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from gapminder import gapminder

import plotly.express as px
import pandas as pd
import numpy as np
import os,sys

app=dash.Dash()
server=app.server

pwd = os.getcwd()

#data for the region plot
loc_data = px.data.gapminder()

# reading the input file
df_data = pd.read_csv(pwd+"//weather_final_data1.csv")
df2 = df_data.merge(loc_data[['continent','iso_alpha']], how='left', left_on='iso3', right_on='iso_alpha')
#print(df2[df2['country'] == "India"])
#get European data
Afr_data =df2[df2['continent'] == "Africa"]
#get unique countries
country_names = Afr_data['country'].unique()
loc_cols=list(df2.columns)
#print(Afr_data['observation_time'])
#print(Afr_data)
Afr_data = Afr_data.drop_duplicates()
#print(Afr_data.isnull().sum())
#sys.exit()



color_discrete_map = {}

# needed only if running this as a single page app
from app import app
#app = dash.Dash(__name__)
#change background and color text
colors = {
    #background to rgb(233, 238, 245)
    'background': '#8FB0FF',
    'text': '#000000'
}



# change to app.layout if running as single page app instead
layout = html.Div(style={'backgroundColor': colors['background']},children=[
    dbc.Container([
        dbc.Row([
            #Header span the whole row
            #className: Often used with CSS to style elements with common properties.
            dbc.Col(html.H1("African Countries Weather",        
             style={
            'textAlign': 'center',
            'color': colors['text']}), 
            className="mb-5 mt-5")
        ]),
        html.Div([
            html.Div([
                html.Label('Select Country/Countries'),
                dcc.Dropdown(id='country_dropdown',
                            options=[{'label': i, 'value': i}
                                    for i in country_names],
                            value=country_names,
                            multi=True
                )
            ],style={'width': '49%', 'display': 'inline-block'}),
            html.Div([
                html.Label('Select UV Index Range'),
                dcc.RangeSlider(id='eur_pop_range',
                    min=0,
                    max=10,
                    value=[0,10],
                    step= 1,
                    marks={
                        0: '0',
                        3: '3',
                        6: '6',
                        10: '10'
                    },
                ),
                html.Label('Select climate parameter to display on the Graphs'),
                dcc.Dropdown(id='eur_y_dropdown',
                    options=[                    
                        {'label': 'Temperature', 'value': 'temperature'},
                        {'label': 'UV Index', 'value': 'uv_index'},
                        {'label': 'Wind Degree', 'value': 'wind_degree'}],
                    value='temperature',
                )
            ],style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
        ]),
        html.Div([
            dcc.Graph(
                id='barchart2'
            ),
            ],style={'width': '80%', 'margin-left': '10%','display': 'inline-block'}),
        html.Div([
            html.Div([
                dcc.Graph(
                        id='geochart2'
                ),
            ],style={'width': '49%','display': 'inline-block'}),
            html.Div([
                dcc.Graph(
                    id='trendline2'
                ),
            ],style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
            ]),
    ])
])


@app.callback(
    [Output(component_id='barchart2', component_property='figure'),
    Output(component_id='geochart2', component_property='figure'),
    Output(component_id='trendline2', component_property='figure')],
    [Input(component_id='country_dropdown', component_property='value'),
    Input(component_id='eur_pop_range', component_property='value'),
    Input(component_id='eur_y_dropdown', component_property='value')]
)
def update_graphs(selected_count,erangevalue,eyvar):
    if not (selected_count or erangevalue or eyvar):
        return dash.no_update
    d = Afr_data[(Afr_data['uv_index'] >= erangevalue[0]) & (Afr_data['uv_index'] <= erangevalue[1])]
    data =[]
    for j in selected_count:
            data.append(d[d['country'] == j])
    df = pd.DataFrame(np.concatenate(data), columns=loc_cols)
    df=df.infer_objects()
    # converting date to datetime
    #df['observation_time'] = pd.to_datetime(df['observation_time'],format="%Y-%m-%d")
    barfig = px.bar(df, y=eyvar, x='country',animation_frame="observation_time",
             # add text labels to bar
             text=eyvar, color='country', 
             # different colour for each country
             color_discrete_map=color_discrete_map,
             # Add country and windspeed info to hover text
             hover_data=['temperature','place'],
             # change labels
             labels={'uv_index':'UV Index','country':'Country','temperature':'Temperature'})
    #update text to be number format rounded with unit 
    barfig.update_traces(texttemplate='%{text:.2s}')
    #update text to be font size 8 and hide if text can not stay with the uniform size
    barfig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',
        plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)',
        showlegend=False, margin=dict( b=200),xaxis_title="")
    barfig['layout']['updatemenus'][0]['pad']=dict(r= 10, t= 170)
    barfig['layout']['sliders'][0]['pad']=dict(r= 10, t= 170,)
    if eyvar == 'temperature':
         barfig.update_yaxes(range=[-40, 100])
    elif eyvar == 'uv_index':
         barfig.update_yaxes(range=[0, 20])
    else:
         barfig.update_yaxes(range=[0, 720])
         

    mapfig= px.choropleth(df,locations="iso3", color=df[eyvar],
            hover_name="country",hover_data=['continent','uv_index','place'],animation_frame="observation_time",    
            color_continuous_scale='Turbo',range_color=[df[eyvar].min(), df[eyvar].max()],
            labels={'uv_index':'UV Index','observation_time':'Day','continent':'Continent',
                'country':'Country','temperature':'Temperature'})
    mapfig.update_layout(plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)')
    mapfig.update_geos(fitbounds="locations")
    mapfig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    linefig = px.line(data_frame=df, 
                x="observation_time",  y = df[eyvar] , color='country',
                # different colour for each country
                color_discrete_map=color_discrete_map,
                hover_data=['uv_index','observation_time','place'],
                 # Add bold variable in hover information
                  hover_name='country',
                 # change labels
                 labels={'uv_index':'UV Index','observation_time':'Day','continent':'Continent',
                     'country':'Country','temperature':'Temperature'})
    linefig.update_layout(plot_bgcolor='rgb(233, 238, 245)',
        paper_bgcolor='rgb(233, 238, 245)')
        
    return [barfig, mapfig, linefig]


# needed only if running this as a single page app
#if __name__ == '__main__':
#    app.run_server(port=8079,debug=True)
