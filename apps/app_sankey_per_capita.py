"""
 # @ Create Time: 2022-08-23 15:40:55.513725
"""

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


# VALID_USERNAME_PASSWORD_PAIRS = [["hello", "world"]]
# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
# # server = app.server

# auth = BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)


cache = Cache(app.server, config={"CACHE_TYPE": "FileSystemCache", "CACHE_DIR": "cache"})

DATA_PATH = pathlib.Path(__file__).parent.joinpath("data").resolve()

REGIONS = {}

with open(f"{DATA_PATH}/regions.json") as f:
    REGIONS = json.loads(f.read())

LABELS = [{"label": v, "value": k} for k, v in REGIONS.items()]


dropdown = dcc.Dropdown(
    id="slct2",
    options=LABELS,
    multi=False,
    value="FR",
)
graph = dcc.Graph(
    id="graph2",
    responsive=True,
)
slider = PlaybackSliderAIO(
    aio_id="bruh2",
    slider_props={
        "min": 1995,
        "max": 2019,  # 2019
        "step": 1,
        "value": 1995,
        "marks": {str(year): str(year) for year in range(1995, 2020, 1)},
    },
    button_props={"className": "float-left"},
    interval_props={"interval": 2500},
)
thanks = html.Div(
    html.P(["Graciously hosted by ", html.A("scalingo", href="https://scalingo.com"), " in 🇫🇷"]),
    id="thanks",
)
citation = html.Div(
    "Citation: Andrieu, B., Le Boulzec, H., Delannoy, L., Verzier, F., Winter, G., Vidal, O., Mapping global greenhouse gases emissions: an interactive, open-access, web application. Available at:",
    className="border",
)


layout = dbc.Container(
    [
        dbc.Row([dbc.Col([dropdown], width=3), dbc.Col(html.Div("Select region"), width=9)], justify="center"),
        dbc.Row(
            [
                dbc.Col(
                    [graph],
                    width=12,
                    style={"height": 450},
                )
            ]
        ),
        html.Div(" "),
        dbc.Row([dbc.Col([slider])], justify="center"),
        citation,
        html.Div("\nYou may use your browser's zoom function for better readability."),
    ],
    fluid=True,
)


color_dict = dict(
    {
        "#8de5a1": "#0072ff",
        "#a1c9f4": "#00cafe",
        "#cfcfcf": "#b0ebff",
        "#debb9b": "#fff1b7",
        "#fab0e4": "#ffdc23",
        "#ff9f9b": "#ffb758",
        "#ffb482": "#ff8200",
    }
)


@app.callback(
    Output("graph2", "figure"),
    Input(PlaybackSliderAIO.ids.slider("bruh2"), "value"),
    Input("slct2", "value"),
)
@cache.memoize()
def fig_sankey_cap(year, region):
    """Builds sankey diagram for emissions per capita.

    Parameters
    ----------
    year : int
    region : string

    Returns
    -------
    fig : figure
    """

    norm = feather.read_feather(DATA_PATH.joinpath("norm_cap.feather"))  # Different norm in t/cap and Mt
    pop = feather.read_feather(DATA_PATH.joinpath("pop.feather"))

    ratio = norm.loc[region].loc[year]

    def node_y(nodes, node, white, color, region):
        """Assigns y position to node.

        Parameters
        ----------
        nodes : pd.DataFrame
            dataframe with all the nodes information
        node : string
            name of node whose y coordinate is wanted
        white : float
            share of the sankey's height which is white (0.3 means that 70% of the height will be filled with color)
        color : float
            1-white
        region : string

        Returns
        -------
        y_coordinate : float
        """
        if node == "CFC":
            node = "GCF"
        if node == "RoW - CFC":
            node = "RoW - GCF"
        if node == "CFCk":
            node = "GCF"
        if node == "RoW - CFCk":
            node = "RoW - GCF"
        if node == "Exports":
            node = "RoW - Health"
        if node == "CFC imports re-exported":
            node = "RoW - Food"
        if node == "Footprint":
            node = "Food"

        pos = nodes["position"].loc[node]
        df = nodes.reset_index().set_index(["position", "index"]).loc[pos]["value Mt"]

        if node in [
            "Households direct ",
            "Households ",
            "Government ",
            "NPISHS ",
            "Positive capital formation ",
        ]:
            df2 = (
                nodes.reset_index()
                .set_index(["position", "index"])
                .loc["8. cons"]["value Mt"]
                .loc[
                    [
                        "RoW - Mobility",
                        "RoW - Shelter",
                        "RoW - Food",
                        "RoW - Clothing",
                        "RoW - Education",
                        "RoW - Health",
                        "RoW - Other goods and services",
                        "RoW - Positive capital formation ",
                    ]
                ]
            )
            df = pd.concat([df.drop("Exports"), df2])

        if node in [
            "Africa",
            "Asia",
            "Europe",
            "Middle East",
            "North America",
            "Oceania",
            "South America",
        ]:
            df2 = (
                nodes.reset_index()
                .set_index(["position", "index"])
                .loc["8. cons"]["value Mt"]
                .loc[
                    [
                        i
                        for i in [
                            "Mobility",
                            "Shelter",
                            "Food",
                            "Clothing",
                            "Education",
                            "Health",
                            "Other goods and services",
                        ]
                        if i in nodes.index
                    ]
                ]
            )
            df = pd.concat([df, df2])
            df3 = (
                nodes.reset_index()
                .set_index(["position", "index"])
                .loc["7. cbaK"]["value Mt"]
                .loc["Positive capital formation "]
            )
            df.loc["Positive capital formation "] = df3

        if node in [
            "RoW - Mobility",
            "RoW - Shelter",
            "RoW - Food",
            "RoW - Clothing",
            "RoW - Education",
            "RoW - Health",
            "RoW - Other goods and services",
            "RoW - Positive capital formation ",
        ]:
            df3 = (
                nodes.reset_index()
                .set_index(["position", "index"])
                .loc["7. cbaK"]["value Mt"]
                .loc["Positive capital formation "]
            )
            df.loc["Positive capital formation "] = df3

        total = max(
            nodes.reset_index().set_index("position").loc["4. cba"]["value Mt"].sum(),
            nodes.reset_index().set_index("position").loc["7. cbaK"]["value Mt"].sum(),
        )
        if pos == "0. ges":
            df = df.reindex(["CO2", "CH4", "N2O", "SF6"])
        elif pos == "1. imp reg":
            df = df.reindex(
                pd.Index([REGIONS[region] + " "]).union(df.index.sort_values().drop(REGIONS[region] + " "), sort=False)
            )
        elif pos == "2. imp dom":
            df = df.reindex(["Territorial", "Imports"])
        elif pos == "3. pba":
            df = df.reindex(
                pd.Index(["Households direct   "])
                .union(
                    df.loc[df.index.str[:2] != "Ro"].index.drop("Households direct   "),
                    sort=False,
                )
                .union(df.loc[df.index.str[:2] == "Ro"].index, sort=False)
            )
        elif pos == "4. cba":
            df = df.reindex(
                [
                    "Households direct",
                    "Households",
                    "Government",
                    "NPISHS",
                    # "Positive capital formation",
                    "GCF",
                    "Negative capital formation",
                    "RoW - Negative capital formation",
                    "RoW - GCF",
                    "RoW - Households",
                    "RoW - Government",
                    "RoW - NPISHS",
                    # "RoW - Positive capital formation",
                ]
            )
        elif pos == "7. cbaK":
            df = df.reindex(
                [
                    "Households direct ",
                    "Households ",
                    "Government ",
                    "NPISHS ",
                    "Positive capital formation ",
                    # "RoW - Mobility",
                    # "RoW - Shelter",
                    # "RoW - Food",
                    "RoW - Clothing",
                    "RoW - Education",
                    "RoW - Health",
                    "RoW - Other goods and services",
                    "RoW - Positive capital formation ",
                ]
            )

        elif pos == "8. cons":
            df = df.reindex(
                [
                    i
                    for i in [
                        "Mobility",
                        "Shelter",
                        "Food",
                        "Clothing",
                        "Education",
                        "Health",
                        "Other goods and services",
                        "Positive capital formation ",
                        # "Households direct ",
                        "RoW - Mobility",
                        "RoW - Shelter",
                        "RoW - Food",
                        "RoW - Clothing",
                        "RoW - Education",
                        "RoW - Health",
                        "RoW - Other goods and services",
                        "RoW - Positive capital formation ",
                        # "CFC imports re-exported",
                    ]
                    if i in nodes.index
                ]
            )
        elif pos == "9. exp":
            df = df.reindex(
                [
                    i
                    for i in [
                        "Mobility",
                        "Shelter",
                        "Food",
                        "Clothing",
                        "Education",
                        "Health",
                        "Other goods and services",
                        "Positive capital formation ",
                        "Africa",
                        "Asia",
                        "Europe",
                        "Middle East",
                        "North America",
                        "Oceania",
                        "South America",
                    ]
                    if i in nodes.index
                ]
            )
        return (
            len(df.loc[:node]) / (len(df) + 1) * (1 - color * df.sum() / total)  # white
            + (df.loc[:node][:-1].sum() + df.loc[node] / 2) / total * color
        )

    def Nodes(region, year, height, top_margin, bottom_margin, pad, ratio):
        nodes = feather.read_feather(
            DATA_PATH.joinpath("Sankey_data/" + region + "/nodes" + region + str(year) + ".feather")
        )

        size = height - top_margin - bottom_margin
        n = max(nodes.reset_index().set_index("position").index.value_counts())
        n = 13
        pad2 = (size - ratio * (size - (n - 1) * pad)) / (n + 1)
        white = ((n + 1) * pad2) / size
        color = 1 - white

        nodes = nodes.assign(
            x=lambda d: d["position"].replace(
                dict(
                    zip(
                        [
                            "0. ges",
                            "1. imp reg",
                            "2. imp dom",
                            "3. pba",
                            "4. cba",
                            "5. ncf",
                            "6. endo",
                            "7. cbaK",
                            "8. cons",
                            "9. exp",
                        ],
                        (
                            [
                                0.00001,
                                0.095,  # 9.5
                                0.19,  # 9.5
                                0.285,  # 9.5
                                0.44,  # 15.5
                                0.52,  # 8
                                0.6,  # 8
                                0.68,  # 8
                                0.835,  # 15.5
                                1,  # 16.5
                            ]
                        ),
                    )
                )
            ),
            y=lambda d: [node_y(nodes, i, white, color, region) for i in d.index],
        )

        try:
            nodes.loc["CFC imports re-exported", "x"] = 0.68
        except KeyError:
            None

        try:
            nodes.loc["RoW - Negative capital formation", "x"] = 0.44
        except KeyError:
            None

        try:
            nodes.loc["Negative capital formation", "x"] = 0.44
        except KeyError:
            None

        nodes.loc["Footprint", "x"] = 1

        return nodes, pad2

    data_sankey = feather.read_feather(
        DATA_PATH.joinpath("Sankey_data/" + region + "/data" + region + str(year) + ".feather")
    ).replace(color_dict)
    node_list = feather.read_feather(
        DATA_PATH.joinpath("Sankey_data/" + region + "/nodelist" + region + str(year) + ".feather")
    )[0].values

    height = 480
    width = 1100
    top_margin = 30
    bottom_margin = 10
    left_margin = 10
    right_margin = 10
    pad = 10

    nodes, pad2 = Nodes(region, year, height, top_margin, bottom_margin, pad, ratio)

    link = dict(
        source=data_sankey["source"],
        target=data_sankey["target"],
        value=data_sankey["value"] * 1000000 / pop.loc[region].loc[year],
        label=list(str(x) + " tCO2eq/capita" for x in data_sankey["value"].astype(float).round(1)),
        color=data_sankey["color"],
        hovertemplate="",
    )

    node = {
        "label": (pd.DataFrame(nodes, index=node_list))["label t/cap"].replace(REGIONS).values,
        "pad": pad2,
        "thickness": 2,
        "color": "#00005A",  # ,#00008E, #0028dc
        "x": nodes["x"].values,
        "y": nodes["y"].values,
    }

    sankey = go.Sankey(link=link, node=node, valueformat=".0f", valuesuffix=" tCO2eq/capita", hoverinfo="none")  #

    fig = go.Figure(sankey)
    fig.update_layout(
        title=f"<b>Greenhouse gas footprint of {REGIONS[region]} in {year} (tCO2eq/capita)<b>",
        font=dict(size=10, color="black"),
        paper_bgcolor="white",
        title_x=0.5,
        font_family="Arial",
    )

    fig.update_traces(
        legendrank=10,
    )

    fig.update_layout(
        autosize=False,
        width=width,
        height=height,
        margin=dict(l=left_margin, r=right_margin, t=top_margin, b=bottom_margin),
    )

    return fig
