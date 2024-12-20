from dash import Dash, html, dcc, callback, Output, Input, State, dash_table
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
    "upper buy price",
    "lower buy price",
    "estimated full rent (weekly)",
    "estimated partial rent (weekly)",
]
prop_derived_col = [
    'stamp duty (upper)', 
    'stamp duty (lower)', 
    'after tax full rent (yearly)', 
    'after tax partial rent (yearly)',
    #'estimated cost', should combine loan into hence in different table
    # or should it be based on the loan with the smallest possible rate?
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
            html.Div(
                dash_table.DataTable(
                    id = 'property_derived', 
                    columns=([{"id": c, "name": c} for c in prop_derived_col]),
                    data=[
                        dict(Model=i, **{param: None for param in prop_derived_col})
                        for i in range(1, 5)
                    ],
                ),
                style = {'display':'inline-flex', 'margin':'20px'},
            ),
            DataTableIO(loan_col, 'loan'),
        ]
    ),
    html.Hr(),
    html.Button(
        "Calculate",
        id="calculate",
        n_clicks=0,
        style={
            "height": "40px",
            "lineHeight": "10px",
            "borderWidth": "1px",
            "borderRadius": "5px",
            "textAlign": "center",
            "margin": "10px",
        },
    ),
    # dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
    # 
    dcc.Graph(id='graph-content1'),
    dcc.Graph(id='graph-content2'),
    dcc.Graph(id='graph-content3'),
    dcc.Graph(id='graph-content'),

]


@callback(
    Output('graph-content1', 'figure'),
    Output('property_derived', 'data'),
    Input('calculate', 'n_clicks'),
    State(DataTableIO.ids.datatable('property'), 'data'),
    prevent_initial_call=True,
)
def update_graph(n_clicks, data):
    print(pd.DataFrame(data))
    #dff = df[df.country == value]
    #return px.line(dff, x="year", y="pop")
    return px.line(), None

if __name__ == "__main__":
    app.run(debug=True)
