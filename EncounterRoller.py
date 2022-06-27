import random
import re
import numpy as np
import gspread
import pygsheets
import time
import math

LEVEL_COLUMN = 1
NAME_ROW = 2
TYPE_ROW = 3
EXPLO_MOD = 3
ADV_MOD = 23
EVENT_MOD = 3
ANDIEL_MOD = 4
GARDENS_MOD = 73
TREASURE_SLOTS = [1, 10, 20, 30, 40, 50]

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

sh = gc.open("Encounter Tables Data Doc")
ws = pg.open("Encounter Tables Data Doc")
exploration_table = sh.worksheet("Exploration Tables")
et_notes = ws.worksheet_by_title("Exploration Tables")
adventure_table = sh.worksheet("Adventure Tables")
ad_notes = ws.worksheet_by_title("Adventure Tables")
ex_events = sh.worksheet("Exploration Area Events")
ex_event_notes = ws.worksheet_by_title("Exploration Area Events")
ad_events = sh.worksheet("Adventure Area Events")
ad_event_notes = ws.worksheet_by_title("Adventure Area Events")
disp_sheet = sh.worksheet("Disposition Tables")
harvest = sh.worksheet("Harvest Tables")
h_notes = ws.worksheet_by_title("Harvest Tables")
sk = gc.open("Test Sunken City")
wk = pg.open("Test Sunken City")
sunken = sk.worksheet("Sunken City")
sunken_notes = wk.worksheet_by_title("Sunken City")
secret_areas = gc.open("New Encounter Areas")
secret_areas_notes = pg.open("New Encounter Areas")
secret_adventures = secret_areas.worksheet("Adventure Tables")
secret_explorations = secret_areas.worksheet("Exploration Tables")
secret_events = secret_areas.worksheet("Area Events")
sa_notes = secret_areas_notes.worksheet_by_title("Adventure Tables")
sx_notes = secret_areas_notes.worksheet_by_title("Exploration Tables")
se_notes = secret_areas_notes.worksheet_by_title("Area Events")
explo_names = secret_explorations.row_values(1)
time.sleep(60)
adven_names = secret_adventures.row_values(1)


def get_mon(area, slot, sheet, note_sheet, non_treasure_flag=True):
    criteria = re.compile('(?i)^' + area + "$")
    area_match = sheet.find(criteria, in_row=1)
    slot_match = sheet.find(str(slot), in_column=1)
    if area_match is None:
        return "There is no area with this name. Please try again"
    if slot_match is None:
        return "Please enter a valid encounter slot number."
    match = sheet.cell(slot_match.row, area_match.col)
    if match.value is None:
        return "This area does not have that many slots. Please try again."
    note_check = note_sheet.cell((match.row, match.col))
    ret_string = "Encounter in slot {0}".format(slot) + "  of area {0} is: ".format(area) + match.value + "\n"
    if note_check.note is not None:
        ret_string += "**Note:**\n" + note_check.note + "\n"
        if "treasure" in note_check.note.lower() or "abberation" in note_check.note.lower():
            if not non_treasure_flag:
                ret_string += "\nPokemon accompanying Treasure / Pokemon that is Abberated is {0}\n\n".format(
                    get_non_treasure(area_match.col, sheet, note_sheet))
            else:
                new_mon = sheet.find(get_non_treasure(area_match.col, sheet, note_sheet), in_column=area_match.col)
                return get_mon(area, new_mon.row, sheet, note_sheet)

        if "Check Note" in match.value:
            ret_string += "\nThe d5 roll for the Rare Pokemon is {0}\n\n".format(random.randint(1, 5))
    return ret_string


def get_event(area, slot, sheet, note_sheet):
    criteria = re.compile('(?i)^' + area + "$")
    area_match = sheet.find(criteria, in_row=1)
    slot_match = sheet.find(slot, in_column=1)
    if area_match is None:
        return "There is no area with this name. Please try again."
    if slot_match is None:
        return "Please enter a valid event slot number."
    match = sheet.cell(slot_match.row, area_match.col)
    if match.value is None:
        return "This area does not have that many events. Please try again."
    note_check = note_sheet.cell((match.row, match.col))
    ret_string = ""
    ret_string += "Event in slot {0}".format(slot) + " of area {0} is: ".format(area) + match.value + "\n"
    if note_check.note is not None:
        ret_string += "\n**Description:** " + note_check.note + "\n"
    return ret_string


def get_non_treasure(area_col, sheet, notes_sheet, min_lim=1, max_lim=100, slot_rev=False):
    slot_num = str(random.randint(min_lim, max_lim))
    slot_match = sheet.find(slot_num, in_column=1)
    match = sheet.cell(slot_match.row, area_col)
    while (notes_sheet.cell((match.row, match.col)).note is not None and "treasure" in notes_sheet.cell(
            (match.row, match.col)).note.lower()) or match.value is None:
        slot_num = random.randint(min_lim, max_lim)
        slot_match = sheet.find(str(slot_num), in_column=1)
        match = sheet.cell(slot_match.row, area_col)
    ret_string = ""
    if slot_rev:
        ret_string += "Slot Number {0}: ".format(slot_num)
    ret_string += match.value
    return ret_string


def get_hidden_slot_adventure(area, slot):
    if any(area.lower() == val.lower() for val in adven_names):
        return get_mon(area, slot, secret_adventures, sa_notes, False)
    return get_mon(area, slot, secret_explorations, sx_notes, False)


def get_hidden_event_adventure(area, slot):
    return get_event(area, slot, secret_events, se_notes)
  

def roll_hidden_adventure(area, tl, pl, luck_roll=None, event=None, rep_array=None, bait_mons=0, extra_players=0,
                   th_attempts=None, th_target=None):
    treasure_flag = False
    ret_string = ''
    guardianFlag = True if int(tl) >= 20 else False
    majorTreasureFlag = True if int(pl) >= 45 else False
    th_hits = None
    max_val = 100
    min_val = 1 if majorTreasureFlag else 2
    criteria = re.compile('(?i)^' + area + "$")
    area_match = secret_adventures.find(criteria, in_row=1)
    if area_match is None:
        return "There is no area with this name. Please try again"
    if luck_roll is None:
        luck_roll = str(random.randint(min_val, max_val))
        slot_match = secret_adventures.find(luck_roll, in_column=area_match.col)
        if slot_match is None:
            max_val = 50
            luck_roll = str(random.randint(min_val, max_val))
            slot_match = secret_adventures.find(luck_roll, in_column=area_match.col)
        if rep_array is not None:
            while luck_roll in rep_array:
                luck_roll = str(random.randint(min_val, max_val))
        if th_attempts is not None:
            th_hits = []
            for i in range(0, int(th_attempts)):
                th_roll = np.random.randint(min_val, max_val, 3)
                th_hits += th_roll.tolist()
                if int(th_target) in th_roll:
                    luck_roll = str(th_target)
                    break
    ret_string += get_mon(area, luck_roll, secret_adventures, sa_notes)
    if "treasure" in ret_string.lower():
        treasure_flag = True
    if extra_players != 0 or bait_mons != 0:
        extra_mons = bait_mons + extra_players
        for i in range(0, extra_mons):
            if i == 3:
                time.sleep(60) 
            ret_string += "Extra Encounter {0} of {1} is: ".format(i + 1, extra_mons) + get_mon(area,
                                                                                                str(random.randint(min_val,
                                                                                                               max_val)),
                                                                                                secret_adventures,
                                                                                                sa_notes,
                                                                                                treasure_flag) + "\n"
            if "treasure" in ret_string.lower() and treasure_flag == False:
                treasure_flag = True
    if event is None:
        event = str(random.randint(1, 20))
    event_rolled = get_event(area, event, secret_events, se_notes)
    swarm_addition = ""
    if "Guardian Encounter" in event_rolled and not guardianFlag:
        event_rolled = get_event(area, str(random.randint(1, 20)), secret_events, se_notes)
    if "Major Pokemon Swarm" in event_rolled:
        for i in range(0, (int(math.ceil(int(tl)/15)))):
            swarm_addition += "Swarm Pokemon {0} of {1} is: ".format(i + 1, (int(math.ceil(int(tl)/15)))) + get_non_treasure(area_match.col,
                                                                                                   secret_adventures,
                                                                                                   sa_notes,
                                                                                                   min_val,
                                                                                                   max_val, True) + "\n"
    ret_string += event_rolled + swarm_addition + find_disposition(area)
    if th_hits is not None:
        ret_string += "\n\nHere are the treasure hunt rolls: " + ", ".join([str(num) for num in th_hits])
    return ret_string
  


def roll_exploration(area, tl, pl, luck_roll=None, event=None, rep_array=None, bait_mons=0, extra_players=0):
    ret_string = ""
    max_val = 30
    min_val = 1 if tl >= 16 else 2
    criteria = re.compile('(?i)^' + area + "$")
    area_match = exploration_table.find(criteria, in_row=1)
    if area_match is None:
        return "There is no area with this name. Please try again"
    if luck_roll is None:
        luck_roll = str(random.randint(min_val, max_val))
        slot_match = exploration_table.find(luck_roll, in_column=area_match.col)
        if slot_match is None:
            max_val = 20
            luck_roll = str(random.randint(min_val, max_val))
            slot_match = exploration_table.find(luck_roll, in_column=area_match.col)
            if slot_match is None:
                max_val = 15
                luck_roll = str(random.randint(min_val, max_val))
        if rep_array is not None:
            while luck_roll in rep_array:
                luck_roll = str(random.randint(1, max_val))
    ret_string += get_mon(area, luck_roll, exploration_table, et_notes)
    if extra_players != 0 or bait_mons != 0:
        extra_mons = bait_mons + extra_players
        for i in range(0, extra_mons):
            ret_string += "Extra Pokemon {0} of {1} is: ".format(i + 1, extra_mons) + get_non_treasure(area_match.col,
                                                                                                   exploration_table,
                                                                                                   et_notes,
                                                                                                   min_val,
                                                                                                   max_val) + "\n"
    if event is None:
        event = str(random.randint(1, 10))
    ret_string += get_event(area, event, ex_events, ex_event_notes) + find_disposition(area)
    if "Pokemon Swarm" in ret_string:
        for i in range(0, 2):
            ret_string += "Swarm Pokemon {0} of {1} is: ".format(i + 1, 2) + get_non_treasure(area_match.col,
                                                                                                   exploration_table,
                                                                                                   et_notes,
                                                                                                   min_val,
                                                                                                   max_val) + "\n"
    return ret_string


def roll_adventure(area, tl, pl, luck_roll=None, event=None, rep_array=None, bait_mons=0, extra_players=0,
                   th_attempts=None, th_target=None):
    treasure_flag = False
    ret_string = ''
    guardianFlag = True if int(tl) >= 20 else False
    majorTreasureFlag = True if int(pl) >= 45 else False
    th_hits = None
    max_val = 100
    min_val = 1 if majorTreasureFlag else 2
    criteria = re.compile('(?i)^' + area + "$")
    area_match = adventure_table.find(criteria, in_row=1)
    if area_match is None:
        return "There is no area with this name. Please try again"
    if luck_roll is None:
        luck_roll = str(random.randint(min_val, max_val))
        slot_match = adventure_table.find(luck_roll, in_column=area_match.col)
        if slot_match is None:
            max_val = 50
            luck_roll = str(random.randint(min_val, max_val))
            slot_match = adventure_table.find(luck_roll, in_column=area_match.col)
        if rep_array is not None:
            while luck_roll in rep_array:
                luck_roll = str(random.randint(min_val, max_val))
        if th_attempts is not None:
            th_hits = []
            for i in range(0, int(th_attempts)):
                th_roll = np.random.randint(min_val, max_val, 3)
                th_hits += th_roll.tolist()
                if int(th_target) in th_roll:
                    luck_roll = str(th_target)
                    break
    ret_string += get_mon(area, luck_roll, adventure_table, ad_notes)
    if "treasure" in ret_string.lower():
        treasure_flag = True
    if extra_players != 0 or bait_mons != 0:
        extra_mons = bait_mons + extra_players
        for i in range(0, extra_mons):
            if i == 3:
                time.sleep(60) 
            ret_string += "Extra Encounter {0} of {1} is: ".format(i + 1, extra_mons) + get_mon(area,
                                                                                                str(random.randint(min_val,
                                                                                                               max_val)),
                                                                                                adventure_table,
                                                                                                ad_notes,
                                                                                                treasure_flag) + "\n"
            if "treasure" in ret_string.lower() and treasure_flag == False:
                treasure_flag = True
    if event is None:
        event = str(random.randint(1, 20))
    event_rolled = get_event(area, event, ad_events, ad_event_notes)
    swarm_addition = ""
    if "Guardian Encounter" in event_rolled and not guardianFlag:
        event_rolled = get_event(area, str(random.randint(1, 20)), ad_events, ad_event_notes)
    if "Major Pokemon Swarm" in event_rolled:
        for i in range(0, (int(math.ceil(int(tl)/15)))):
            swarm_addition += "Swarm Pokemon {0} of {1} is: ".format(i + 1, (int(math.ceil(int(tl)/15)))) + get_non_treasure(area_match.col,
                                                                                                   adventure_table,
                                                                                                   ad_notes,
                                                                                                   min_val,
                                                                                                   max_val) + "\n"
    ret_string += event_rolled + swarm_addition + find_disposition(area)
    if th_hits is not None:
        ret_string += "\n\nHere are the treasure hunt rolls: " + ", ".join([str(num) for num in th_hits])
    return ret_string


def roll_harvest_table(area):
    criteria = re.compile('(?i)^' + area + "$")
    area_match = harvest.find(criteria, in_row=1)
    match = harvest.cell(random.randint(2, 11), area_match.col)
    if match is None:
        return "This area does not exist. Please try again."
    ret_string = match.value + "\n"
    harvest_desc = h_notes.cell((match.row, match.col))
    if harvest_desc.note is not None:
        ret_string += "\nDescription: " + harvest_desc.note + "\n"
    return ret_string


def find_disposition(area):
    criteria = re.compile('(?i)^' + area + "$")
    area_match = disp_sheet.find(criteria, in_row=1)
    roll = random.randint(2, 6)
    match = disp_sheet.cell(roll, area_match.col)
    if match is None:
        return "This area does not exist. Please try again"
    return "\nThe starting disposition of this encounter is " + match.value + "\n"
