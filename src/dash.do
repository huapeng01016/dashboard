cscript

sysuse auto, clear

python:
from sfi import Data
import numpy as np
import pandas as pd
dataraw   = Data.get('foreign mpg price', valuelabel=True,
                     missingval=np.nan)
df = pd.DataFrame(dataraw, columns=['foreign', 'mpg', 'price'])


import plotly.express as px
import plotly.io as pio
pio.renderers.default = 'browser'
fig = px.scatter(df, x='mpg', y='price', color='foreign')
fig.show()
end
