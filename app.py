import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
from dash import html
import plotly.graph_objects as go
import random
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

app = dash.Dash(suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP], title='Mindful Data')

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

markdown_text = '''
# Dash Data Visualisation
# '''

random_x = [random.randint(1,1000) for i in range(20)]
random_y = [i for i in range(1,21)]
size = [random.randint(1,50) for i in range(20)]
color_list = ['x','y','z']
color = [random.choice(color_list) for i in range(20)]
data_list = {"random_x":random_x,"random_y":random_y,"size":size,"color":color}
df = pd.DataFrame(data_list, columns =['random_x','random_y','size','color'])

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

# Create home page layout to display data when server starts
home_page_layout = html.Div([   
    dcc.Markdown(children=markdown_text, id="markdown_div", className="header_div"),
    html.Br(),  
    dash_table.DataTable(
        id='adding-rows-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        editable=True,
        row_deletable=True,
        page_size=5,
        page_action='none',
        style_table={'height': '180px', 'overflowY': 'auto'}
    ),
    html.Br(), 
    html.Div(dcc.Input(id='input-on-submit', type='number', min=2, max=1000, step=1)),
    html.Button('Submit', id='editing-rows-button', className = "submit-button", n_clicks=0),    
    html.Div(id='container-button-basic', children='Enter a value and press submit', className="report-section"),
    dcc.Graph(id='adding-rows-graph')
])

@app.callback(
    Output('adding-rows-table', 'data'),
    Input('editing-rows-button', 'n_clicks'),  
    [State('adding-rows-table', 'data'),
    State('input-on-submit', 'value')])
def add_row(n_clicks, rows, value):    
    if n_clicks > 0:
        #print({"random_x":value,"random_y":random.randint(1,100),"size":random.randint(1,100),"color":"w"})
        rows.append({"random_x":value,"random_y":random.randint(1,21),"size":random.randint(1,50),"color":random.choice(["a","b","c"])})
    return rows

@app.callback(
    Output('container-button-basic', 'children'),
    Input('editing-rows-button', 'n_clicks'),
    State('input-on-submit', 'value'))
def update_output(n_clicks, value):
    if n_clicks > 0:
    #print(value)
    #rows.append({"random_x":random.randint(1,100),"random_y":random.randint(1,21),"size":random.randint(1,50),"color":random.choice(["a","b","c"])}) 
        return "" if value == None else f"The all-important value driving our business decisions is {value+5}"

@app.callback(
    Output('adding-rows-graph', 'figure'),
    Input('adding-rows-table', 'data'))
    # Input('adding-rows-table', 'columns'))
def display_output(rows):   
    fig = px.scatter(rows, 
        x="random_x", 
        y="random_y",
        size="size",
        color="color",
        log_x=True, size_max=50)

    return fig

def render_page_content(pathname):
    if pathname == "/":
        return home_page_layout
    elif pathname == "/page-1":
        return page_1_layout
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

if __name__ == '__main__':
    app.run_server(debug=True)