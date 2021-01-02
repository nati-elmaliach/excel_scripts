from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
import math
import operator
from itertools import chain


from ExcelReader.ExcelReader import ExeclReader


columns_to_delete = {
    "Unnamed: 9": "Unnamed: 20",
    "Unnamed: 27": "Unnamed: 31",
    "Unnamed: 33": "Unnamed: 37"
}


MAX = 5000000000


def print_row(*args):
    print("-----------------")
    print(args)
    print("-----------------")


def get_column_value(index, col_name, data, should_print=False):
    if should_print:
        print(index)
        print(col_name)
    return data.iloc[index - 1].iloc[columns_map[col_name]]


# 5


def get_valid_rows(data, ex_file, valid_rows_pass):
    filterd_rows = []
    for index in valid_rows_pass:
        # print_row(data.iloc[index - 1])

        per_year_per_pair = get_column_value(index,  "per_year_per_pair", data)
        avg_winr = get_column_value(index,  "avg_winr", data)
        avg_dd = get_column_value(index,  "avg_dd", data) * 100
        high_dd = get_column_value(index,  "high_dd", data) * 100
        std = get_column_value(index,  "std", data)
        profit_std = get_column_value(index,  "profit_std", data)
        total_profit = get_column_value(index,  "total_profit", data)

        # print(profit_std)
        print(get_column_value(index,  "pass", data))

        isValidPass = False
        if per_year_per_pair >= 0:
            if avg_winr >= 69.99:
                if avg_dd >= 0:
                    if high_dd >= 0:
                        if std > 4999:
                            if profit_std >= 1999:
                                if total_profit >= 4999:
                                    isValidPass = True

        if isValidPass:
            print(True)
            one_pass = get_column_value(index,  "pass", data)
            filterd_rows.append(one_pass)

    return filterd_rows


# 4
def get_file_ending_row_index(data, ex_file):
    ending_row_index = data.shape[0]
    for row_index in range(ending_row_index):
        sample_columns_value = data.iloc[row_index].iloc[columns_map["per_year_per_pair"]]

        # find out what is the index of the last row
        if type(sample_columns_value) is None:
            return row_index

        if math.isnan(sample_columns_value):
            return row_index

    return ending_row_index

# 3


def get_stdo_data(file_name):
    print(f'Getting {file_name} data')
    # Reading the file will give us a dict
    dict_pd = pd.read_excel(file_name, sheet_name=None)

    # under the STDo is a dataframe
    df = dict_pd["STDo"]

    # the data start at row number 7
    data = df.iloc[7:]

    ending_row_index = get_file_ending_row_index(data, file_name)

    return data, ending_row_index


def print_all_columns_names(data):
    print_row(data.columns.values)


def format_value(value):
    return round(value, 2)


# 2
DATA_COLUMNS = ["Pass", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020",
                        "Per Year Per Pair", "AVG WINR", "AVG DD", "HIGH DD", "STD", "Profit STD", "P.p (avg)", "P.F(AVG)", "Total Profit"]


def write_to_excel(valid_pass_numbers, excel_data):
    # print(excel_data[list(excel_data.keys())[0]])
    for broker, data in excel_data.items():
        # print(type(data))

        data = data[np.isin(data.Pass, valid_pass_numbers)]
        print(broker)
        print(data)


def start(excel_files):

    valid_passes = []
    excel_data = {}

    for excel_file in excel_files:
        print("--------------------------")
        print(excel_file)
        print("--------------------------")

        data = ExeclReader.get_df(excel_file)
        # print_all_columns_names(data)

        data = ExeclReader.filter(data, "total_profit", operator.gt, 0)
        data = ExeclReader.mid_filter(data, "std", operator.lt)
        data = ExeclReader.mid_filter(data, "total_profit", operator.gt)

        # drop unnecassary columns
        for key, value in columns_to_delete.items():
            data.drop(
                data.loc[:, key: value].columns, axis=1, inplace=True)

        #  All new columns names, need to generate first 9 - 20
        data.columns = DATA_COLUMNS

        excel_data[excel_file] = data

        data = ExeclReader.get_col(data, "Pass")
        data = list(data)
        data.sort()
        # print(data)

        valid_passes.append(data)
        print("--------------------------")

    res_dict = {}
    for arr in valid_passes:
        for val in arr:
            if val in res_dict:
                res_dict[val] += 1
            else:
                res_dict[val] = 1

    # print the the reults, pass: number of hits
    # print(res_dict)

    valid_pass_numbers = []
    for pass_num in res_dict:
        if res_dict[pass_num] == len(excel_files):
            # prits the results on one line
            # print_row(pass_num)
            valid_pass_numbers.append(pass_num)

    print_row(valid_pass_numbers)
    write_to_excel(valid_pass_numbers, excel_data)


# 1
def get_all_excels(files_list):
    valid_files = []
    for index, file_name in enumerate(files_list):
        if "xlsm" in file_name:
            valid_files.append(file_name)
    return valid_files


# 0
def main():
    all_files = [f for f in listdir("./") if isfile(join("./", f))]
    excel_files = get_all_excels(all_files)
    print(excel_files)
    start(excel_files)


main()
