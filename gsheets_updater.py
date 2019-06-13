from typing import Any
from gspread import *
from gspread.utils import rowcol_to_a1
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime as dt


def get_spreadsheet(name: str) -> Spreadsheet:
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name("google_config.json", scope)
    gc = authorize(creds)
    sh = gc.open(name)
    return sh


def get_worksheet(spreadsheet: Spreadsheet, name: str) -> Worksheet:
    # TODO : need to handle exception here?
    return spreadsheet.worksheet(name)


def get_current_month_name() -> str:
    return dt.now().strftime("%B")


def get_next_empty_cell_after_cell(worksheet: Worksheet, after_cell: Cell, return_format="a1") -> Any:
    """ Gets the next empty cell after a specified cell (column-wise) in the specified format """
    # look at all cells next to after_cell
    all_names = worksheet.row_values(after_cell.row)[after_cell.col:]
    # start col counter at cell next to after_cell
    col_counter = after_cell.col + 1 
    for name in all_names:
        # if string is empty we've found an empty cell inbetween names
        if not name:
            break
        col_counter += 1
    # if no empty cells found inbetween names the col_counter will be at cell after all names 
    try:
        empty_cell = worksheet.cell(after_cell.row, col_counter)
    # if we encounter an APIError we've run out of columns and need to allocate more
    except GSpreadException: 
        worksheet.add_cols(10)
        empty_cell = worksheet.cell(after_cell.row, col_counter)
    # return cell based on return format
    if 'a1' in return_format:
        return_val = rowcol_to_a1(empty_cell.row, empty_cell.col)
    elif 'cell' in return_format:
        return_val = empty_cell
    elif 'rowcol' in return_format:
        return_val = empty_cell.row, empty_cell.col
    else:
        raise Exception("ERROR: Unknown format requested : '{0}'. Expected one of : 'a1', 'cell', 'rowcol'.".format(return_format))
    return return_val


def add_user(worksheet: Worksheet, username: str) -> str:
    try: 
        worksheet.find(username)
    except CellNotFound:
        names_cell = worksheet.find("Names")
        empty_cell_a1 = get_next_empty_cell_after_cell(worksheet, names_cell, return_format="a1")
        worksheet.update_acell(empty_cell_a1, username)
    else:
        raise Exception("ERROR: User '{0}' already exists.".format(username))


# points_logger_sheet = get_spreadsheet("Points Logger")
# current_month = get_current_month_name()
# current_worksheet = get_worksheet(points_logger_sheet, current_month)

# print(add_user(current_worksheet, "boop"))
