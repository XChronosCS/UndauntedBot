import gspread
import re
from constants import *


credentials = {
    "type": "service_account",
    "project_id": "undaunteddiscordbot",
    "private_key_id": "b815b93c7e0bba1070d4a2c875e4994f02d43f39",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC4eHKbjM5qeK4k\n7Wu18aGFM/QQ7HjSKNk3/qpGgA0cdPVM6iSTD/Eew+/WkttRrWn211NjLDkq86GX\nemTOeTuajoUcuitWRwOR19N79qL66RZUBZoGnlA1z/3pQfX8mrxhn7KFVBOA66fy\nArf+UoKoKZQ2Qe8G8LIQxfM+ZT9zF5k1KfmKR6bvqB38L3MRMSPStSxbFzylkwJH\n9Czq+LNnIyYmyfB0qPBYwMlEDT2aPi7hzWXku9iX2qQwua0+lYOSeVyPeFfm3JJX\nwP+/iON4DU3Qq+5BBe67shoz2CbGtDphF3fHX0i6gxWv7fvaYta0xyGYXMVdYD1W\n8sftBDKPAgMBAAECggEAF0siUbEEiZ5GgyQ1wypJVowaaB6sHQGKeE8gijl2Ll84\ncGdqieVr8ZIVUXeG2Tf4FvLWtUGq0FkmUP3kB8x4McqIVXnOqhzafwqNSmx45Q0U\nxDRW4DoSb9EdQ1yQZr7VRdCIFtzof5GCSgV83VDm7bweWoGV4L75BTQxxHG9gtdD\nJJ5BAwkGLblR5j9gqU1jYLhMN/WjK8BIyBrfAvIHANjv4rLK+jjj4Ut5h4CxsxpW\n/Aqwti7T0NwiCLERhbIENkNxbFd7hr4q+yjoCW23LCUbjnx1XdiIlJuKbty8iQsu\nBYNKXvolEHv8FEzKdSSz9Nvi4esl6Hm9Dg7pBiJuRQKBgQD4Gd1L21w3q49kdh16\no0j4GKtzy2dxxVbNi3OMcUYbvX3TwUees0iG+WBcX2I9TRTzsDUbRW4oZftGJ88s\nriTwO1aV2CzDTMBgnalkqVjP9c6/RlRgpHsjB8K2ujqIkTxeH+vbQzzO4Fj98ff3\nl+PGttktlxEkdKy/Roek8T/uqwKBgQC+V/czrvMRom6Ugh4RltEGrdgicVgemqYk\nDO2LVlKWlXZ2zW26FQcxXA5AuB13/nZFd7vfvzIoC6OK/QS6a10DITJIwbE0ex9/\nUQK0DlqAAEN8EcoAJzm32pmHMTE90rvGhFnQ4VsZw9vnQjIBqcw52DmYsSCSpO8m\nJ29bUGu7rQKBgBADa1soD22wbxLm5MQzodQRk49nw4d+WzntFEouTX4g3uw5/2to\n2veLRQLxTR/zx7Rq3SKjepa07mD61M5ndw7iZZZKW6lHXOtfgb1ziL3zeaKy4WNT\nencqWxD8OCb0aNcSbGC8mEIqDNRnN8ANV7BNwPrGU17tAPFflgW5ZIz9AoGAbsIT\nB1D7Abzp6aKZSpTexqssBEa+BvjoSjv3kcfGQPdxuompGsmXqOIvLPu1shgwzBVz\nDixcTC8RmBPIx40nz2VmtC15JteqKVSDZTCg+rCslCppx5MLo+8gvSkjxRy1xTtI\nZCJt910fvb6oCI28V8B5K1+OW6Z7vlDeHF18gvUCgYBJZ0B6zhIdGyCBQ+I4gDxh\n1FfviL35Wz0qJxHnyEAnjm4X33p6jDzNyVrwr6lJyL3ixFm77y7Qes6asF9s61UF\n51GJrjLRCcC+9X1WSmB1rGM+W76SUXKBxrwj0mNe922rm+lgJPRAx7jkjVvAeRMe\nkFtJXHo5iVWUSEVV5MW6lw==\n-----END PRIVATE KEY-----\n",
    "client_email": "undaunted@undaunteddiscordbot.iam.gserviceaccount.com",
    "client_id": "112647756200358490521",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/undaunted%40undaunteddiscordbot.iam.gserviceaccount.com"
}

gc = gspread.service_account_from_dict(credentials)

sh = gc.open("Data Get Test Sheet")
abilities = sh.worksheet("Abilities Data")
features = sh.worksheet("Features Data")
items = sh.worksheet("Inventory Data")
edges = sh.worksheet("Edges Data")
moves = sh.worksheet("Moves Data")


def get_ability_data(name):
    match = abilities.find(name, in_column=1)
    if match is None:
        return ["There is no ability by that name"]
    else:
        row = match.row
        ability_name = abilities.cell(row, 1).value
        ability_freq = "\n" + abilities.cell(row, 2).value
        ability_eff = "\n" + abilities.cell(row, 3).value
        return [ability_name, ability_freq, ability_eff]


def get_feature_data(name):
    print(name)
    match = features.find(name, in_column=1)
    if match is None:
        return ["There is no feature by that name"]
    else:
        row = match.row
        feature_name = features.cell(row, 1).value
        feature_pre = "\n" + features.cell(row, 2).value
        feature_tag = "\n" + features.cell(row, 3).value
        feature_freq = "\n" + features.cell(row, 4).value
        feature_eff = "\n" + features.cell(row, 5).value
        return [feature_name, feature_pre, feature_tag, feature_freq, feature_eff]


def get_item_data(name):
    match = items.find(name, in_column=28)
    if match is None:
        return ["There is no item by that name"]
    else:
        row = match.row
        item_name = items.cell(row, 28).value
        item_eff = "\n" + items.cell(row, 29).value
        return [item_name, item_eff]


def get_edge_data(name):
    match = edges.find(name, in_column=1)
    if match is None:
        return ["There is no edge by that name"]
    else:
        row = match.row
        edge_name = edges.cell(row, 1).value
        edge_freq = "\n" + edges.cell(row, 2).value
        edge_eff = "\n" + edges.cell(row, 3).value
        return [edge_name, edge_freq, edge_eff]


def get_move_data(name):
    if name == "Roar Of Time":
        name = "Roar of Time"
    if name == "Cone Of Force":
        name = "Cone of Force"
    match = moves.find(name, in_column=1)
    if match is None:
        return ["There is no move by that name"]
    else:
        row = match.row
        move_name = "Name: " + moves.cell(row, 1).value
        move_type = "\nType: " + moves.cell(row, 2).value
        move_class = "\n" + moves.cell(row, 3).value
        move_freq = "\n" + moves.cell(row, 4).value
        move_range = "\n" + moves.cell(row, 5).value
        move_ac = "\nAC: " + str(moves.cell(row, 6).value)
        move_db = "\nDB: " + str(moves.cell(row, 7).value)
        move_eff = "\nEffect: " + moves.cell(row, 8).value
        move_tag = "\nStyle Tag: " + moves.cell(row, 9).value
        return [move_name, move_type, move_class, move_freq, move_range, move_ac, move_db, move_eff, move_tag]
      
      
habitat = gc.open("Data Habitat Areas").worksheet("Data")


def get_habitat(name):
    match = habitat.find(name, in_column=1)
    if match is None:
        return "This is either not the species's basic form or it cannot be found anywhere at the moment."
    else:
        row = match.row
        ret_array = []
        areas = habitat.range(row, 3, row, 12)
        for x in areas:
            if x.value is not None and x.value != '':
                ret_array.append(x.value)
        ret_string = "This pokemon is found in the following locations: " + ", ".join(ret_array)
        return ret_string


def get_keyword_moves(name):
    criteria = re.compile(name)
    match = moves.findall(criteria, in_column=5)
    if len(match) != 0:
        ret_array = []
        for x in match:
            ret_array.append(moves.cell(x.row, 1).value)
        ret_string = "Here is a list of all moves with that keyword: " + ", ".join(ret_array)
        return ret_string
    else:
        return "That is not a valid attack Keyword. Please try again"
      

def poke_ability(name):
    temp_name = name.title() if name.lower() != "power of alchemy" else "Power of Alchemy"
    ret_array = [pokemon['name'].title() for pokemon in ALLPOKEMON if temp_name in pokemon['abilities'] or temp_name in pokemon['advabilities'] or temp_name in pokemon['highabilities']]
    ret_string = "**Here is a list of all the pokemon with the ability " + temp_name + ":** " + ", ".join(ret_array)
    return ret_string
  
  
  
def poke_moves(name):
    first_name = name.title() if name.lower() != "Roar of Time" else "Roar of Time"
    temp_name = name.title() if name.lower() != "Light of Ruin" else "Light of Ruin"
    ret_array = [pokemon['name'].title() for pokemon in ALLPOKEMON if any(temp_name in full_name for full_name in pokemon["moves"])]
    ret_string = "**Here is a list of all the pokemon with the level up move " + temp_name + ":** " + ", ".join(ret_array)
    return ret_string