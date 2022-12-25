import gspread
import pygsheets

from gspread_credentials import *

gc = gspread.service_account_from_dict(credentials)
pg = pygsheets.authorize(service_file='UndauntedBot/service_account_credentials.json')
sh = gc.open("Data Encounter Sheet")
ws = pg.open("Data Encounter Sheet")
statter = sh.worksheet("Template")
copy_sheet = ws.worksheet_by_title("Template")
