from dash import Dash, html, dcc, callback, Output, Input, dash_table
import pandas as pd
import plotly.express as px

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash()

_property_fixed_columns = ['address', 'water', 'council', 'strata']

params = [
    'Weight', 'Torque', 'Width', 'Height',
    'Efficiency', 'Power', 'Displacement'
]

app.layout = [
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    #dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
    dash_table.DataTable(
        id = 'property fixed information table',
        columns = (
            {'id':c, 'name':c} for c in _property_fixed_columns
        ),
        data=[
            dict(**{param: None for param in _property_fixed_columns})
            for i in range(1, 5)
        ],
        editable=True
    ),
    #dcc.Graph(id='graph-content')
]

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df[df.country==value]
    return px.line(dff, x='year', y='pop')

if __name__ == '__main__':
    app.run(debug=True)