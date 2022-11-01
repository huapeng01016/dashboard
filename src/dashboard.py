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

from dash import Dash, html, dcc, Input, Output
app = Dash()

geo_dropdown = dcc.Dropdown(options=auto['foreign'].unique(), value='1')

app.layout = html.Div(children=[
        html.H1(children='Stata Auto Dataset Dashboard'),
        geo_dropdown,
        dcc.Graph(id='fig_1'),

        dcc.Graph(id='fig_2'),
])


@app.callback(
    Output(component_id='fig_1', component_property='figure'),
    Output(component_id='fig_2', component_property='figure'),
    Input(component_id=geo_dropdown, component_property='value')
)

def update_graph(selected_geography):
    filtered_auto = auto[auto['foreign'] == selected_geography]
    fig_1 = px.scatter(filtered_auto,
                       x='price', y='mpg',
                       color='rep78',
                       title='Auto Prices in {selected_geography}')

    if selected_geography == "Foreign":
        stata.run('''
              sysuse auto, clear
              scatter mpg price if foreign
              graph export sc1.png, replace
              ''', echo=True)

        try:
            img = np.array(Image.open("C:/stata/talks/dashboard/src/sc1.png"))
        except OSError:
            raise PreventUpdate
    elif selected_geography == "Domestic":
        stata.run('''
              sysuse auto, clear
              scatter mpg price if !foreign
              graph export sc2.png, replace
              ''', echo=True)
    
        try:
            img = np.array(Image.open("C:/stata/talks/dashboard/src/sc2.png"))
        except OSError:
            raise PreventUpdate
    else:
        stata.run('''
              sysuse auto, clear
              scatter price mpg 
              graph export sc3.png, replace
              ''', echo=True)
    
        try:
            img = np.array(Image.open("C:/stata/talks/dashboard/src/sc3.png"))
        except OSError:
            raise PreventUpdate
            
    fig_2 = px.imshow(img, color_continuous_scale="gray")

    return [fig_1, fig_2]

if __name__ == '__main__':
    app.run_server(debug=True)
