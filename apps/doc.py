import pandas as pd
import plotly.graph_objs as go
from dash import Dash, html, dcc, Output, Input, State, callback, MATCH
from dash_auth import BasicAuth
from dash.exceptions import PreventUpdate
import uuid
import dash_bootstrap_components as dbc
import pyarrow.feather as feather
import pathlib
import json
from flask_caching import Cache
from app import app
from slider import PlaybackSliderAIO
import base64

DATA_PATH = pathlib.Path(__file__).parent.joinpath("data").resolve()

thanks = html.Div(
    html.P(["Graciously hosted by ", html.A("scalingo", href="https://scalingo.com", target="_blank"), " in 🇫🇷"]),
    id="thanks",
)


layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.A(
                            html.Img(src=app.get_asset_url("tsp2.jpg"), style={"height": 100, "justify": "center"}),
                            href="https://theshiftproject.org/en/home/",
                            target="_blank",
                        )
                    ],
                    width=3,
                ),
                dbc.Col(
                    [
                        html.A(
                            html.Img(src=app.get_asset_url("isterre.png"), style={"height": 100, "justify": "center"}),
                            href="https://www.isterre.fr/?lang=en",
                            target="_blank",
                        )
                    ],
                    width=3,
                ),
                dbc.Col(
                    [
                        html.A(
                            html.Img(src=app.get_asset_url("steep2.jpg"), style={"height": 100, "justify": "center"}),
                            href="https://steep.inria.fr/en/",
                            target="_blank",
                        )
                    ],
                    width=3,
                ),
                dbc.Col(
                    [
                        html.A(
                            html.Img(src=app.get_asset_url("uga.png"), style={"height": 100, "justify": "center"}),
                            href="https://www.univ-grenoble-alpes.fr/english/",
                            target="_blank",
                        )
                    ],
                    width=3,
                ),
            ],
        ),
        dbc.Row([dbc.Col([thanks], width=12)])
        # html.Div(thanks, id="page-content"),
    ],
    fluid=True,
)
