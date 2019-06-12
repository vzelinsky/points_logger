import gspread
from gspread.utils import rowcol_to_a1
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime as dt


def get_spreadsheet(name):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name("google_config.json", scope)
    gc = gspread.authorize(creds)
    sh = gc.open(name)
    return sh


def get_worksheet(spreadsheet, name):
    return spreadsheet.worksheet(name)


def get_current_month():
    return dt.now().strftime("%B")


def get_next_empty_name_cell_a1(worksheet):
    row = worksheet.find("Names").row
    all_names = worksheet.row_values(row)[1:]
    col_counter = 2
    empty_cell = None
    for name in all_names:
        if not name: # If string is empty
            break
        col_counter += 1
    try:
        empty_cell = worksheet.cell(row, col_counter)
    except Exception:
        worksheet.add_cols(10)
        empty_cell = worksheet.cell(row, col_counter)
    return rowcol_to_a1(empty_cell.row, empty_cell.col)



def add_user(worksheet, username):
    empty_cell_a1 = get_next_empty_name_cell_a1(worksheet)
    worksheet.update_acell(empty_cell_a1, username)



points_logger_sheet = get_spreadsheet("Points Logger")
current_month = get_current_month()
current_worksheet = get_worksheet(points_logger_sheet, current_month)

add_user(current_worksheet, "test")
