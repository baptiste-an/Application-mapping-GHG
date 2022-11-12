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
import os 
import json
from flask_caching import Cache

class PlaybackSliderAIO(html.Div):
    class ids:
        play = lambda aio_id: {
            "component": "PlaybackSliderAIO",
            "subcomponent": "button",
            "aio_id": aio_id,
        }
        play_icon = lambda aio_id: {
            "component": "PlaybackSliderAIO",
            "subcomponent": "i",
            "aio_id": aio_id,
        }
        slider = lambda aio_id: {
            "component": "PlaybackSliderAIO",
            "subcomponent": "slider",
            "aio_id": aio_id,
        }
        interval = lambda aio_id: {
            "component": "PlaybackSliderAIO",
            "subcomponent": "interval",
            "aio_id": aio_id,
        }

    ids = ids

    def __init__(self, button_props=None, slider_props=None, interval_props=None, aio_id=None):
        if aio_id is None:
            aio_id = str(uuid.uuid4())

        button_props = button_props.copy() if button_props else {}
        slider_props = slider_props.copy() if slider_props else {}
        interval_props = interval_props.copy() if interval_props else {}

        button_props["active"] = False

        super().__init__(
            [
                dbc.Button(html.I(id=self.ids.play_icon(aio_id)), id=self.ids.play(aio_id), **button_props),
                dcc.Slider(id=self.ids.slider(aio_id), **slider_props),
                dcc.Interval(id=self.ids.interval(aio_id), **interval_props),
            ]
        )

    @callback(
        Output(ids.play(MATCH), "active"),
        Output(ids.play_icon(MATCH), "className"),
        Output(ids.interval(MATCH), "disabled"),
        Input(ids.play(MATCH), "n_clicks"),
        State(ids.play(MATCH), "active"),
    )

    def toggle_play(clicks, curr_status):
        if clicks:
            text = "fa-solid fa-play" if curr_status else "fa-solid fa-pause"
            return not curr_status, text, curr_status
        return curr_status, "fa-solid fa-play", not curr_status

    @callback(
        Output(ids.slider(MATCH), "value"),
        Input(ids.play(MATCH), "active"),
        Input(ids.interval(MATCH), "n_intervals"),
        State(ids.slider(MATCH), "min"),
        State(ids.slider(MATCH), "max"),
        State(ids.slider(MATCH), "step"),
        State(ids.slider(MATCH), "value"),
    )
    def start_playback(play, interval, min, max, step, value):
        if not play:
            raise PreventUpdate

        new_val = value + step
        if new_val > max:
            new_val = min

        return new_val


VALID_USERNAME_PASSWORD_PAIRS = [["hello", "world"]]
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])

cache = Cache(app.server, config={
    'CACHE_TYPE': 'FileSystemCache',
    'CACHE_DIR': 'cache'
})

auth = BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)

DATA_PATH = pathlib.Path(__file__).parent.joinpath("data").resolve()

REGIONS={}

with open(f"{DATA_PATH}/regions.json") as f:
    REGIONS = json.loads(f.read())

LABELS=[ { 'label': v, 'value': k } for k, v in REGIONS.items() ]
 
app.layout = html.Div(
    [
        # html.H4(""),
        # html.P("region"),
        dcc.Dropdown(
            id="slct",
            # options=[dict(zip(df['region'],df['full name']))],
            options=LABELS,
            multi=False,
            value="CN",
            style={"width": "40%"},
        ),
        dcc.Graph(id="graph", responsive=False),
        # html.P("year"),
        PlaybackSliderAIO(
            aio_id="bruh",
            slider_props={
                "min": 1995,
                "max": 2019,  # 2019
                "step": 1,
                "value": 1995,
                "marks": {str(year): str(year) for year in range(1995, 2020, 1)},  # 2020
            },
            button_props={"className": "float-left"},
            interval_props={"interval": 2000},
        ),
        html.Div(
            html.P([
                "Graciously hosted by ",
                html.A("scalingo", href="https://scalingo.com"),
                " in 🇫🇷"
            ]), 
            id="thanks",
        ),
    ]
)


@app.callback(
    Output("graph", "figure"),
    # Output("text", "children"),
    Input(PlaybackSliderAIO.ids.slider("bruh"), "value"),
    Input("slct", "value"),
)
@cache.memoize()
def fig_sankey(year, region):
    norm = feather.read_feather("norm.feather")
    ratio = norm.loc[region].loc[year]

    def node_y(nodes, node, white, color, region):
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
            node = "RoW - Mobility"

        pos = nodes["position"].loc[node]
        df = nodes.reset_index().set_index(["position", "index"]).loc[pos]["value Mt"]

        if node in [
            "Households direct ",
            "Households ",
            "Government ",
            "NPISHS ",
            "Net capital formation ",
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
                        "RoW - Net capital formation ",
                        # "CFC imports re-exported",
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
                .loc["Net capital formation "]
            )
            df.loc["Net capital formation "] = df3

        if node in [
            "RoW - Mobility",
            "RoW - Shelter",
            "RoW - Food",
            "RoW - Clothing",
            "RoW - Education",
            "RoW - Health",
            "RoW - Other goods and services",
            "RoW - Net capital formation ",
            # "CFC imports re-exported",
        ]:
            df3 = (
                nodes.reset_index()
                .set_index(["position", "index"])
                .loc["7. cbaK"]["value Mt"]
                .loc["Net capital formation "]
            )
            df.loc["Net capital formation "] = df3

        total = max(
            nodes.reset_index().set_index("position").loc["4. cba"]["value Mt"].sum(),
            nodes.reset_index().set_index("position").loc["7. cbaK"]["value Mt"].sum(),
        )
        if pos == "0. ges":
            df = df.reindex(["CO2", "CH4", "N2O", "SF6"])
        elif pos == "1. imp reg":
            df = df.reindex(pd.Index([region + " "]).union(df.index.sort_values().drop(region + " "), sort=False))
        elif pos == "2. imp dom":
            df = df.reindex(["Territorial", "Imports"])
        elif pos == "3. pba":
            df = df.reindex(
                pd.Index(["Households direct emissions"])
                .union(
                    df.loc[df.index.str[:2] != "Ro"].index.drop("Households direct emissions"),
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
                    "Net capital formation",
                    # "Consumption of fixed capital",
                    "GCF",
                    "Negative capital formation",
                    "RoW - Negative capital formation",
                    "RoW - GCF",
                    "RoW - Households",
                    "RoW - Government",
                    "RoW - NPISHS",
                    "RoW - Net capital formation",
                    # "RoW - Consumption of fixed capital ",
                ]
            )
        elif pos == "7. cbaK":
            df = df.reindex(
                [
                    "Households direct ",
                    "Households ",
                    "Government ",
                    "NPISHS ",
                    "Net capital formation ",
                    # "Exports",
                    "RoW - Mobility",
                    "RoW - Shelter",
                    "RoW - Food",
                    "RoW - Clothing",
                    "RoW - Education",
                    "RoW - Health",
                    "RoW - Other goods and services",
                    "RoW - Net capital formation ",
                    # "CFC imports re-exported",
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
                        "Net capital formation ",
                        "RoW - Mobility",
                        "RoW - Shelter",
                        "RoW - Food",
                        "RoW - Clothing",
                        "RoW - Education",
                        "RoW - Health",
                        "RoW - Other goods and services",
                        "RoW - Net capital formation ",
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
                        "Net capital formation ",
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
            len(df.loc[:node]) / (len(df) + 1) * (1 - color * df.sum() / total)
            + (df.loc[:node][:-1].sum() + df.loc[node] / 2) / total * color
        )

    def Nodes(region, year, height, top_margin, bottom_margin, pad, ratio):

        nodes = feather.read_feather(
            DATA_PATH.joinpath("Sankeys/" + region + "/nodes" + region + str(year) + ".feather")
        )

        # ratio = 1
        size = height - top_margin - bottom_margin
        n = max(nodes.reset_index().set_index("position").index.value_counts())
        pad2 = (size - ratio * (size - (n + 1) * pad)) / (n + 1)
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
                                0.001,
                                0.05,
                                0.14,
                                0.21,
                                0.33,
                                0.47,
                                0.58,
                                0.7,
                                0.9,
                                0.999,
                            ]
                        ),
                    )
                )
            ),
            y=lambda d: [node_y(nodes, i, white, color, region) for i in d.index],
        )

        nodes.loc["x", "Exports"] = 0.65
        try:
            nodes.loc["x", "CFC imports re-exported"] = 0.65
        except KeyError:
            None

        try:
            nodes.loc["x", "RoW - Negative capital formation"] = 0.38
        except KeyError:
            None

        try:
            nodes.loc["x", "Negative capital formation"] = 0.38
        except KeyError:
            None
        # nodes["x"].loc[["CFC","RoW - CFC"]] = 0.76
        # nodes["x"].loc[["CFCk","RoW - CFCk"]] = 0.76

        nodes.loc["x", 
            [
                "RoW - Mobility",
                "RoW - Shelter",
                "RoW - Food",
                "RoW - Clothing",
                "RoW - Education",
                "RoW - Health",
                "RoW - Other goods and services",
                "RoW - Net capital formation ",
            ]
        ] = 0.77
        return nodes, pad2

    norm = feather.read_feather(DATA_PATH.joinpath("norm.feather"))
    data_sankey = feather.read_feather(
        DATA_PATH.joinpath("Sankeys/" + region + "/data" + region + str(year) + ".feather")
    )
    node_list = feather.read_feather(
        DATA_PATH.joinpath("Sankeys/" + region + "/nodelist" + region + str(year) + ".feather")
    )[0].values

    height = 450
    width = 1100
    top_margin = 50
    bottom_margin = 0
    left_margin = 50
    right_margin = 50
    pad = 10

    nodes, pad2 = Nodes(region, year, height, top_margin, bottom_margin, pad, ratio)
    # node_dict, node_list, data_sankey = data_Sankey(year, region)

    link = dict(
        source=data_sankey["source"],
        target=data_sankey["target"],
        value=data_sankey["value"],
        label=list(str(x) + " Mt CO2 eq" for x in data_sankey["value"].astype(float).round(1)),
        color=data_sankey["color"],
        hovertemplate="",
    )

    node = {
        # "label": pd.DataFrame(node_list)[0],
        "label": (pd.DataFrame(nodes, index=node_list))["label t/cap"].replace(REGIONS).values,
        "pad": pad2,
        "thickness": 5,
        "color": "gray",
        "x": nodes["x"].values,
        "y": nodes["y"].values,
    }

    sankey = go.Sankey(
        link=link,
        node=node,  #
        valueformat=".0f",
        valuesuffix=" Mt CO2eq",
        # arrangement="snap",
    )

    fig = go.Figure(sankey)
    fig.update_layout(
        hovermode="y",
        title=f"Greenhouse gas footprint of {REGIONS[region]} for {year} (Mt CO2eq)",
        font=dict(size=8, color="black"),
        paper_bgcolor="white",
    )

    fig.update_traces(
        legendrank=10,
        node_hoverinfo="all",
        hoverlabel=dict(align="left", bgcolor="white", bordercolor="black"),
    )

    fig.update_layout(
        autosize=False,
        width=width,
        height=height,
        margin=dict(l=left_margin, r=right_margin, t=top_margin, b=bottom_margin),
    )

    # fig.update_traces(textfont_size=7)
    # fig.write_image(
    #     "Sankeys/" + region + "/fig2" + region + str(year) + ".pdf", engine="orca"
    # )
    # # fig.write_image("SankeyFR" + str(year) + ".svg", engine="orca")

    return fig


# app.run_server(debug=False)
server = app.server

if __name__ == "__main__":
    port=int(os.getenv("PORT", "8050"))
    app.run_server(debug=True, host="0.0.0.0", port=port)
