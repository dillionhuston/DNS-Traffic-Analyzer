
import plotly.graph_objects as go


class graph:

    def GraphTest():

        fig = go.Figure(data=go.Scatter(
        x=[0, 1, 2],
        y=[6, 10, 2],
        error_y=dict(
        type='data', # value of error bar 
        array=[1, 2, 3],
        visible=True)
    ))
        fig.show()
