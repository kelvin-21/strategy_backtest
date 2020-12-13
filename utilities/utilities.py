import pandas as pd
from openpyxl import load_workbook

from config import represent_in_precentage, represent_with_comma, represent_as_integer, represent_as_decimal


def object_list_contains_object(obj_list, obj):
    for obj_temp in obj_list:
        if obj_temp == obj:
            return True
    return False

# def save_to_excel(df, excel_name, sheet_name):

#     try:
#         book = load_workbook(excel_name)
#         writer = pd.ExcelWriter(excel_name, engine='openpyxl') # pylint: disable=abstract-class-instantiated
#         writer.book = book
#         writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
#         write_new_sheet(writer, df, sheet_name)
#     except Exception as e:
#         print('[ERROR]', e)
#         writer = pd.ExcelWriter(excel_name, engine='xlsxwriter') # pylint: disable=abstract-class-instantiated
#         write_new_sheet(writer, df, sheet_name)
    
#     writer.close()

def write_new_sheet(writer, df, sheet_name):
    
    workbook = writer.book
    format_percent = workbook.add_format({'num_format': '0.0000%'})
    format_comma = workbook.add_format({'num_format': '#,##0.00'})
    format_integer = workbook.add_format({'num_format': '#,##'})
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
        max_len = max((
            series.astype(str).map(len).max(),  # len of largest item
            len(str(series.name))  # len of column name/header
            )) + 1  # adding a little extra space
        worksheet.set_column(idx, idx, max_len)  # set column width

    print('[OUTPUT] Completed writing new sheet {}'.format(sheet_name))

def index_to_col_letter(i):
    return chr(ord('A') + i)

def decimal_to_presentage(x):
    return '{:.4%}'.format(x)