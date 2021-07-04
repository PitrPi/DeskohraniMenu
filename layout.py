import dash
import plotly
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import pandas
from dash.dependencies import Input, Output

layout = html.Div([
    html.H1('Deskoherní menu')
    , dbc.Row([dbc.Col(
        html.Div([
            html.H2('Filters')
            , html.Div([html.H5('Players Slider')
                           , dcc.RangeSlider(id='players-slider'
                                             , min=1
                                             , max=8
                                             , marks={1: '1',
                                                      2: '2',
                                                      3: '3',
                                                      4: '4',
                                                      5: '5',
                                                      6: '6',
                                                      7: '7',
                                                      8: '8+'
                                                      }
                                             , value=[0, 5]
                                             )

                        ])

        ], style={'marginBottom': 50, 'marginTop': 25, 'marginLeft': 15, 'marginRight': 15})
        , width=3)

        , dbc.Col(html.Div([
            dcc.Tabs(id="tabs", value='tab-1', children=[
                dcc.Tab(label='Data Table', value='tab-1'),
                dcc.Tab(label='Scatter Plot', value='tab-2'),
            ])
            , html.Div(id='tabs-content')
        ]), width=9)])

])