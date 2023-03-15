from dash import html, dcc
import dash_bootstrap_components as dbc
import pathlib
from app import app


DATA_PATH = pathlib.Path(__file__).parent.joinpath("data").resolve()


text = dcc.Markdown(
    """
    ##### Documentation

    The goal of this project is to build a visual representation of all possible scopes for calculating greenhouse gas footprint. We use EXIOBASE3 - a global multi-regional input-output database - to calculate emissions for 49 regions of the world between 1995 and 2019. 
    
    A full explanation of the diagrams is available in the paper: https://doi.org/10.21203/rs.3.rs-2617637/v1

    ##### Code and figures downloads
    
    The **code** used to calculate the **footprints** is available on github: https://github.com/baptiste-an/Mapping-global-ghg-emissions

    The **code** to build the **application** is available on github: https://github.com/baptiste-an/Application-mapping-GHG

    The **sankey diagrams in svg format** can be downloaded on github: https://github.com/baptiste-an/Mapping-global-ghg-emissions/tree/main/Results/Sankey_figs

    ##### Funding

    Most of this work has been funded by [*The Shift Project*](https://theshiftproject.org/en), a French think tank advocating the shift to a post carbon economy. As a non-profit organisation committed to serving the general interest, *The Shift Project* is dedicated to informing and influencing the debate on energy transition in Europe.

    Other funders include [ISTerre]("https://www.isterre.fr/?lang=en"), [STEEP]("https://steep.inria.fr/en/"), [GAEL]("https://gael.univ-grenoble-alpes.fr/?language=en"), [University Grenoble Alpes]("https://www.univ-grenoble-alpes.fr/english/"), [CNRS](https://www.cnrs.fr/en), and the [French National Research Agency](https://anr.fr/en/).

    ##### Citation

    Andrieu, B., Le Boulzec, H., Delannoy, L., Verzier, F., Winter, G., Vidal, O., Mapping global greenhouse gases emissions: an interactive, open-access, web application. Available at: https://doi.org/10.21203/rs.3.rs-2617637/v1
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
                    width=2,
                ),
                dbc.Col(
                    [
                        html.A(
                            html.Img(src=app.get_asset_url("isterre2.jpg"), style={"height": 100, "justify": "center"}),
                            href="https://www.isterre.fr/?lang=en",
                            target="_blank",
                        )
                    ],
                    width=2,
                ),
                dbc.Col(
                    [
                        html.A(
                            html.Img(src=app.get_asset_url("steep2.jpg"), style={"height": 100, "justify": "center"}),
                            href="https://steep.inria.fr/en/",
                            target="_blank",
                        )
                    ],
                    width=2,
                ),
                dbc.Col(
                    [
                        html.A(
                            html.Img(src=app.get_asset_url("gael2.jpg"), style={"height": 100, "justify": "center"}),
                            href="https://gael.univ-grenoble-alpes.fr/?language=en",
                            target="_blank",
                        )
                    ],
                    width=2,
                ),
                dbc.Col(
                    [
                        html.A(
                            html.Img(src=app.get_asset_url("uga2.jpg"), style={"height": 100, "justify": "center"}),
                            href="https://www.univ-grenoble-alpes.fr/english/",
                            target="_blank",
                        )
                    ],
                    width=2,
                ),
            ],
            justify="center",
        ),
        html.Div(text, className="border", style={"fontSize": 13})
        # dbc.Row([dbc.Col([thanks], width=12)])
        # html.Div(thanks, id="page-content"),
    ],
    fluid=True,
)
