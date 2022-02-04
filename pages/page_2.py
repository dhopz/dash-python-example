import dash

from dash.dependencies import Input, Output, State
from dash import dcc, html
from dash.exceptions import PreventUpdate
import random


from app import app

layout = html.Div([
    # The memory store reverts to the default on every page refresh
    #dcc.Store(id='memory'),
    # The local store will take the initial data
    # only the first time the page is loaded
    # and keep it until it is cleared.
    dcc.Store(id='local', storage_type='local'),
    # Same as the local store but will lose the data
    # when the browser/tab closes.
    #dcc.Store(id='session', storage_type='session'),
    html.Table([
        html.Thead([
            html.Tr(html.Th('Click to store in:', colSpan="3")),
            html.Tr([
                #html.Th(html.Button('memory', id='memory-button')),
                html.Th(html.Button('localStorage', id='local-button')),
                #html.Th(html.Button('sessionStorage', id='session-button'))
            ]),
            html.Tr([
                #html.Th('Memory clicks'),
                html.Th('Local clicks'),
                #html.Th('Session clicks')
            ])
        ]),
        html.Tbody([
            html.Tr([
                #html.Td(0, id='memory-clicks'),
                html.Td(0, id='local-clicks'),
                #html.Td(0, id='session-clicks')
            ])
        ])
    ])
])

store = 'local'

# @app.callback(Output('local', 'data'),
#                 Input('local-button', 'n_clicks'),
#                 State('local', 'data'))
# def on_click(n_clicks, data):
#     if n_clicks is None:        
#         raise PreventUpdate
#     # Give a default data dict with 0 clicks if there's no data.
#     #data = data or {'clicks': 0}
#     print("this puts data in local storage")
#     #data['clicks'] = data['clicks'] + 1
#     data = {"random_x":10,"random_y":random.randint(1,21),"size":random.randint(1,50),"color":random.choice(["a","b","c"])}
#     return data

# output the stored clicks in the table cell.
@app.callback(Output('local-clicks', 'children'),                
                Input('local', 'modified_timestamp'),
                State('local', 'data'))
def on_data(ts, data):
    #print(ts, data)
    #print({"random_x":15,"random_y":random.randint(1,21),"size":random.randint(1,50),"color":random.choice(["a","b","c"])})
    # if ts is None:
    #     raise PreventUpdate

    data = data or {}
    #print(data)

    #return data.get('random_x', 0)
    return "" if data.get('random_x', 0) == None else f"The all-important value driving our business decisions is {data.get('random_x', 0)+5}"



