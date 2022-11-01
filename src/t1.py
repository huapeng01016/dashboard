# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 09:59:03 2022

@author: hop
"""

import plotly.graph_objects as go

import plotly.io as pio
#pio.renderers.default = 'svg'
pio.renderers.default = 'browser'

x = ['Product A', 'Product B', 'Product C']
y = [20, 14, 23]

fig = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=y,
            textposition='auto',
        )])
fig.show()
