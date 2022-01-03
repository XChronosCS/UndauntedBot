import gspread
import random
import pygsheets
from constants import TYPES
import RollingCommands

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
pg = pygsheets.authorize(service_file='UndauntedBot/service_account_credentials.json')

sh = gc.open("Data Get Test Sheet")
sp = pg.open("Data Undaunted Egg Rolls")
sg = gc.open("Data Undaunted Egg Rolls")
pokemon = sh.worksheet("Poke Data")
eggs = sp.worksheet_by_title("Eggs")
# Need Temp to help find the row and column of specific cell
eggs_temp = sg.worksheet("Eggs")
p_with_megas = pokemon.col_values(1)
p_names = [x for x in p_with_megas if " Mega" not in x]
max_pokemon = len(p_names)


def exclusion(lst1, lst2):
    lst3 = [value for value in lst1 if value not in lst2]
    return lst3


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def roll_mon():
    index = random.randrange(1, max_pokemon)
    return p_names[index]


def roll_egg(p_type):
    if p_type == 'Random':
        p_type = TYPES[random.randrange(0, len(TYPES))]
    type_col = eggs_temp.find(p_type).col
    roll_list = eggs_temp.col_values(type_col)
    del roll_list[:1]
    index = random.randrange(0, len(roll_list))
    return roll_list[index]


# noinspection PyBroadException
def roll_egg_move(p_type):
    if p_type == 'Random':
        p_type = TYPES[random.randrange(0, len(TYPES))]
    first_string = roll_egg(p_type)
    cell = eggs_temp.find(first_string)
    cell_row = cell.row
    cell_col = cell.col
    n_cell = eggs.cell((cell_row, cell_col))
    note = n_cell.note
    try:
        egg_moves = note.splitlines()
        del egg_moves[:2]
        index = random.randrange(0, len(egg_moves))
        temp_list = egg_moves[index].split(" ")
        del temp_list[:1]
        ret_egg = ' '.join(temp_list)
        ret_string = first_string + " with the egg move " + ret_egg
        return ret_string
    except:
        return first_string + " with the egg move [PORY404 ERROR -> EGG MOVES NOT FOUND]"


def roll_details():
    nature = RollingCommands.nature()
    gender = RollingCommands.gender()
    ability = random.randint(1, 2)
    result_array = [nature, gender, ability]
    return "This pokemon has a {0[0]} nature, is a {0[1]} gender if allowed, and has ability option {0[2]} " \
           "if there are multiple options.".format(result_array)
