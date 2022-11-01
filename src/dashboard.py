# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 09:21:23 2022

@author: hop
"""
import os
import pandas as pd
import plotly.express as px
import plotly.io as pio
from PIL import Image
import numpy as np
from dash.exceptions import PreventUpdate

pio.renderers.default = 'browser'
auto = pd.read_csv('../data/auto.csv')

import stata_setup
stata_setup.config("C:/Program Files/Stata17", "se")
from pystata import stata

from pystata import stata


# fig = px.scatter(df, x='mpg', y='price', color='foreign')
# fig.show()

from dash import Dash, html, dcc, Input, Output, dash_table
app = Dash()

geo_dropdown = dcc.Dropdown(options=auto['foreign'].unique(), value='ALL')

app.layout = html.Div(children=[
        html.H1(children='Stata Auto Dataset Dashboard'),
        geo_dropdown,


        dash_table.DataTable(id='data_table'),

        dcc.Graph(id='fig_1'),

        dcc.Graph(id='fig_2'),

        html.Iframe(
            id="regress-output",
            src="assets/tt3.html",
            ),        
])


@app.callback(
    Output(component_id='data_table', component_property='data'),
    Output(component_id='data_table', component_property='columns'),
    Output(component_id='fig_1', component_property='figure'),
    Output(component_id='fig_2', component_property='figure'),
    Output(component_id='regress-output', component_property='src'), 
    Input(component_id=geo_dropdown, component_property='value')
)

def update_graph(selected_geography):
    if selected_geography == "ALL":
        filtered_auto = auto
    else:
        filtered_auto = auto[auto['foreign'] == selected_geography]
    
    data = filtered_auto.to_dict(orient='records')
    columns = [{'name': col, 'id': col} for col in filtered_auto.columns]
    
    fig_1 = px.scatter(filtered_auto,
                       x='price', y='mpg',
                       color='rep78',
                       title='Auto Prices in {selected_geography}')

    if selected_geography == "Foreign":
        stata.run('''
              sysuse auto, clear
              scatter mpg price if foreign
              graph export sc1.png, replace
              ''')

        try:
            img = np.array(Image.open("C:/stata/talks/dashboard/src/sc1.png"))
        except OSError:
            raise PreventUpdate
    elif selected_geography == "Domestic":
        stata.run('''
              sysuse auto, clear
              scatter mpg price if !foreign
              graph export sc2.png, replace
              ''')
    
        try:
            img = np.array(Image.open("C:/stata/talks/dashboard/src/sc2.png"))
        except OSError:
            raise PreventUpdate
    else:
        stata.run('''
              sysuse auto, clear
              scatter price mpg 
              graph export sc3.png, replace
              ''')
    
        try:
            img = np.array(Image.open("C:/stata/talks/dashboard/src/sc3.png"))
        except OSError:
            raise PreventUpdate
            
    fig_2 = px.imshow(img, color_continuous_scale="gray")

    if selected_geography == "Foreign":
        stata.run('''
              sysuse auto, clear
              regress price mpg if foreign 
              etable
              collect export assets/tt1.html, replace
              ''')
              
        src = "assets/tt1.html"
    elif selected_geography == "Domestic":
        stata.run('''
              sysuse auto, clear
              regress price mpg if !foreign 
              etable
              collect export assets/tt2.html, replace
              ''')
              
        src = "assets/tt2.html"
    else:
        stata.run('''
              sysuse auto, clear
              regress price mpg
              etable
              collect export assets/tt3.html, replace
              ''')
              
        src = "assets/tt3.html"
    
    return [data, columns, fig_1, fig_2, src]

if __name__ == '__main__':
    app.run_server(debug=True)
