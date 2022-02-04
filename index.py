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

### Page container ###
# page_container = html.Div(
#     children=[
#         # represents the URL bar, doesn't render anything
#         dcc.Location(
#             id='url',
#             refresh=False,
#         ),
#         # content will be rendered in this element
#         html.Div(id='page-content')
#     ]
# )

### Set app layout to page container ###
# app.layout = page_container

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
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

# ### Index Page Layout ###
# index_layout = html.Div(
#     children=[
#         dcc.Link(
#             children='Go to Page 1',
#             href='/page-1',
#         ),
#         html.Br(),
#         dcc.Link(
#             children='Go to Page 2',
#             href='/page-2',
#         ),
#     ]
# )

# ### Assemble all layouts ###
# app.validation_layout = html.Div(
#     children = [
#         page_container,
#         index_layout,
#         page_1.layout,
#         page_2.layout,
#     ]
# )

# ### Update Page Container ###
# @app.callback(
#     Output(
#         component_id='page-content',
#         component_property='children',
#         ),
#     [Input(
#         component_id='url',
#         component_property='pathname',
#         )]
# )
# def display_page(pathname):
#     if pathname == '/':
#         return index_layout
#     elif pathname == '/page-1':
#         return page_1.layout
#     elif pathname == '/page-2':
#         return page_2.layout
#     else:
#         return '404'
