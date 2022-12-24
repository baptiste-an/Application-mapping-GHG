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

thanks = html.Div(
    html.P(["Graciously hosted by ", html.A("scalingo", href="https://scalingo.com"), " in 🇫🇷"]),
    id="thanks",
)


layout = html.Div(
    [
        html.Div(thanks, id="page-content"),
    ]
)
