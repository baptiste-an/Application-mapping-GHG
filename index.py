from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash_auth import BasicAuth
import os
import dash_bootstrap_components as dbc

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import app_sankey, app_sankey_per_capita, doc

# VALID_USERNAME_PASSWORD_PAIRS = [["hello", "world"]]
# auth = BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)

thanks = html.Div(
    html.P(
        [
            "Graciously hosted by ",
            html.A(
                "scalingo",
                href="https://scalingo.com?utm_source=referral&utm_medium=website-footer&utm_campaign=shiftproject",
                target="_blank",
            ),
            " in 🇫🇷",
        ]
    ),
    id="thanks",
    # justify="right",
)

app.layout = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(
                    label="EMISSIONS PER CAPITA",
                    tab_id="tab-1",
                    active_label_style={"color": "#FF8200"},
                    # label_style={"color": "#00005A"},
                ),
                dbc.Tab(
                    label="TOTAL EMISSIONS",
                    tab_id="tab-2",
                    active_label_style={"color": "#FF8200"},
                    # label_style={"color": "#00005A"},
                ),
                dbc.Tab(
                    label="DOCUMENTATION AND DOWNLOADS",
                    tab_id="tab-3",
                    active_label_style={"color": "#FF8200"},
                    # label_style={"color": "#00005A"},
                ),
            ],
            id="tabs",
            active_tab="tab-1",
        ),
        html.Div(id="content"),
        html.Div(thanks),
    ]
)


@app.callback(Output("content", "children"), [Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "tab-1":
        return app_sankey_per_capita.layout
    elif at == "tab-2":
        return app_sankey.layout
    elif at == "tab-3":
        return doc.layout


# for deployment:
if __name__ == "__main__":
    port = int(os.getenv("PORT", "8050"))
    app.run(debug=False, host="0.0.0.0", port=port)
