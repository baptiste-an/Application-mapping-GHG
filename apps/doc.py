from dash import html, dcc
import dash_bootstrap_components as dbc
import pathlib
from app import app


DATA_PATH = pathlib.Path(__file__).parent.joinpath("data").resolve()

text = (
    dcc.Textarea(
        id="textarea-state-example",
        value="",
        style={"width": "100%", "height": 200},
    ),
)
text = dcc.Markdown(
    """
    The goal of this project is to build a visual representation of all possible scopes for calculating greenhouse gas footprint. We use EXIOBASE3 - a global multi-regional input-output database - to calculate emissions for 49 regions of the world between 1995 and 2019. 
    
    A full explanation of the diagrams is available in the **paper**: not yet posted on preprint server

    The **code** used to calculate the **footprints** is available on github: https://github.com/baptiste-an/Mapping-global-ghg-emissions

    The **code** to build the **application** is available on github: https://github.com/baptiste-an/Application-mapping-GHG

    The **sankey diagrams in svg format** can be downloaded on github: https://github.com/baptiste-an/Mapping-global-ghg-emissions/tree/main/Results/Sankey_figs


"""
)

# *This text will be italic*

# _This will also be italic_


# **This text will be bold**

# __This will also be bold__

# _You **can** combine them_


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
                            html.Img(src=app.get_asset_url("isterre2.jpg"), style={"height": 100, "justify": "center"}),
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
                            html.Img(src=app.get_asset_url("uga2.jpg"), style={"height": 100, "justify": "center"}),
                            href="https://www.univ-grenoble-alpes.fr/english/",
                            target="_blank",
                        )
                    ],
                    width=3,
                ),
            ],
        ),
        html.Div(text, className="border")
        # dbc.Row([dbc.Col([thanks], width=12)])
        # html.Div(thanks, id="page-content"),
    ],
    fluid=True,
)
