from dash import html
import dash_bootstrap_components as dbc
import pathlib
from app import app


DATA_PATH = pathlib.Path(__file__).parent.joinpath("data").resolve()


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
        # dbc.Row([dbc.Col([thanks], width=12)])
        # html.Div(thanks, id="page-content"),
    ],
    fluid=True,
)
