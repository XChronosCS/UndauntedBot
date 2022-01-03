import gspread
import random
import pygsheets

LEVEL_COLUMN = 1
NAME_ROW = 2
TYPE_ROW = 3
EXPLO_MOD = 3
ADV_MOD = 23
EVENT_MOD = 3
ANDIEL_MOD = 4
GARDENS_MOD = 73

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

sh = gc.open("Data Encounter Sheet")
ws = pg.open("Data Encounter Sheet")
encounters = sh.worksheet("Encounter Tables")
notesheet = ws.worksheet_by_title("Encounter Tables")
events = sh.worksheet("Area Events")
event_notes = ws.worksheet_by_title("Area Events")

area_names = encounters.row_values(2)
e_area_names = events.row_values(2)


def find_mon(area, roll, pl=None):
    ret_string = None
    selection = None
    note = None
    level_mod = None
    modifier = 0
    if area in area_names:
        area_cell = encounters.find(area)
        if "Andeil Forest" in area_cell.value:
            modifier = ANDIEL_MOD
        elif "Gabrien Gardens" in area_cell.value:
            modifier = GARDENS_MOD
        elif encounters.cell(TYPE_ROW, area_cell.col).value == 'Exploration':
            modifier = EXPLO_MOD
        else:
            modifier = ADV_MOD
        select_cell = encounters.cell(int(roll) + modifier, area_cell.col)
        note_check = notesheet.cell((select_cell.row, select_cell.col))
        if note_check.note is not None:
            note = "\nNote: " + note_check.note
        else:
            note = ''
        selection = select_cell.value
        level_mod = encounters.cell(select_cell.row, LEVEL_COLUMN).value
        if pl is not None:
            level_mod = eval(pl + level_mod)
    else:
        return "This encounter area does not exist. Please try again."
    ret_array = [area, roll, selection, level_mod, note]
    if "Non-Valid" in selection:
        ret_string = "In {0[0]}, a roll of {0[1]} is a {0[2]}".format(ret_array)
    else:
        ret_string = "{0[2]} Level {0[3]}".format(ret_array)
    return ret_string


def roll_exploration(area, sk, tl, pl):
    luck_roll = random.randint(1, 20)
    note_roll = random.randint(1, 4)
    swarm_flag = True if int(tl) > 15 else False
    swarm_check = True if luck_roll == 1 else False
    note_flag = True if luck_roll == 20 else False
    sc_array = [False, False, False]  # in order: 1 Below, 1 Above, 2 Above
    ret_string = 'Encounter Stating Results:\nYou Rolled a {0} for your luck roll.\n\nYour Options are '.format(str(luck_roll))
    skill = int(sk)
    if 11 > skill > 6:
        sc_array[0] = True
    if 16 > skill > 10:
        sc_array[1] = True
    if 21 > skill > 15:
        sc_array[0] = True
        sc_array[1] = True
    if skill > 20:
        sc_array[0] = True
        sc_array[1] = True
        sc_array[2] = True
    if sc_array[0]:
        t1 = luck_roll - 1
        if t1 == 1:
            swarm_check = True
        ret_string += find_mon(area, str
(t1), pl) + ", "
    ret_string += find_mon(area, str(luck_roll), pl)
    if note_flag:
        ret_string += " Option {0}".format(str(note_roll))
    if sc_array[1] and luck_roll < 20:
        t2 = str(luck_roll + 1)
        ret_string += ", " + find_mon(area, t2, pl)
    if sc_array[2] and luck_roll < 19:
        t3 = str(luck_roll + 2)
        ret_string += ", " + find_mon(area, t3, pl)
    if swarm_flag and swarm_check:
        ret_string += "\n\n You are a high enough level to qualify for a swarm encounter. If chosen, have your GM roll 2 " \
                      "more pokemon for the encounter."
    return ret_string
  
  
  
def choose_event(area):
    dice_roll = None
    event_name = None
    note = None
    if area in area_names:
        area_cell = events.find(area)
        if events.cell(TYPE_ROW, area_cell.col).value == 'Exploration':
            dice_roll = random.randint(1, 10) + EVENT_MOD
        else:
            dice_roll = random.randint(1, 20) + EVENT_MOD
        event_name = events.cell(dice_roll, area_cell.col).value
        print(event_name)
        note_check = event_notes.cell((dice_roll, area_cell.col))
        if note_check.note is not None:
            note = "\nNote: " + note_check.note
        else:
            note = ''
    else:
        return "This encounter area does not exist. Please try again."
    ret_array = [dice_roll - EVENT_MOD, event_name, note]
    ret_string = "Event {0[0]}: {0[1]}\n{0[2]}".format(ret_array)
    return ret_string
  
  
  