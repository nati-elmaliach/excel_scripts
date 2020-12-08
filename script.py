from os import listdir
from os.path import isfile, join
import pandas as pd
import math

columns_map = {
    "pass": 0,
    "per_year_per_pair": 21,
    "avg_winr": 22,
    "avg_dd": 23,
    "high_dd": 24,
    "std": 25,
    "profit_std": 26,
    "total_profit": 39
}


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

        #print(profit_std)

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
    # return 6
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


# 2
def start(excel_files):
    one_excel_file = excel_files.pop()
    data, ending_row_index = get_stdo_data(one_excel_file)
    valid_rows_pass = get_valid_rows(
        data, one_excel_file, [x for x in range(ending_row_index)])

    print(valid_rows_pass)

    if len(excel_files) > 0:
        for file_name in excel_files:
            data = get_stdo_data(file_name)[0]

            valid_rows_pass = get_valid_rows(
                data,  file_name, valid_rows_pass)

            print(valid_rows_pass)


# 1


def get_all_excels(files_list):
    for index, file_name in enumerate(files_list):
        if "xlsm" not in file_name:
            files_list.pop(index)
    return files_list


# 0
def main():
    all_files = [f for f in listdir("./") if isfile(join("./", f))]
    excel_files = get_all_excels(all_files)
    start(excel_files)


main()
