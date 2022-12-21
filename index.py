import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_auth import BasicAuth

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import app_sankey, app_sankey_per_capita

VALID_USERNAME_PASSWORD_PAIRS = [["hello", "world"]]
auth = BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(
            [
                dcc.Link("Sankey | ", href="/apps/app_sankey"),
                dcc.Link("Sankey per capita", href="/apps/app_sankey_per_capita"),
            ],
            className="row",
        ),
        html.Div(id="page-content", children=[]),
    ]
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/apps/app_sankey":
        return app_sankey.layout
    if pathname == "/apps/app_sankey_per_capita":
        return app_sankey_per_capita.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == "__main__":
    app.run_server(debug=False)
