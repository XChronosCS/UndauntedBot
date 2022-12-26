import gspread
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from gspread_credentials import *

creds = ServiceAccountCredentials.from_json_keyfile_name('service_account_credentials.json',
                                                         scopes="https://www.googleapis.com/auth/documents.readonly")
service = build('docs', 'v1', credentials=creds)

gc = gspread.service_account_from_dict(credentials)

sh = gc.open("Data Get Test Sheet")

# Loading Worksheets for Primary Information Lookup
abilities = sh.worksheet("Abilities Data")
features = sh.worksheet("Features Data")
items = sh.worksheet("Inventory Data")
edges = sh.worksheet("Edges Data")
moves = sh.worksheet("Moves Data")
extras = sh.worksheet("Class Data")
misc = sh.worksheet("Misc Data")
habitat = gc.open("Data Habitat Areas").worksheet("Data")

worksheets = [("abilities", abilities, 1, 1, 3), ("features", features, 1, 1, 5), ("items", items, 2, 28, 29),
              ("edges", edges, 1, 1, 3), ("moves", moves, 1, 1, 9), ("mechanics", extras, 2, 1, 3),
              ("techniques", extras, 2, 4, 7),
              ("orders", features, 1, 6, 8), ("orders 2", features, 1, 9, 11), ("capabilities", misc, 1, 7, 8),
              ("keywords", misc, 1, 17, 18), ("statuses", misc, 1, 9, 10), ("maneuvers", moves, 1, 10, 15)]
infodex = {}

for worksheet in worksheets:

    # Prompt the user to enter the row number to use for the key names
    key_row_num = worksheet[2]
    start_col = worksheet[3]
    end_col = worksheet[4]

    # Get the data from the worksheet as a list of lists
    data = worksheet[1].get_all_values()

    # Get the key names from the specified row
    keys = data[key_row_num - 1][start_col - 1:end_col]

    # Initialize the dictionary to store the data
    data_dict = {}

    # Iterate over the rows of data and add them to the dictionary
    for i, row in enumerate(data):
        if i <= key_row_num - 1:
            continue  # Skip the row with the key names
        data_dict[row[start_col - 1]] = {keys[j]: row[j + start_col - 1] for j in range(len(keys))}

    infodex[worksheet[0]] = data_dict

infodex["orders"].update(infodex["orders 2"])

'''
# Iterate over the rows of data and add them to the dictionary
with open('moves.txt', 'w', encoding='utf-8') as f:
    # Write the dictionary to the file as a string
    f.write(str(infodex))
'''
