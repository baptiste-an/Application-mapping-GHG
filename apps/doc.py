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

    Andrieu, B., Le Boulzec, H., Delannoy, L., Verzier, F., Winter, G., Vidal, O., Stadler, K., An open-access web application to visualise countries’ and regions’ carbon footprints using Sankey diagrams. Available at: https://www.nature.com/articles/s43247-024-01378-8

    Based on Stadler, K.; Wood, R.; Bulavskaya, T.; Södersten, C.-J.; Simas, M.; Schmidt, S.; Usubiaga, A.; Acosta-Fernández, J.; Kuenen, J.; Bruckner, M.; Giljum, S.; Lutter, S.; Merciai, S.; Schmidt, J. H.; Theurl, M. C.; Plutzar, C.; Kastner, T.; Eisenmenger, N.; Erb, K.-H.; de Koning, A.; Tukker, A. EXIOBASE 3: Developing a Time Series of Detailed Environmentally Extended Multi-Regional Input-Output Tables: EXIOBASE 3. Journal of Industrial Ecology 2018, 22 (3), 502–515. https://doi.org/10.1111/jiec.12715.

    And Södersten, C.-J. H.; Wood, R.; Hertwich, E. G. Endogenizing Capital in MRIO Models: The Implications for Consumption-Based Accounting. Environ. Sci. Technol. 2018, 52 (22), 13250–13259. https://doi.org/10.1021/acs.est.8b02791.
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
                            html.Img(
                                src=app.get_asset_url("NTNU.png"),
                                style={"height": 100, "justify": "center"},
                            ),
                            href="https://www.ntnu.edu/",
                            target="_blank",
                        )
                    ],
                    width=2,
                ),
                dbc.Col(
                    [
                        html.A(
                            html.Img(
                                src=app.get_asset_url("tsp2.jpg"),
                                style={"height": 100, "justify": "center"},
                            ),
                            href="https://theshiftproject.org/en/home/",
                            target="_blank",
                        )
                    ],
                    width=2,
                ),
                dbc.Col(
                    [
                        html.A(
                            html.Img(
                                src=app.get_asset_url("isterre2.jpg"),
                                style={"height": 100, "justify": "center"},
                            ),
                            href="https://www.isterre.fr/?lang=en",
                            target="_blank",
                        )
                    ],
                    width=2,
                ),
                dbc.Col(
                    [
                        html.A(
                            html.Img(
                                src=app.get_asset_url("steep2.jpg"),
                                style={"height": 100, "justify": "center"},
                            ),
                            href="https://steep.inria.fr/en/",
                            target="_blank",
                        )
                    ],
                    width=2,
                ),
                dbc.Col(
                    [
                        html.A(
                            html.Img(
                                src=app.get_asset_url("gael2.jpg"),
                                style={"height": 100, "justify": "center"},
                            ),
                            href="https://gael.univ-grenoble-alpes.fr/?language=en",
                            target="_blank",
                        )
                    ],
                    width=2,
                ),
                # dbc.Col(
                #     [
                #         html.A(
                #             html.Img(src=app.get_asset_url("uga2.jpg"), style={"height": 100, "justify": "center"}),
                #             href="https://www.univ-grenoble-alpes.fr/english/",
                #             target="_blank",
                #         )
                #     ],
                #     width=2,
                # ),
            ],
            justify="center",
        ),
        html.Div(text, className="border", style={"fontSize": 13}),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.A(
                            html.Img(
                                src=app.get_asset_url("exiobase.png"),
                                style={"height": 100, "justify": "center"},
                            ),
                            href="https://www.exiobase.eu/",
                            target="_blank",
                        )
                    ],
                    width=6,
                )
            ],
            justify="center",
        ),
        # dbc.Row([dbc.Col([thanks], width=12)])
        # html.Div(thanks, id="page-content"),
    ],
    fluid=True,
)
