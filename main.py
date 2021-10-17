"""Importing Libraries"""
import base64
import io

# import numpy as np
import pandas as pd
# import dash
from dash import html, dcc, dash_table, no_update, Dash
# import dash_bootstrap_components as dbc
# import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import plotly.express as px
from flask import Flask

# %%

# app = dash.Dash(__name__)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
server = Flask(__name__)
app = Dash(external_stylesheets=external_stylesheets, server=server)

# %%

# data = pd.read_csv("./data/rf-0917-FinalRecDB-rms", delimiter="\s+")

# %%
# available_cols = ["DRIFTA", "DRIFTB", "ZSTART", "ZDEPLOY", "ZPICKUP", "NHITS"]

# %%

app.layout = html.Div(style={
    'backgroundColor': 'White',
    'columnCount': 1
},
    children=[
        dcc.Store(
            id='csv-data',
            storage_type='session',
            data=None,
        ),

        dcc.Upload(
            id='data-table-upload',
            children=html.Div(
                [
                    html.Button('Upload File')
                ],
                style={
                    # 'width': '49%',
                    # 'height': "30px", 'borderWidth': '1px',
                    # 'borderRadius': '5px',
                    'textAlign': 'center',
                }
            ),
            multiple=False
        ),

        html.Div(
            [
                html.Div(
                    [
                        # Display graph
                        html.Div(
                            [
                                dcc.Graph(id="graph1")
                            ],
                            style={
                                'display': 'inline-block',
                                'width': '84%',
                                # 'height': "auto%",
                            }
                        ),
                        html.Div(
                            [
                                # X Variable
                                html.Div(
                                    [
                                        html.Label(
                                            [
                                                "Select X Variable: ",
                                                dcc.Dropdown(
                                                    id='x-variable',
                                                    multi=False,
                                                    # value="REC_X",
                                                    placeholder="Select an option for X")
                                            ],
                                        )
                                    ],
                                    style={'padding': 10}
                                ),

                                # Y Variable
                                html.Div(
                                    [
                                        html.Label(
                                            [
                                                "Select Y Variable:",
                                                dcc.Dropdown(
                                                    id='y-variable',
                                                    multi=False,
                                                    # value="REC_Y",
                                                    placeholder="Select an option for Y"
                                                )
                                            ],
                                        ),
                                    ],
                                    style={"padding": 10}
                                ),

                                # Color Variable
                                html.Div(
                                    [
                                        html.Label(
                                            [
                                                "Select color variable:",
                                                dcc.Dropdown(
                                                    id="color-variable",
                                                    multi=False,
                                                    # value="REC_Z",
                                                    placeholder="Select color variable"
                                                )
                                            ],
                                        )
                                    ],
                                    style={"padding": 10}
                                ),

                                # Annotation
                                html.Div(
                                    [
                                        html.Label(
                                            [
                                                "Select Annotation:",
                                                dcc.Dropdown(
                                                    id="annotation",
                                                    multi=True,
                                                    placeholder="Select annotation"
                                                )
                                            ],
                                        )
                                    ],
                                    style={"padding": 10,
                                           "width": "150%"}
                                ),

                                # Colorbar range
                                html.Div(
                                    [
                                        html.Label(
                                            [
                                                "Colorbar Range",
                                                html.Div(
                                                    [
                                                        dcc.Input(
                                                            id="colorbar-min",
                                                            type="number",
                                                            placeholder="min"
                                                        ),

                                                        dcc.Input(
                                                            id="colorbar-max",
                                                            type="number",
                                                            placeholder="max"
                                                        )
                                                    ],
                                                    style={
                                                        # "padding": 20,
                                                        # "float": "right",
                                                        # "width": "50%"
                                                    }
                                                )
                                            ],
                                        )
                                    ],
                                    style={
                                        'padding': 10,
                                        "width": "100%"
                                    }
                                ),

                                # Filter data
                                html.Div(
                                    [
                                        html.Label(
                                            [
                                                "Enter query to filter data",
                                                dcc.Input(
                                                    id="filter-query",
                                                    type="text",
                                                    placeholder="Query",
                                                    value="",
                                                )
                                            ]
                                        )
                                    ],
                                    style={
                                        "padding": 10,
                                        "width": "150%"
                                    }
                                ),

                                # Filter Graph
                                html.Div(
                                    [
                                        html.Label(
                                            [
                                                "Filter Graph points",
                                                html.Div(
                                                    [
                                                        dcc.RadioItems(
                                                            id="filter-graph",
                                                            options=[
                                                                {"label": "Original", "value": "orig"},
                                                                {"label": "Filtered", "value": "filter"}
                                                            ],
                                                            value="orig"
                                                        )
                                                    ]
                                                )
                                            ]
                                        )
                                    ],
                                    style={
                                        "padding": 10,
                                    }
                                )
                            ],
                            style={
                                "display": "inline-block",
                                "width": "15%",
                                "float": "right",
                                "fontSize": 14,
                                "font-family": "Ariel",
                                "backgroundColor": "#ffffff"
                            }
                        ),
                        html.Div(
                            id="show-table",
                            style={
                                "display": "inline-block",
                                "width": "50%"
                            }
                        )
                    ],
                    className="container",
                    style={
                        # "padding": 40,
                        "backgroudColor": "#ffffff"
                    }
                )
            ]
        ),
    ],
)


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif 'txt' or 'tsv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), delimiter=r'\s+'
                             )
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    return df


# Load Data
@app.callback(Output("csv-data", "data"),
              [Input("data-table-upload", "contents")],
              [State("data-table-upload", "filename")],
              prevent_initial_call=True, )
def parse_uploaded_file(contents, filename):
    if not filename:
        return no_update
    df = parse_contents(contents, filename)
    return df.to_json(date_format="iso", orient="split")


# Populate X, Y, Color Variable
@app.callback(
    [Output("x-variable", "options"),
     Output("y-variable", "options"),
     Output("color-variable", "options"),
     Output("annotation", "options")],
    [Input("csv-data", "data")])
def populate_x_y_color_dropdown(data):
    if not data:
        return no_update, no_update, no_update, no_update
    df = pd.read_json(data, orient="split")
    options = [{"label": i, "value": i} for i in df.columns]
    return options, options, options, options


# Display graph
@app.callback(
    Output("graph1", "figure"),
    [Input("x-variable", "value"),
     Input("y-variable", "value"),
     Input("color-variable", "value"),
     Input("colorbar-min", "value"),
     Input("colorbar-max", "value"),
     Input("annotation", "value"),
     Input("filter-query", "value"),
     Input("filter-graph", "value")],
    State("csv-data", "data")
)
def update_figure(x_var, y_var, color_var, colorbar_min, colorbar_max, annotation, filter_query, filter_graph, data):
    # fig = go.Figure(
    #     data=[
    #         go.Scatter(
    #             x=data['REC_X'],
    #             y=data['REC_Y'],
    #             mode='markers',
    #             marker=dict(
    #                 size=5,
    #                 color=data[selected_col],
    #                 colorscale='Rainbow',
    #                 showscale=True,
    #                 range_color = [0, 10]
    #             ),
    #             text=data['REC_ID'],
    #             hovertemplate=
    #             "<b>%{text}</b><br>" +
    #             "X: %{x}<br>" +
    #             "Y: %{y}<br>" +
    #             selected_col + ": %{marker.color:, %d}" +
    #             "<extra></extra>",
    #         )
    #     ],
    #     layout=go.Layout(
    #         title=selected_col
    #     )
    # )
    df = pd.read_json(data, orient="split")
    if filter_query != "" and filter_graph == "filter":
        print("Inside graph query: ", filter_query)
        df.query(filter_query, inplace=True)
        print(df.columns)
    fig = px.scatter(df,
                     x=x_var,
                     y=y_var,
                     color=color_var,
                     color_continuous_scale="rainbow",
                     range_color=[colorbar_min, colorbar_max],
                     hover_name=df.columns[0],
                     hover_data=annotation)
    fig.update_traces(marker_size=7)
    # Scaling x and y axis
    fig.update_yaxes(
        scaleanchor="x",
        scaleratio=1,
    )
    # Update fig size
    fig.update_layout(
        width=800,
        height=800,
        margin=dict(
            l=40,
            r=30,
            b=25,
            t=35,
            pad=4
        ),
        paper_bgcolor="White",
    )
    return fig


# Display Table
@app.callback(
    Output("show-table", "children"),
    [Input("x-variable", "value"),
     Input("y-variable", "value"),
     Input("color-variable", "value"),
     Input("annotation", "value"),
     Input("filter-query", "value")],
    State("csv-data", "data")
)
def show_table(x_var, y_var, col_var, annotation, filter_query, data):
    if not (x_var and y_var and col_var):
        return no_update
    df = pd.read_json(data, orient="split")
    cols = [df.columns[0], x_var, y_var, col_var]
    if annotation is not None:
        for c in annotation:
            cols.append(c)
    if filter_query != "":
        df.query(filter_query, inplace=True)
    df = df.loc[:, cols]
    table = dash_table.DataTable(
        id="table",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records")
    )
    return table


if __name__ == '__main__':
    app.run_server(debug=True)
