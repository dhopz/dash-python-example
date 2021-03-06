### Import Packages ###
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

### Import Dash Instance and Pages ###
from app import app
from pages import page_1
from pages import page_2

# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "11rem",
    "padding": "2rem 1rem",
    "background-color": "rgba(177,73,207,255)",
    "text-color":"black"
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "12rem",
    "margin-right": "2rem",
    "padding": "1rem 1rem",
    #"backgroundColor": "#db9ff7",
}

sidebar = html.Div(
    [
        html.H2(html.Img(src=app.get_asset_url('m.png'),height="150px")),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact", className="page-link"),
                dbc.NavLink("Page 1", href="/page-1", active="exact", className="page-link"),
                dbc.NavLink("Page 2", href="/page-2", active="exact", className="page-link"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
    #className="navbar navbar-default"
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])

def render_page_content(pathname):
    if pathname == "/":
        return page_1.layout
    elif pathname == "/page-1":
        return page_2.layout
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")
    # If the user tries to reach a different page, return a 404 message
    else:
        return '404'
    
