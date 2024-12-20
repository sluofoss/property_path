from dash import Dash, html, dcc, callback, Output, Input, State, dash_table
from datatableio import DataTableIO
import pandas as pd
import plotly.express as px
from finance_etc.mortgage import stamp_duty, buy_amortized, project_n_years_property_spend

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
    "address",
    'stamp duty (upper)', 
    'stamp duty (lower)', 
    'after tax full rent (yearly)', 
    'after tax partial rent (yearly)',
    'monthly mortgage (upper)',
    'monthly mortgage (lower)',
    'yearly total spending (upper)',
    'yearly total spending (lower)',
    #'estimated cost', should combine loan into hence in different table
    # or should it be based on the loan with the smallest possible rate?
]
loan_col = [
    #"bank", 
    "loan name", 
    "rate", 
    #"repay interest only", 
    #"year period"
]

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
    html.Div(
        dash_table.DataTable(
            id = 'property_derived', 
            columns=([{"id": c, "name": c} for c in prop_derived_col]),
            data=[
                dict(Model=i, **{param: None for param in prop_derived_col})
                for i in range(1, 5)
            ],
        ),
        style = {'display':'flex', 'margin':'20px'},
    ),
    dcc.Graph(id='graph-content1')
]


@callback(
    Output('graph-content1', 'figure'),
    Output('property_derived', 'data'),
    Input('calculate', 'n_clicks'),
    State(DataTableIO.ids.datatable('property'), 'data'),
    State(DataTableIO.ids.datatable('loan'), 'data'),
    State("input_deposit", 'value'),
    prevent_initial_call=True,
)
def update_graph(n_clicks, property_data, loan_data, deposit):
    #print(pd.DataFrame(data))
    loan_df = pd.DataFrame(loan_data)
    loan_df['rate'] = loan_df['rate'].astype(float) 
    if 'Model' in loan_df.columns:
        loan_df = loan_df.drop(columns=['Model'])

    derived = []
    for rec in property_data:
        derived.append({
            "address":rec["address"],
            'stamp duty (upper)':stamp_duty(int(rec['upper buy price'])),
            'stamp duty (lower)':stamp_duty(int(rec['lower buy price'])),
            'after tax full rent (yearly)': int(int(rec['estimated full rent (weekly)'])*40*0.8), 
            'after tax partial rent (yearly)': int(int(rec['estimated partial rent (weekly)'])*40*0.8),
            'monthly mortgage (upper)': (_upper:= buy_amortized(
                loan_amount = int(rec['upper buy price'])-deposit, #TODO replace 
                interest_rate = loan_df['rate'].min(), #TODO do group by loan type (is interest only), 
                years= 30, #TODO allow customized year 
                year_days = 365.25, 
                repay_day_apart = 365.25/12
            )),
            'monthly mortgage (lower)': (_lower:= buy_amortized(
                loan_amount = int(rec['lower buy price'])-deposit, #TODO replace 
                interest_rate = loan_df['rate'].min(), #TODO do group by loan type (is interest only), 
                years= 30, #TODO allow customized year
                year_days = 365.25, 
                repay_day_apart = 365.25/12
            )),
            'yearly total spending (upper)': 4*(rec['water']+rec['council']+rec['strata'])+_upper*12,
            'yearly total spending (lower)': 4*(rec['water']+rec['council']+rec['strata'])+_lower*12

        })
    ordered = sorted(derived, key= lambda r:r['yearly total spending (upper)']-r['after tax partial rent (yearly)'])
    #dff = df[df.country == value]
    #return px.line(dff, x="year", y="pop")
    return (
        px.bar(
            pd.DataFrame(ordered), 
            x = 'address', 
            y = ['yearly total spending (upper)','yearly total spending (lower)'],
            barmode = 'overlay',
            width = 1000,
            height = 1000
        ), 
        ordered
    )

if __name__ == "__main__":
    app.run(debug=True)
