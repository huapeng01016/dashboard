cscript


syntax [anything] , [show]

python:
import numpy as np
import pandas as pd
df = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/01-10-2021.csv")
df.columns = df.columns.str.lower()
df = df.loc[df['country_region'] == "US"]
df = df.loc[df['province_state'] == "Texas"]     
end

python:
df.count()
end

quietly python:
from urllib.request import urlopen
import numpy as np
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)


import plotly.express as px
fig = px.choropleth(df, geojson=counties, locations='fips', color='confirmed',
						   hover_data=['confirmed'],
						   color_continuous_scale='ylorrd',
						   range_color = [100, 5000],
						   scope="usa",
                           labels={'confirmed':'confirmed cases'},
                           width=800, height=800,
						  )

fig.update_geos(fitbounds="locations", visible=False)

fig.write_image("../images/fig1.svg")
end
