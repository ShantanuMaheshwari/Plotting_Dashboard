"""Importing Libraries"""
import numpy as np
import pandas as pd
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import plotly.express as px

# %%

app = dash.Dash(__name__)

# %%

data = pd.read_csv("./data/rf-0917-FinalRecDB-rms", delimiter="\s+")

# %%
available_cols = ["DRIFTA", "DRIFTB", "ZSTART", "ZDEPLOY", "ZPICKUP", "NHITS"]

# %%

# # pyo.plot(figure_or_data=fig)
# fig.show()
# Using plotly express
# fig = px.scatter(data, x="REC_X", y="REC_Y", color="NHITS")

# %%

app.layout = html.Div(style={
    'backgroundColor': 'White',
    'columnCount': 1
},
    children=[
        dcc.Dropdown(
            id="select_col",
            options=[{'label': i, 'value': i} for i in available_cols],
            value=available_cols[0]
        ),
        dcc.Input(
            id="input1",
            type="number",
            placeholder="Min"
        ),
        dcc.Input(
            id="input2",
            type="number",
            placeholder="Max"
        ),
        dcc.Graph(id='graph1')
    ],
)

# @app.callback(
#     Output('output_colorbar_slider', 'children'),
#     Input('colorbar_slider', 'value'))
# def update_output(value):
#     return 'You have selected "{}"'.format(value)

@app.callback(
    Output("graph1", "figure"),
    [Input("select_col", "value"),
     Input("input1", "value"),
     Input("input2", "value")])
def update_figure(selected_col, colorbar_min, colorbar_max):
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
    fig = px.scatter(data,
                     x="REC_X",
                     y="REC_Y",
                     color=selected_col,
                     color_continuous_scale="rainbow",
                     range_color=[colorbar_min, colorbar_max],
                     hover_name="REC_ID")
    # Scaling x and y axis
    fig.update_yaxes(
        scaleanchor="x",
        scaleratio=1,
    )
    # Update fig size
    fig.update_layout(
        width=700,
        height=700,
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


if __name__ == '__main__':
    app.run_server(debug=True)
