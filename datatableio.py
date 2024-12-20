from dash import Dash, Output, Input, State, html, dcc, callback, MATCH, dash_table
import uuid
import pandas as pd


class DataTableIO(html.Div):
    # A set of functions that create pattern-matching callbacks of the subcomponents

    class ids:
        datatable = lambda aio_id: {
            "component": "DataTableAIO",
            "subcomponent": "datatable",
            "aio_id": aio_id,
        }
        store = lambda aio_id: {
            "component": "DataTableAIO",
            "subcomponent": "store",
            "aio_id": aio_id,
        }

    # Make the ids class a public class
    ids = ids

    def __init__(self, df: pd.DataFrame = None, aio_id=None, **datatable_props):
        """DataTableIO is an All-in-One component that is composed of a parent `html.Div`
        with a `dcc.Store` and a `dash_table.DataTable` as children.

        - `df` - A Pandas dataframe
        - `aio_id` - The All-in-One component ID used to generate the `dcc.Store` and `DataTable` components's dictionary IDs.
        - `**datatable_props` - Properties passed into the underlying `DataTable`
        """
        if aio_id is None:
            aio_id = str(uuid.uuid4())

        # Define the component's layout
        super().__init__(
            [
                # Equivalent to `html.Div([...])`
                # html.H2('file upload', style={'margin':'10px'}),
                # html.H2('file download', style={'margin':'10px'}),
                html.Div(
                    [
                        dcc.Upload(
                            id=aio_id + "datatable-upload",
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
                html.Div(
                    dash_table.DataTable(
                        id=aio_id + "datatable",
                        columns=([{"id": c, "name": c} for c in df.columns]),
                        data=[
                            dict(Model=i, **{param: None for param in df.columns})
                            for i in range(1, 5)
                        ],
                        editable=True,
                        row_deletable=True,
                        export_format="csv",
                        export_headers="display",
                    ),
                    style={"display": "block"},
                ),
            ]
        )
