import pandas as pd
import math


columns_map = {
    "Pass": "Pass",
    "std": "Unnamed: 25",
    "total_profit": "Unnamed: 39",

}


class ExeclReader:

    @staticmethod
    def get_df(file_name):
        # Reading the file will give us a dict
        dict_pd = pd.read_excel(file_name, sheet_name=None)["STDo"]

        # print all columns of this excel file
        #print(dict_pd.columns.values)

        num_of_rows = dict_pd.shape[0]

        should_break = False
        for row_index in range(0, num_of_rows):

            total_profit = dict_pd.iloc[row_index][columns_map["total_profit"]]

            if type(total_profit) is str:
                should_break = True

            if type(total_profit) is float and should_break:
                return dict_pd.iloc[row_index:]

    @staticmethod
    def filter(df, col, relate, cut):
        return df[relate(df[columns_map[col]], cut)]

    @staticmethod
    def mid_filter(df, col, relate):

        mid = (df[columns_map[col]].min() + df[columns_map[col]].max()) / 2
        print(f"{col} min {df[columns_map[col]].min()}")
        print(f"{col} max {df[columns_map[col]].max()}")
        print(f"{col} mid {mid}")

        return ExeclReader.filter(df, col, relate, mid)

    @staticmethod
    def get_col(df, col):
        return df[columns_map[col]].values

    @staticmethod
    def get_row(df, col):
        return df[columns_map[col]].values
