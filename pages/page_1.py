import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
from dash import html
import random
import plotly.express as px
import pandas as pd
from dash.exceptions import PreventUpdate


from app import app

markdown_text = '''
# Dash Data Visualisation
# '''

### Dummy Dataframe for Data Viz
random_x = [random.randint(1,1000) for i in range(20)]
random_y = [i for i in range(1,21)]
size = [random.randint(1,50) for i in range(20)]
color_list = ['x','y','z']
color = [random.choice(color_list) for i in range(20)]
data_list = {"random_x":random_x,"random_y":random_y,"size":size,"color":color}
df = pd.DataFrame(data_list, columns =['random_x','random_y','size','color'])

# Create home page layout to display data when server starts
layout = html.Div([   
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
    dcc.Store(id='local', storage_type='local'),
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
    #State('local', 'data')])
def add_row(n_clicks, rows, value): 
    #print(data, "local storage")   
    if n_clicks > 0:
        rows.append({"random_x":value,"random_y":random.randint(1,21),"size":random.randint(1,50),"color":random.choice(["a","b","c"])})
    return rows

@app.callback(
    Output('container-button-basic', 'children'),
    Input('editing-rows-button', 'n_clicks'),
    [State('input-on-submit', 'value'),
    State('local', 'data')])
def update_output(n_clicks, value, data):
    if n_clicks > 0:
        return "" if value == None else f"The all-important value driving our business decisions is {value+5}"
    else:
        return f"From previous input {data['random_x']}, the all-important value driving our business decisions is {data['random_x']+5}"
@app.callback(
    Output('adding-rows-graph', 'figure'),
    Input('adding-rows-table', 'data'))
def display_output(rows):   
    fig = px.scatter(rows, 
        x="random_x", 
        y="random_y",
        size="size",
        color="color",
        log_x=True, size_max=50)

    return fig

@app.callback(
    Output('local', 'data'),
    Input('editing-rows-button', 'n_clicks'),
    [State('local', 'data'),
    State('input-on-submit', 'value')])
def on_click(n_clicks, data, value):
    print(value)
    if n_clicks is None:        
        raise PreventUpdate
    # Give a default data dict with 0 clicks if there's no data.
    #data = data or {'clicks': 0}
    print("this puts data in local storage")
    #data['clicks'] = data['clicks'] + 1
    data = {"random_x":value,"random_y":random.randint(1,21),"size":random.randint(1,50),"color":random.choice(["a","b","c"])}
    print(data)
    return data