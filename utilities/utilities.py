import pandas as pd
import numpy as np
from openpyxl import load_workbook
from datetime import datetime

from config import represent_in_precentage, represent_with_comma, represent_as_integer, represent_as_decimal


def object_list_contains_object(obj_list, obj):
    for obj_temp in obj_list:
        if obj_temp == obj:
            return True
    return False

def write_new_sheet(writer, df, sheet_name):
    
    workbook = writer.book
    format_percent = workbook.add_format({'num_format': '0.0000%'})
    format_comma = workbook.add_format({'num_format': '#,##0.00'})
    format_integer = workbook.add_format({'num_format': '#,##0'})
    format_decimal = workbook.add_format({'num_format': '0.0000'})

    df.to_excel(writer, sheet_name=sheet_name, index=False)
    worksheet = writer.sheets[sheet_name]

    # col format
    for i in range(len(df.columns)):
        col = df.columns[i]
        col_letter = index_to_col_letter(i)
        whole_col = '{}:{}'.format(col_letter, col_letter)
        if col in represent_in_precentage:
            worksheet.set_column(whole_col, None, format_percent)
        elif col in represent_with_comma:
            worksheet.set_column(whole_col, None, format_comma)
        elif col in represent_as_integer:
            worksheet.set_column(whole_col, None, format_integer)
        elif col in represent_as_decimal:
            worksheet.set_column(whole_col, None, format_decimal)

    # adjust col width
    for idx, col in enumerate(df):  # loop through all columns
        series = df[col]
        if col in represent_in_precentage:
            max_len = max((
                series.astype(str).map(dp_4).map(len).max() + 1, # adding 1 for % sign
                len(str(series.name))  # len of column name/header
            )) + 1  # adding a little extra space
        else:
            max_len = max((
                series.astype(str).map(len).max(),  # len of largest item
                len(str(series.name))  # len of column name/header
                )) + 1  # adding a little extra space
        worksheet.set_column(idx, idx, max_len)  # set column width

    print('[OUTPUT] Completed writing new sheet {}'.format(sheet_name))

def index_to_col_letter(i: int) -> str:
    return chr(ord('A') + i)

def dp_4(x: str) -> str:
    i = x.find('.')
    if i == -1:
        return x
    else:
        return x[:i+5]

def decimal_to_presentage(x: float) -> str:
    return '{:.4%}'.format(x)

def dtStr_to_dt(date_time_str: str):
    return datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')

def str_time_diff_in_days(start:str, end:str) -> int:
    start_obj = dtStr_to_dt(start)
    end_obj = dtStr_to_dt(end)
    return (end_obj - start_obj).days

def df_contains_dict(df: pd.DataFrame, my_dict: dict) -> bool:
    if len(my_dict) == 0:
        raise ValueError('[ERROR] empty dict')

    result = set()
    flag = 0

    for key in my_dict.keys():
        if my_dict[key]:
            if type(my_dict[key]) is tuple:
                temp = set(df[df[key] == str(my_dict[key])].index)
            else:
                temp = set(df[df[key] == my_dict[key]].index)
        else:
            temp = set(df[df[key].isnull()].index)

        if flag == 0:
            result = temp
            flag = 1
        else:
            result = result.intersection(temp)
            if len(result) == 0:
                return False
    return True


if __name__ == '__main__':
    df = pd.DataFrame()
    df['A'] = [10.9999, 20.77777 ,30.888 ,40.22, 40.12345678, 5.2, 60]
    df['B'] = [120, 240 ,310 ,430, 40, 25, 560]
    df['C'] = df['B'].copy() + 10
    df['D'] = df['C'].copy() + 20

    my_dict = dict({'B': 40, 'C': 50, 'D': 150})

    print(df)
    print(my_dict)

    print(df_contains_dict(df, my_dict))