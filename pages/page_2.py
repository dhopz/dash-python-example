import dash

import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
import random


from app import app

layout = html.Div([
    # The memory store reverts to the default on every page refresh
    dcc.Store(id='memory'),
    # The local store will take the initial data
    # only the first time the page is loaded
    # and keep it until it is cleared.
    dcc.Store(id='local', storage_type='local'),
    # Same as the local store but will lose the data
    # when the browser/tab closes.
    dcc.Store(id='session', storage_type='session'),
    html.Table([
        html.Thead([
            html.Tr(html.Th('Click to store in:', colSpan="3")),
            html.Tr([
                html.Th(html.Button('memory', id='memory-button')),
                html.Th(html.Button('localStorage', id='local-button')),
                html.Th(html.Button('sessionStorage', id='session-button'))
            ]),
            html.Tr([
                html.Th('Memory clicks'),
                html.Th('Local clicks'),
                html.Th('Session clicks')
            ])
        ]),
        html.Tbody([
            html.Tr([
                html.Td(0, id='memory-clicks'),
                html.Td(0, id='local-clicks'),
                html.Td(0, id='session-clicks')
            ])
        ])
    ])
])

store = 'local'

# Create two callback for every store.
#for store in ('memory', 'local', 'session'):

# add a click to the appropriate store.
@app.callback(Output(store, 'data'),
                Input('{}-button'.format(store), 'n_clicks'),
                State(store, 'data'))
def on_click(n_clicks, data):
    if n_clicks is None:
        # prevent the None callbacks is important with the store component.
        # you don't want to update the store for nothing.
        raise PreventUpdate

    # Give a default data dict with 0 clicks if there's no data.
    data = data or {'clicks': 0}

    #data['clicks'] = data['clicks'] + 1
    data = {"random_x":17,"random_y":random.randint(1,21),"size":random.randint(1,50),"color":random.choice(["a","b","c"])}
    return data

# output the stored clicks in the table cell.
@app.callback(Output('{}-clicks'.format(store), 'children'),
                # Since we use the data prop in an output,
                # we cannot get the initial data on load with the data prop.
                # To counter this, you can use the modified_timestamp
                # as Input and the data as State.
                # This limitation is due to the initial None callbacks
                # https://github.com/plotly/dash-renderer/pull/81
                Input(store, 'modified_timestamp'),
                State(store, 'data'))
def on_data(ts, data):
    print(ts, data)
    #print({"random_x":15,"random_y":random.randint(1,21),"size":random.randint(1,50),"color":random.choice(["a","b","c"])})
    if ts is None:
        raise PreventUpdate

    data = data or {}
    #print(data)

    return data.get('random_x', 0)



