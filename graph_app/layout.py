from dash import dcc, html

import dash_bootstrap_components as dbc
import dash_cytoscape as cyto


cyto.load_extra_layouts()
cyto_fig = cyto.Cytoscape(
    id='graph',
    layout={'name': 'cose', 'animate': True},
    style={'width': '100%', 'height': '800px'},
    elements=[]
)

node_types = ['person', 'car', 'food']
new_node_type = dbc.Alert(
    children=[
        dbc.FormText("Type Name"),
        dbc.Input(id='node-type-name'),
        dbc.FormText("Type Color"),
        dbc.Input(type='color', id='node-type-color'),
        dbc.FormText("Type Shape"),
        dcc.Dropdown(
            id='node-type-shape',
            options=[
                {'label': v, 'value': v} 
                for v in ['circle', 'triangle', 'square']
            ],
            value='circle',
        ),
        dbc.Button(
            "Save Type",
            id='new-node-type-btn',
            color='primary',
            outline=True,
            size='sm',
            className='mt-2'
        ),
        dbc.Button(
            "Delete Type",
            id='delete-node-type-btn',
            color='danger',
            outline=True,
            size='sm',
            className='mt-2 ml-2'
        ),
    ],
    color='light',
    className='mt-2',
)

node_options = html.Div(
    children=[
        html.H5("Nodes"),

        dbc.FormText("Name"),
        dbc.Input(
            id='node-name',
            placeholder="my_node",
            className='mb-2',
        ),
        
        dbc.FormText("Type"),
        dbc.InputGroup(
            children=[
                dbc.Select(
                    id='node-type',
                    options=[{'label': v, 'value': v} for v in node_types],
                    value='person',
                ),
                dbc.Button(
                    html.I(className="fa fa-plus-circle"),
                    id='expand-node-type',
                    color='primary',
                    outline=True,
                )
            ],
        ),
        dbc.Collapse(
            new_node_type,
            id='new-node-type-collapse',
        ),
        dbc.Button(
            "Create New", 
            id='new-node-btn',
            color='success', 
            #size='sm',
            outline=False, 
            className='my-3',
        ),
        dbc.Button(
            "Update", 
            id='update-node-btn',
            color='secondary', 
            #size='sm',
            outline=False, 
            className='my-3 ml-4',
        ),
        dbc.Button(
            "Delete", 
            id='delete-node-btn',
            color='danger', 
            #size='sm',
            outline=False, 
            className='my-3 ml-4',
        ),
    ],
)

edge_types = ['A', 'B', 'C', '???']
edge_options = html.Div(
    children=[
        html.H5("Edges"),
        dbc.Collapse(
            dbc.Alert(
                children=[
                    dbc.FormText("Selected nodes:"),
                    html.Pre(id="selected-nodes", style={'marginBottom': 0}),
                ],
                color='light',
                className='mt-2',
            ),
            id='selected-nodes-collapse',
        ),
        dbc.InputGroup(
            children=[
                dbc.InputGroupText("Name"),
                dbc.Input(
                    id='edge-name',
                    placeholder="my_edge"
                ),
            ],
            className='mt-2',
        ),
        dbc.InputGroup(
            children=[
                dbc.InputGroupText("Type"),
                dbc.Select(
                    id='edge-type',
                    options=[{'label': v, 'value': v} for v in edge_types],
                    value='A',
                ),
            ],
            className='mt-2',
        ),
        dbc.Button(
            "Create New", 
            id='new-edge-btn',
            color='success', 
            #size='sm',
            outline=False, 
            className='my-3',
        ),
        dbc.Button(
            "Update", 
            id='update-edge-btn',
            color='secondary', 
            #size='sm',
            outline=False, 
            className='my-3 ml-2',
        ),
        dbc.Button(
            "Delete", 
            id='delete-edge-btn',
            color='danger', 
            #size='sm',
            outline=False, 
            className='my-3 ml-2',
        ),
    ],
)

debug = dbc.Alert(
    html.Pre(id='debug-info'),
    color='info',
    className='my-5',
    style={
        'height': '300px',
        'overflow-y': 'scroll'
    }
)

LAYOUT = html.Div(
    children=[
        html.H1("Graph Testing", className='mb-4'),
        dbc.Row([
            dbc.Col(
                dbc.Card(cyto_fig), 
                width=8
            ),
            dbc.Col(
                children=[
                    dbc.Card(node_options, body=True, className='mb-3'), 
                    dbc.Card(edge_options, body=True, className='mb-3'), 
                    dbc.Card(html.Pre(id='action-feedback'), body=True),
                ],
                width=4,
                style={
                    'height': '800px',
                    'overflow-y': 'auto'
                }
            ),
        ]),
        debug,
    ],
    className="m-4",
)