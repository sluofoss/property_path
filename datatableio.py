from dash import Dash, Output, Input, State, html, dcc, callback, MATCH, dash_table
import uuid

import pandas as pd
import base64
import io


class DataTableIO(html.Div):
    # A set of functions that create pattern-matching callbacks of the subcomponents

    class ids:
        datatable = lambda aio_id: {
            "component": "DataTableAIO",
            "subcomponent": "datatable",
            "aio_id": aio_id,
        }
        upload = lambda aio_id: {
            "component": "DataTableAIO",
            "subcomponent": "upload",
            "aio_id": aio_id,
        }
        download_button = lambda aio_id: {
            "component": "DataTableAIO",
            "subcomponent": "download_button",
            "aio_id": aio_id,
        }
        download = lambda aio_id: {
            "component": "DataTableAIO",
            "subcomponent": "download",
            "aio_id": aio_id,
        }
        addrow = lambda aio_id: {
            "component": "DataTableAIO",
            "subcomponent": "addrow",
            "aio_id": aio_id,
        }

    # Make the ids class a public class
    ids = ids

    def __init__(self, columns: list = [], aio_id=None, **datatable_props):
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
            [# [] Equivalent to `html.Div([...])`

                html.Div(
                    [
                        dcc.Upload(
                            id=self.ids.upload(aio_id),
                            children=html.Div(
                                ["Drag and Drop or ", html.A("Select Files")],
                                style = {
                                    'margin':'10px'
                                }
                            ),
                            style={
                                "height": "40px",
                                "lineHeight": "10px",
                                "borderWidth": "1px",
                                "borderStyle": "dashed",
                                "borderRadius": "5px",
                                "textAlign": "center",
                                "margin": "10px",
                            },
                        ),
                        html.Button(
                            "Download",
                            id=self.ids.download_button(aio_id),
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
                        dcc.Download(id=self.ids.download(aio_id)),
                        html.Button(
                            "Add row",
                            id=self.ids.addrow(aio_id),
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
                    ],
                    style={"display": "flex"},
                ),
                html.Div(
                    dash_table.DataTable(
                        id=self.ids.datatable(aio_id),
                        columns=([{"id": c, "name": c} for c in columns]),
                        data=[
                            dict(Model=i, **{param: None for param in columns})
                            for i in range(1, 5)
                        ],
                        editable=True,
                        row_deletable=True,
                        #export_format="csv",
                        #export_headers="display",
                    ),
                    style={"display": "block"},
                ),
            ], 
            #style = {'display':'grid', 'grid-template-columns': 'auto auto auto', 'width':'100px'})
            style = {"width": "40%", "display": "inline-block", "margin": "10px"}
        )

    #@callback(
    #    Output(ids.datatable(MATCH), 'data'),
    #    Output(ids.datatable(MATCH), 'columns'),
    #    Input(ids.upload(MATCH), 'contents'),
    #    State(ids.upload(MATCH), 'filename'))
    #def upload_file(contents, filename):
    #    if contents is None:
    #        return [{}], []
    #    df = parse_contents(contents, filename)
    #    return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]


    #@callback(
    #    Output(ids.download(MATCH), "data"),
    #    Input(ids.download_button(MATCH), "n_clicks"),
    #    State(ids.datatable(MATCH),"data"),
    #    prevent_initial_call=True,
    #)
    #def download_file(n_clicks,data):
    #    #return dcc.send_data_frame(df.to_csv, "mydf.csv")
    #    return None
    #
    @callback(
        Output(ids.datatable(MATCH), "data"),
        Input(ids.addrow(MATCH), "n_clicks"),
        State(ids.datatable(MATCH), "data"),
        State(ids.datatable(MATCH), "columns"),
    )
    def add_row(n_clicks, data, columns):
        if n_clicks > 0:
            data.append({c["id"]: "" for c in columns})
        return data

    # @callback()
    # def table_update():
    #    # maybe this should be moved to some other place?
    #    # this is more focused on how this component changes other visual outside of the data table
    #    pass


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if 'csv' in filename:
        # Assume that the user uploaded a CSV file
        return pd.read_csv(
            io.StringIO(decoded.decode('utf-8')))
    elif 'xls' in filename:
        # Assume that the user uploaded an excel file
        return pd.read_excel(io.BytesIO(decoded))