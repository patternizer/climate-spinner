#! /usr/bin python

#------------------------------------------------------------------------------
# PROGRAM: app.py
#------------------------------------------------------------------------------
# Version 0.1
# 8 July, 2020
# Michael Taylor
# https://patternizer.github.io
# patternizer AT gmail DOT com
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# IMPORT PYTHON LIBRARIES
#------------------------------------------------------------------------------
import numpy as np
import random
from random import randint
from random import randrange
# Plotting libraries:
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import colors as mcol
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# Silence library version notifications
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
# App Deployment Libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from flask import Flask
import os
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# METHODS: impact scales
#------------------------------------------------------------------------------

def choose_spinner(value):
    
    if value == 0:
        # Saffir-Simpson Hurricane Categories: https://en.wikipedia.org/wiki/Saffir%E2%80%93Simpson_scale
        #
        # NB: Beaufort Wind Force Scale / Tropical Cyclone Intensity Scale: https://en.wikipedia.org/wiki/Tropical_cyclone_scales
        # (terminology for tropical cyclones differs across regions)        
        # Cat 1   33–42 m/s   Very dangerous winds will produce some damage
        # Cat 2   43–49 m/s   Extremely dangerous winds will cause extensive damage 
        # Cat 3   50–58 m/s   Devastating damage will occur 
        # Cat 4   58–70 m/s   Catastrophic damage will occur 
        # Cat 5   ≥ 70 m/s    Catastrophic damage will occur 

        labels = ['Cat 1', 'Cat 2', 'Cat 3', 'Cat 4', 'cat 5']        
        angles_now = np.array([0.4, 0.35, 0.15, 0.08, 0.02]) * 360.0
        angles_cc = np.array([0.3, 0.3, 0.2, 0.12, 0.08]) * 360.0

    elif value == 1:
        # Heat Index Categories: https://en.wikipedia.org/wiki/Heat_index       
        #
        # 26–32 °C  Caution: fatigue is possible with prolonged exposure and activity. Continuing activity could result in heat cramps.
        # 32–41 °C 	Extreme caution: heat cramps and heat exhaustion are possible. Continuing activity could result in heat stroke.
        # 41–54 °C 	Danger: heat cramps and heat exhaustion are likely; heat stroke is probable with continued activity.
        # >  54 °C 	Extreme danger: heat stroke is imminent.         

        labels = ['Caution', 'Extreme Caution', 'Danger', 'Extreme Danger']
        angles_now = np.array([0.25, 0.25, 0.25, 0.25]) * 360.0
        angles_cc = np.array([0.25, 0.25, 0.25, 0.25]) * 360.0

    elif value == 2:
        # Flood Alert Categories: https://flood-warning-information.service.gov.uk/warnings
        #        
        
        labels = ['Alert', 'Warning', 'Severe']
        angles_now = np.array([0.33, 0.33, 0.34]) * 360.0
        angles_cc = np.array([0.33, 0.33, 0.34]) * 360.0
        
    elif value == 3:
        # Air Quality Index Categories: https://en.wikipedia.org/wiki/Air_quality_index
        #
        # Low       1–3 	Enjoy your usual outdoor activities. 	Enjoy your usual outdoor activities.
        # Moderate 	4–6 	Adults and children with lung problems, and adults with heart problems, who experience symptoms, should consider reducing strenuous physical activity, particularly outdoors. 	Enjoy your usual outdoor activities.
        # High      7–9 	Adults and children with lung problems, and adults with heart problems, should reduce strenuous physical exertion, particularly outdoors, and particularly if they experience symptoms. People with asthma may find they need to use their reliever inhaler more often. Older people should also reduce physical exertion. 	Anyone experiencing discomfort such as sore eyes, cough or sore throat should consider reducing activity, particularly outdoors.
        # Very High  10 	Adults and children with lung problems, adults with heart problems, and older people, should avoid strenuous physical activity. People with asthma may find they need to use their reliever inhaler more often. 	Reduce physical exertion, particularly outdoors, especially if you experience symptoms such as cough or sore throat.         
        #
        # Index 	Ozone, Running 8 hourly mean (μg/m3) 	Nitrogen Dioxide, Hourly mean (μg/m3) 	Sulphur Dioxide, 15 minute mean (μg/m3) 	PM2.5 Particles, 24 hour mean (μg/m3) 	PM10 Particles, 24 hour mean (μg/m3)
        #   1       0–33        0–67         0–88       0–11 	0–16
        #   2       34–66       68–134       89–177 	12–23 	17–33
        #   3       67–100      135–200 	178–266 	24–35 	34–50
        #   4       101–120 	201–267 	267–354 	36–41 	51–58
        #   5       121–140 	268–334 	355–443 	42–47 	59–66
        #   6       141–160 	335–400 	444–532 	48–53 	67–75
        #   7       161–187 	401–467 	533–710 	54–58 	76–83
        #   8       188-213 	468–534 	711–887 	59–64 	84–91
        #   9       214–240 	535–600 	888–1064 	65–70 	92–100
        #   10      ≥ 241       ≥ 601       ≥ 1065      ≥ 71    ≥ 101         
        
        labels = ['Low', 'Moderate', 'High', 'Very High']
        angles_now = np.array([0.25, 0.25, 0.25, 0.25]) * 360.0
        angles_cc = np.array([0.25, 0.25, 0.25, 0.25]) * 360.0

    elif value == 4:
        # UV Index Categories: https://en.wikipedia.org/wiki/Ultraviolet_index
        #
        # 0 to 2 	Green 	"Low"         A UV index reading of 0 to 2 means low danger from the Sun's UV rays for the average person. Wear sunglasses on bright days. If you burn easily, cover up and use broad spectrum SPF 30+ sunscreen. Bright surfaces, such as sand, water, and snow, will increase UV exposure.
        # 3 to 5 	Yellow 	"Moderate"    A UV index reading of 3 to 5 means moderate risk of harm from unprotected Sun exposure. Stay in shade near midday when the Sun is strongest. If outdoors, wear Sun protective clothing, a wide-brimmed hat, and UV-blocking sunglasses. Generously apply broad spectrum SPF 30+ sunscreen every 1.5 hours, even on cloudy days, and after swimming or sweating. Bright surfaces, such as sand, water, and snow, will increase UV exposure.
        # 6 to 7 	Orange 	"High"        A UV index reading of 6 to 7 means high risk of harm from unprotected Sun exposure. Protection against skin and eye damage is needed. Reduce time in the Sun between 10 a.m. and 4 p.m. If outdoors, seek shade and wear Sun protective clothing, a wide-brimmed hat, and UV-blocking sunglasses. Generously apply broad spectrum SPF 30+ sunscreen every 1.5 hours, even on cloudy days, and after swimming or sweating. Bright surfaces, such as sand, water, and snow, will increase UV exposure.
        # 8 to 10 	Red 	"Very high"   A UV index reading of 8 to 10 means very high risk of harm from unprotected Sun exposure. Take extra precautions because unprotected skin and eyes will be damaged and can burn quickly. Minimize Sun exposure between 10 a.m. and 4 p.m. If outdoors, seek shade and wear Sun protective clothing, a wide-brimmed hat, and UV-blocking sunglasses. Generously apply broad spectrum SPF 30+ sunscreen every 1.5 hours, even on cloudy days, and after swimming or sweating. Bright surfaces, such as sand, water, and snow, will increase UV exposure.
        # 11+       Violet 	"Extreme"     A UV index reading of 11 or more means extreme risk of harm from unprotected Sun exposure. Take all precautions because unprotected skin and eyes can burn in minutes. Try to avoid Sun exposure between 10 a.m. and 4 p.m. If outdoors, seek shade and wear Sun protective clothing, a wide-brimmed hat, and UV-blocking sunglasses. Generously apply broad spectrum SPF 30+ sunscreen every 1.5 hours, even on cloudy days, and after swimming or sweating. Bright surfaces, such as sand, water, and snow, will increase UV exposure. 
        
        labels = ['Low', 'Moderate', 'High', 'Very High', 'Extreme']
        angles_now = np.array([0.2, 0.2, 0.2, 0.2, 0.2]) * 360.0
        angles_cc = np.array([0.2, 0.2, 0.2, 0.2, 0.2]) * 360.0

    elif value == 5:
        # Enhanced Fujita Tornado Scale: 
        #
        # EF0 	65–85 mph    Light damage
        # EF1 	86–110 mph   Moderate damage
        # EF2 	111–135 mph  Considerable damage
        # EF3 	136–165 mph  Severe damage
        # EF4 	166–200 mph  Devastating damage
        # EF5 	>200 mph     Incredible damage 

        labels = ['EF0', 'EF1', 'EF2', 'EF3', 'EF4', 'EF5']
        angles_now = np.array([0.16, 0.16, 0.16, 0.16, 0.16, 0.2]) * 360.0
        angles_cc = np.array([0.16, 0.16, 0.16, 0.16, 0.16, 0.2]) * 360.0

    return labels, angles_now, angles_cc

#------------------------------------------------------------------------------
# SETTINGS
#------------------------------------------------------------------------------

# Climate spinner key value:

  # 0 = Saffir-Simpson Hurricane Categories
  # 1 = Heat Index Categories
  # 2 = Flood Alert Categories
  # 3 = Air Quality Index Categories
  # 4 = UV Index Categories
  # 5 = Enhanced Fujita Tornado Scale

spinners = ['Hurricanes (Saffir-Simpson)', 'Heat Index (HI)', 'Flood Alerts (UKEA)', 'Air Quality Index (AQI)', 'Ultraviolet Index (UVI)', 'Tornados (Enhanced Fujita)']
value = 0
opts = [{'label' : spinners[i], 'value' : i} for i in range(len(spinners))]

# ========================================================================
# Start the App
# ========================================================================

server = Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=server)
app.config.suppress_callback_exceptions = True

app.layout = html.Div(children=[
            
# ------------
    html.H1(children='Climate Spinners',            
            style={'padding' : '10px', 'width': '100%', 'display': 'inline-block'},
    ),
# ------------
            
# ------------
    html.Div([

        dbc.Row([

            # ------------
            dbc.Col(html.Div([
                    
                dcc.Dropdown(
                    id = "input",
                    options = opts,           
                    value = 0,
                    style = {'padding' : '10px', 'width': '60%', 'display': 'inline-block'},
                ),
                                    
            ]), 
            width={'size':8}, 
            ),
                        
# ------------
            dbc.Col(html.Div([

                dcc.RadioItems(
                    id = "radio",
                    options=[
                        {'label': ' Viridis', 'value': 'Viridis'},
                        {'label': ' Cividis', 'value': 'Cividis'},
                        {'label': ' Plotly3', 'value': 'Plotly3'},
                        {'label': ' Magma', 'value': 'Magma'},
                        {'label': ' Shikari', 'value': 'Shikari'}                        
                    ],
                    value = 'Shikari',
                    labelStyle={'padding' : '5px', 'display': 'inline-block'},
                ),
                               
            ]), 
            width={'size':4}, 
            ),
            
        ]),
    ]),
# ------------

# ------------
    html.Div([   

        dbc.Row([

# ------------
            dbc.Col(html.Div([
                dcc.Graph(id="climate-spinner", style = {'padding' : '0px', 'width': '100%', 'display': 'inline-block'}),  
            ]), 
            width={'size':8}, 
            ),
            
# ------------
            dbc.Col(html.Div([  
                                                    
# ------------
                dbc.Row(

                    html.P([
                        html.H3(children='About'),
                        html.Div(children='A visual tool for the public and media to use to help understand and communicate statistical climate attribution and the probability of occurrence of extreme weather events using digital climate spinner boards. The app is designed as a basis for including a range of probabilistic climate impact scales as they are now and how they are expected to change in reponse to anthropogenic climate change.'),
                    ],                        
                    style = {'padding' : '10px', 'fontSize' : '15px', 'width': '90%', 'display': 'inline-block'}),   
                ),

# ------------
                dbc.Row(

                    html.P([
                        html.Div(children=['Inspiration: Twitter thread by ', html.A('@richardabetts', href='https://twitter.com/richardabetts/status/1280794725679800321')]),                            
                        html.Div(children=['& paper by: ', html.A('Dryden & Morgan (2020)', href='https://doi.org/10.1175/BAMS-D-19-0174.1')]),    
                        html.Div(children=['Codebase: ', html.A('Github', href='https://github.com/patternizer/climate-spinner')]),       
                    ],
                    style = {'padding' : '10px', 'fontSize' : '15px', 'width': '100%', 'display': 'inline-block'}),                               
                ),

# ------------
                dbc.Row(

                    html.P([
                        html.Div(children=['Created using Plotly Python by ', html.A('Michael Taylor', href='https://patternizer.github.io')]),            
                    ],
                    style = {'padding' : '10px', 'fontSize' : '15px', 'width': '100%', 'display': 'inline-block'}),                               
                ),
     
            ]), 
            width={'size':4}, 
            ),
                
        ]),
                        
    ]), 
# ------------

])

# ========================================================================
# Callbacks
# ========================================================================
           
@app.callback(
    Output(component_id='climate-spinner', component_property='figure'),
    [Input(component_id='input', component_property='value'), 
    Input(component_id='radio', component_property='value')],    
    )
    
def update_graph(value, colors):

    labels, angles_now, angles_cc = choose_spinner(value)
    nlabels = len(labels)
    
    
    # Create Plotly figure
    """
    Draw climate spinner
    """
    if colors == 'Viridis':    
        cmap = px.colors.sequential.Viridis_r
    elif colors == 'Cividis':    
        cmap = px.colors.sequential.Cividis_r
    elif colors == 'Plotly3':
        cmap = px.colors.sequential.Plotly3_r
    elif colors == 'Magma':
        cmap = px.colors.sequential.Magma_r
    elif colors == 'Shikari':
        cmap = ['#2f2f2f','#a1dcfc','#fdee03','#75b82b','#a84190','#0169b3']                                
    cmap_idx = np.linspace(0,len(cmap)-1, nlabels, dtype=int)
    colors = [cmap[i] for i in cmap_idx]
                    
    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    fig.add_trace(go.Pie(labels=labels, values=angles_now, name="Now"), 1, 1)
    fig.add_trace(go.Pie(labels=labels, values=angles_cc, name="Future"), 1, 2)
    
    fig.update_traces(
        hoverinfo='percent', 
        textinfo='label', 
        insidetextorientation='radial', 
        textfont_size=15, 
        marker=dict(colors=colors, line=dict(color='#000000', width=2)),
        hole=0.5,
    )
        
    fig.update_layout(
#        title_text="Climate Spinners",
        annotations=[
            dict(text='Now', x=0.2, y=0.5, font_size=20, showarrow=False),
            dict(text='Future', x=0.825, y=0.5, font_size=20, showarrow=False)])
    
    return fig
        
##################################################################################################
# Run the dash app
##################################################################################################

if __name__ == "__main__":
    app.run_server(debug=True)
    



