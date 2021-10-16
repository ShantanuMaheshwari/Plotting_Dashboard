"""Importing Libraries"""
import numpy as np
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import plotly.express as px

# %%

app = dash.Dash(__name__)

# %%

data = pd.read_csv("./data/rf-0917-FinalRecDB-rms", delimiter="\s+")

# %%
available_cols = ["DRIFTA", "DRIFTB", "ZSTART", "ZDEPLOY", "ZPICKUP"]

# %%

# # pyo.plot(figure_or_data=fig)
# fig.show()
# Using plotly express
# fig = px.scatter(data, x="REC_X", y="REC_Y", color="NHITS")

# %%

app.layout = html.Div(style={
    'backgroundColor': '#111111'
},
    children=[
        dcc.Graph(id='graph1'),
        dcc.Dropdown(
            id="select_col",
            options=[{'label': i, 'value': i} for i in available_cols],
            value=available_cols[0]
        )
    ]
)


@app.callback(
    Output("graph1", "figure"),
    Input("select_col", "value"))
def update_figure(selected_col):
    fig = go.Figure(
        data=[
            go.Scatter(
                x=data['REC_X'],
                y=data['REC_Y'],
                mode='markers',
                marker=dict(
                    size=5,
                    color=data[selected_col],
                    colorscale='Rainbow',
                    showscale=True,
                ),
                text=data['REC_ID'],
                hovertemplate=
                "<b>%{text}</b><br>" +
                "X: %{x}<br>" +
                "Y: %{y}<br>" +
                selected_col + ": %{marker.color:, %d}" +
                "<extra></extra>",
            )
        ],
        layout=go.Layout(
            title=selected_col
        )
    )
    # Scaling x and y axis
    fig.update_yaxes(
        scaleanchor="x",
        scaleratio=1,
    )
    # Update fig size
    fig.update_layout(
        width=680,
        height=680,
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
