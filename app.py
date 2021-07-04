import dash
import dash_table
import sys
import pandas as pd
import data_loader
import pic_loader

app = dash.Dash(__name__, assets_folder="assets")


def table_type(df_column):
    # Note - this only works with Pandas >= 1.0.0

    if sys.version_info < (3, 0):  # Pandas 1.0.0 does not support Python 2
        return 'any'

    if 'local' in df_column:
        return 'Image'
    elif isinstance(df_column.dtype, pd.DatetimeTZDtype):
        return 'datetime',
    elif (isinstance(df_column.dtype, pd.StringDtype) or
            isinstance(df_column.dtype, pd.BooleanDtype) or
            isinstance(df_column.dtype, pd.CategoricalDtype) or
            isinstance(df_column.dtype, pd.PeriodDtype)):
        return 'text'
    elif (isinstance(df_column.dtype, pd.SparseDtype) or
            isinstance(df_column.dtype, pd.IntervalDtype) or
            isinstance(df_column.dtype, pd.Int8Dtype) or
            isinstance(df_column.dtype, pd.Int16Dtype) or
            isinstance(df_column.dtype, pd.Int32Dtype) or
            isinstance(df_column.dtype, pd.Int64Dtype)):
        return 'numeric'
    else:
        return 'any'


def prepare_df(path: str) -> pd.DataFrame:
    data = pd.read_csv(path, sep=";", encoding="utf-8")
    # Reorder and drop some cols
    data = data.loc[:, ["local_thumb",
                        "name_x",
                        "yearpublished",
                        "minplayers",
                        "maxplayers",
                        "age",
                        "name_y",
                        "boardgamecategory",
                        "description"]]
    data.rename(columns={"name_x": "Name", "name_y": "Other_names"}, inplace=True)
    return data


def prepare_app(df):
    app = dash.Dash(__name__, assets_folder="assets")
    app.layout = dash_table.DataTable(
        columns=[
            {'name': i, 'id': i, 'type': table_type(df[i]), 'presentation': 'markdown'} for i in df.columns
        ],
        data=df.to_dict('records'),
        # filter_action='native',

        css=[{
            'selector': 'table',
            'rule': 'table-layout: fixed'  # note - this does not work with fixed_rows
        }],
        style_table={'height': 400},
        style_data={
            'width': '{}%'.format(100. / len(df.columns)),
            'textOverflow': 'ellipsis',
        },
        tooltip_data=[
            {
                column: {'value': str(value), 'type': 'markdown'}
                for column, value in row.items()
            } for row in df.to_dict('rows')
        ],
        tooltip_duration=None
    )
    return app


@app.callback()
def filter_data():
    pass



if __name__ == '__main__':
    PATH = 'games_full_info.csv'
    data_loader.step()
    pic_loader.step()
    data = prepare_df(PATH)
    app = prepare_app(data)
    app.run_server(debug=True)
