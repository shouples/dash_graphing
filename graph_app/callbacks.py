from dash.dependencies import Input, Output, State

import dash
import pprint
import uuid


def register_callbacks(app):

    @app.callback(
        Output('debug-info', 'children'),
        [
            Input('graph', 'selectedNodeData'),
            Input('graph', 'selectedEdgeData'),
            Input('graph', 'elements'),
            Input('new-node-btn', 'n_clicks'),
        ],
    )
    def show_debug(nodes, edges, elements, clicks):
        out = f"""
trigger:
{triggered_component()} ({triggered_property()})


all nodes:
{pprint.pformat(elements)}
-------
selected nodes:
{pprint.pformat(nodes)}
-------
selected edges:
{pprint.pformat(edges)}
-------
"""
        return out


    @app.callback(
        [
            Output('selected-nodes', 'children'),
            Output('selected-nodes-collapse', 'is_open'),
        ],
        Input('graph', 'selectedNodeData')
    )
    def show_selected(nodes):
        if not nodes:
            return '', False
        node_list = [data['label'] for data in nodes]
        edge_preview = "-->".join([
            f"({n})" for n in node_list
        ])
        return edge_preview, True

    @app.callback(
        Output('graph', 'stylesheet'),
        [
            Input('new-node-btn', 'n_clicks'),
            Input('update-node-btn', 'n_clicks'),
            Input('new-edge-btn', 'n_clicks'),
            Input('update-edge-btn', 'n_clicks'),
            Input('new-node-type-btn', 'n_clicks'),
        ],
        State('graph', 'stylesheet'),
    )
    def update_stylesheet(new_node, update_node, new_edge, update_edge, new_node_type, stylesheet):
        stylesheet = stylesheet or [
            {
                'selector': 'edge',
                'style': {
                    'label': 'data(label)',
                    'source-arrow-shape': 'triangle',
                }
            },
            {
                'selector': 'node',
                'style': {
                    'label': 'data(label)',

                }
            }
        ]
        return stylesheet


    @app.callback(
        [
            Output('graph', 'elements'),
            Output('action-feedback', 'children'),
        ],
        [
            Input('new-node-btn', 'n_clicks'),
            Input('update-node-btn', 'n_clicks'),
            Input('delete-node-btn', 'n_clicks'),
            Input('new-edge-btn', 'n_clicks'),
            Input('update-edge-btn', 'n_clicks'),
            Input('delete-edge-btn', 'n_clicks'),
        ],
        [
            State('graph', 'elements'),
            State('graph', 'selectedNodeData'),
            State('graph', 'selectedEdgeData'),
            State('node-name', 'value'),
            State('node-type', 'value'),
            State('edge-name', 'value'),
            State('edge-type', 'value'),
        ]
    )
    def update_graph_elements(new_node, update_node, delete_node, new_edge, update_edge, delete_edge, elements, selected_nodes, selected_edges, node_name, node_type, edge_name, edge_type):
        elements = elements or []

        trigger = triggered_component()

        if 'new-node-btn' in trigger:
            elements.append(
                {
                    'data': {
                        'id': str(uuid.uuid1()), 
                        'label': node_name
                    },
                    'classes': node_type,
                }
            )

        if 'new-edge-btn' in trigger:
            if selected_nodes:
                selected_node_labels = [n['id'] for n in selected_nodes]
                for i, node in enumerate(selected_node_labels):
                    if len(selected_node_labels) == i+1:
                        break
                    elements.append(
                        {
                            'data': {
                                'source': node, 
                                'target': selected_node_labels[i+1],
                                'label': edge_name,
                            },
                            'classes': edge_type,
                        }
                    )

        if 'delete-node-btn' in trigger:
            selected_node_ids = [n['id'] for n in selected_nodes]
            elements = [
                e for e in elements
                if e['data']['id'] not in selected_node_ids
            ]

        if 'delete-edge-btn' in trigger:
            selected_edge_ids = [e['id'] for e in selected_edges]
            elements = [
                e for e in elements
                if e['data']['id'] not in selected_edge_ids
            ]

        return elements, f"{triggered_component()} ({triggered_property()})"

    @app.callback(
        Output('new-node-type-collapse', 'is_open'),
        Input('expand-node-type', 'n_clicks'),
        State('new-node-type-collapse', 'is_open'),
        prevent_initial_call=True,
    )
    def toggle_new_node_type(clicks, is_open):
        return not is_open


def triggered_component():
    return dash.callback_context.triggered[0]['prop_id'].split(".")[0]

def triggered_property():
    return dash.callback_context.triggered[0]['prop_id'].split(".")[1]