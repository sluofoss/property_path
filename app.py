from dash import Dash, html, dcc, callback, Output, Input, dash_table
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


property_table = dash_table.DataTable(
    id="property info table",
    columns=([{"id": c, "name": c} for c in prop_col]),
    data=[dict(Model=i, **{param: None for param in prop_col}) for i in range(1, 5)],
    editable=True,
    row_deletable=True,
    export_format="csv",
    export_headers="display",
    # style={'width': '45%', 'display': 'inline-block', 'margin': '10px'}
)
loan_table = dash_table.DataTable(
    id="home loan info table",
    columns=([{"id": c, "name": c} for c in loan_col]),
    data=[dict(Model=i, **{param: None for param in loan_col}) for i in range(1, 5)],
    editable=True,
    row_deletable=True,
    export_format="csv",
    export_headers="display",
    # style={'width': '45%', 'display': 'inline-block', 'margin': '10px'}
)
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
            html.Div(
                [
                    html.Div(
                        [
                            # html.H2('file upload', style={'margin':'10px'}),
                            # html.H2('file download', style={'margin':'10px'}),
                            dcc.Upload(
                                id="datatable-upload-" + tid,
                                children=html.Div(
                                    ["Drag and Drop or ", html.A("Select Files")]
                                ),
                                style={
                                    "width": "100%",
                                    "height": "60px",
                                    "lineHeight": "60px",
                                    "borderWidth": "1px",
                                    "borderStyle": "dashed",
                                    "borderRadius": "5px",
                                    "textAlign": "center",
                                    "margin": "10px",
                                },
                            )
                        ],
                        style={"display": "flex"},
                    ),
                    html.Div(table, style={"display": "block"}),
                ],
                style={"width": "40%", "display": "inline-block", "margin": "10px"},
            )
            for tid, table in [("property", property_table), ("loan", loan_table)]
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
