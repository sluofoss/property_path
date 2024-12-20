from dash import Dash, html, dcc, callback, Output, Input, dash_table
from datatableio import DataTableIO
import pandas as pd
import plotly.express as px

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv"
)

app = Dash(__name__, external_stylesheets=external_stylesheets)

prop_col = [
    "address",
    "water",
    "council",
    "strata",
    "estimated full rent",
    "estimated partial rent",
]
loan_col = ["bank", "loan name", "rate", "repay interest only", "year period"]

app.layout = [
    html.H1(
        children="Investment and principal residence return calculator",
        style={"textAlign": "center"},
    ),
    dcc.Input(
        id="input_deposit",
        type="number",
        placeholder="initial deposit amount",
    ),
    html.Div(
        [
            DataTableIO(prop_col, 'property'),
            DataTableIO(loan_col, 'loan'),
        ]
    ),
    html.Hr(),
    # dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
    # dcc.Graph(id='graph-content')
]


# @callback(
#    Output('graph-content', 'figure'),
#    Input('dropdown-selection', 'value')
# )
def update_graph(value):
    dff = df[df.country == value]
    return px.line(dff, x="year", y="pop")


if __name__ == "__main__":
    app.run(debug=True)
