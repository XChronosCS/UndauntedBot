import random
import re

import gspread
import pygsheets

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
at_notes = ws.worksheet_by_title("Adventure Tables")
ex_events = sh.worksheet("Exploration Area Events ")
ex_event_notes = ws.worksheet_by_title("Exploration Area Events")
ad_events = sh.worksheet("Adventure Area Events ")
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
secret_events = secret_areas.worksheet("Area Events")
sa_notes = secret_areas_notes.worksheet_by_title("Adventure Tables")
se_notes = secret_areas_notes.worksheet_by_title("Area Events")


def get_mon(area, slot, sheet, note_sheet, treasure_flag=False):
    criteria = re.compile('(?i)^' + area + "$")
    area_match = sheet.find(criteria, in_row=1)
    slot_match = sheet.find(slot, in_column=1)
    if area_match is None:
        return "There is no area with this name. Please try again"
    if slot_match is None:
        return "Please enter a valid encounter slot number."
    match = sheet.cell(slot_match.row, area_match.col)
    if match.value is None:
        return "This area does not have that many slots. Please try again."
    note_check = note_sheet.cell((match.row, match.col))
    ret_string = "Encounter in slot {0}".format(slot) + " of area {0} is: ".format(area) + match.value + "\n"
    if note_check.note is not None:
        ret_string += "**Note:**\n" + note_check.note + "\n"
        if "treasure" in note_check.note.lower():
            if treasure_flag:
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


def get_non_treasure(area_col, sheet, notes_sheet, min_lim=1, max_lim=100):
    slot_num = str(random.randint(min_lim, max_lim))
    slot_match = sheet.find(slot_num, in_column=1)
    match = sheet.cell(slot_match.row, area_col)
    while (notes_sheet.cell((match.row, match.col)).note is not None and "treasure" in notes_sheet.cell(
            (match.row, match.col)).note.lower()) or match.value is None:
        slot_num = random.randint(min_lim, max_lim)
        slot_match = sheet.find(slot_num, in_column=1)
        match = sheet.cell(slot_match.row, area_col)
    return match.value


def get_hidden_slot_adventure(area, slot):
    return get_mon(area, slot, secret_adventures, sa_notes, True)


def get_hidden_event_adventure(area, slot):
    return get_event(area, slot, secret_events, se_notes)


def roll_exploration(area, tl, pl, luck_roll=None, event=None, rep_array=None, bait_mons=0, extra_players=0):
    ret_string = ""
    max_val = 30
    min_val = 1 if tl >= 16 else 2
    if luck_roll is None:
        luck_roll = str(random.randint(min_val, max_val))
        slot_match = exploration_table.find(luck_roll, in_column=1)
        if slot_match is None:
            max_val = 20
            luck_roll = str(random.randint(min_val, max_val))
            slot_match = exploration_table.find(luck_roll, in_column=1)
            if slot_match is None:
                max_val = 15
                luck_roll = str(random.randint(min_val, max_val))
        if rep_array is not None:
            while luck_roll in rep_array:
                luck_roll = str(random.randint(1, max_val))
    ret_string += get_mon(area, luck_roll, exploration_table, et_notes)
    criteria = re.compile('(?i)^' + area + "$")
    area_match = exploration_table.find(criteria, in_row=1)
    if extra_players != 0 and bait_mons != 0:
        extra_mons = bait_mons + extra_players
        for i in range(0, extra_mons):
            ret_string += "Extra Pokemon {0} of {1} is: ".format(i, extra_mons) + get_non_treasure(area_match.col,
                                                                                                   exploration_table,
                                                                                                   et_notes,
                                                                                                   min_val,
                                                                                                   max_val) + "\n"
    if event is None:
        event = str(random.randint(1, 10))
    ret_string += get_event(area, event, ex_events, ex_event_notes) + find_disposition(area)
    return ret_string


def roll_adventure(area, tl, pl, th=None, target=None, force_mon=None, force_event=None, extra_players=0):
    #     encounter_roll = None
    #     treasure_guardian = None
    #     encounter = None
    #     event = None
    #     disposition = None
    #     treasure_flag = False
    #     ex_treasure_flag = False
    #     ret_string = ''
    #     alpha_flag = False
    #     num_treasure_hunts = 0
    #     guardianFlag = True if int(tl) >= 20 else False
    #     majorTreasureFlag = True if int(pl) >= 45 else False
    #     if force_mon is None:
    #         if majorTreasureFlag:
    #             encounter_roll = random.randint(1, 50)
    #         else:
    #             encounter_roll = random.randint(2, 50)
    #         if encounter_roll in TREASURE_SLOTS:
    #             treasure_flag = True
    #             if encounter_roll == 50:
    #                 alpha_flag = True
    #             else:
    #                 treasure_guardian = find_mon(area, str(roll_exclude()), pl)
    #         if th is not None and target is not None and str(encounter_roll) != target:
    #             starting_val = 1 if majorTreasureFlag else 2
    #             treasure_array = numpy.random.randint(starting_val, 50, size=int(th) * 3)
    #             if int(target) in treasure_array:
    #                 if int(target) == 50:
    #                     alpha_flag = True
    #                 else:
    #                     alpha_flag = False
    #                 encounter_roll = int(target)
    #                 num_treasure_hunts = int(math.ceil(treasure_array.tolist().index(int(target)) / 3))
    #             else:
    #                 num_treasure_hunts = int(th)
    #     else:
    #         encounter_roll = int(force_mon)
    #         if encounter_roll in TREASURE_SLOTS:
    #             treasure_flag = True
    #             if encounter_roll == 50:
    #                 alpha_flag = True
    #             else:
    #                 treasure_guardian = find_mon(area, str(roll_exclude()), pl)
    # #
    #     encounter = find_mon(area, str(encounter_roll), pl)
    #     ret_string += "Encounter 1: " + encounter[0]
    #     if encounter[1] != "":
    #         ret_string += encounter[1]
    #     if treasure_flag:
    #         if alpha_flag:
    #             alpha_mon = find_mon(area, str(roll_exclude()), pl)
    #             ret_string += "\nAlpha Mon Selected is: " + alpha_mon[0] + alpha_mon[1]
    #             alpha_flag = False
    #         else:
    #             ret_string += "\nThe treasure guardian is: " + treasure_guardian[0] + treasure_guardian[1]
    #     if extra_players > 0:
    #         ret_string += "\n\nNow rolling encounters for additional players...\n"
    #         encounter_num = int(extra_players)
    #         additional_mons = None
    #         if treasure_flag:
    #             additional_mons = [roll_exclude() for i in range(encounter_num)]
    #             treasure_flag = False
    #         else:
    #             additional_mons = [roll_exclude() for i in range(encounter_num - 1)]
    #             if majorTreasureFlag:
    #                 additional_mons.append(random.randint(1, 50))
    #             else:
    #                 additional_mons.append(random.randint(2, 50))
    #             if additional_mons[-1] == 50:
    #                 alpha_flag = True
    #             else:
    #                 treasure_guardian = find_mon(area, str(roll_exclude()), pl)
    #         i = 2
    #         print(additional_mons)
    #         for x in additional_mons:
    #             if x in TREASURE_SLOTS:
    #                 ex_treasure_flag = True
    #             additional_encounter = find_mon(area, str(x), pl)
    #             ret_string += "Encounter {0}: ".format(i) + additional_encounter[0] + additional_encounter[1] + "\n"
    #             i += 1
    #             if ex_treasure_flag:
    #                 if alpha_flag:
    #                     alpha_mon = find_mon(area, str(roll_exclude()), pl)
    #                     ret_string += "\nAlpha Mon Selected is: " + alpha_mon[0] + alpha_mon[1] + "\n"
    #                 else:
    #                     ret_string += "\nThe treasure guardian is: " + treasure_guardian[0] + treasure_guardian[1] + "\n"
    #     if force_event is not None:
    #         ret_string += "\n\nArea Event: " + choose_event(area, pl, tl, force_event)
    #     else:
    #         ret_string += "\n\nArea Event: " + choose_event(area, pl, tl)
    #     if th is not None:
    #         ret_string += "\n\nYou Treasure Hunted {0} times and got these results".format(num_treasure_hunts)
    #         ret_string += "\nHere are the treasure hunt rolls: " + ", ".join([str(num) for num in treasure_array.tolist()])
    #     ret_string += find_disposition(area)
    #     return ret_string

    return "This Command is not in service at the moment. Please try again later."


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
            note = "\nNote:\n" + note_check.note
        else:
            note = ''
        selection = select_cell.value
        level_mod = encounters.cell(select_cell.row, LEVEL_COLUMN).value
        if pl is not None:
            level_mod = eval(pl + level_mod) if roll != 1 else "???"
    else:
        return "This encounter area does not exist. Please try again."
    ret_array = [area, roll, selection, level_mod, note]
    if "Non-Valid" in selection:
        ret_string = "In {0[0]}, a roll of {0[1]} is a {0[2]}".format(ret_array)
    else:
        ret_string = "{0[2]} Level {0[3]}".format(ret_array)
    return ret_string, ret_array[4]


def roll_harvest_table(area):
    criteria = re.compile('(?i)^' + area + "$")
    area_match = harvest.find(criteria, in_row=1)
    match = harvest.cell(random.randint(2, 11), area_match.col)
    if match is None:
        return "This area does not exist. Please try again."
    ret_string = match.value
    harvest_desc = h_notes.cell((match.row, match.col))
    if harvest_desc.note is not None:
        ret_string += "\nDescription: " + harvest_desc.note + "\n"
    return ret_string


def find_disposition(area):
    criteria = re.compile('(?i)^' + area + "$")
    area_match = exploration_table.find(criteria, in_row=1)
    roll = random.randint(2, 6)
    match = disp_sheet.cell(roll, area_match.col)
    if match is None:
        return "This area does not exist. Please try again"
    return "\n\nThe starting disposition of this encounter is " + match.value


def choose_event(area, pl=None, tl=0, event_choice=None):
    dice_roll = None
    event_name = None
    note = None
    alpha_check = False
    swarm_check = False
    if area in area_names:
        area_cell = events.find(area)
        if event_choice is None:
            if events.cell(TYPE_ROW, area_cell.col).value == 'Exploration':
                if event_choice is None:
                    dice_roll = random.randint(1, 10) + EVENT_MOD
                if dice_roll - EVENT_MOD == 10:
                    alpha_check = True
                if dice_roll - EVENT_MOD == 1:
                    swarm_check = True
            else:
                dice_roll = random.randint(1, 20) + EVENT_MOD
                if dice_roll - EVENT_MOD == 20 and int(tl) < 20:
                    dice_roll = random.randint(1, 19) + EVENT_MOD
        else:
            dice_roll = int(event_choice) + EVENT_MOD
            if dice_roll - EVENT_MOD == 10 and area != "Grand Performance Hall":
                alpha_check = True
            if dice_roll - EVENT_MOD == 20 and int(tl) < 20:
                dice_roll = random.randint(1, 19) + EVENT_MOD
        event_name = events.cell(dice_roll, area_cell.col).value
        note_check = event_notes.cell((dice_roll, area_cell.col))
        if note_check.note is not None:
            note = "\n" + note_check.note
        else:
            note = ''
    else:
        return "This encounter area does not exist. Please try again."
    ret_array = [dice_roll - EVENT_MOD, event_name, note]
    ret_string = "Event {0[0]}: {0[1]}\n{0[2]}".format(ret_array)
    if alpha_check and pl is not None:
        alpha_roll = random.randint(2, 20)
        alpha_tuple = find_mon(area, str(alpha_roll), pl)
        alpha_mon = alpha_tuple[0].split()
        alpha_mon[-1] = str(eval(pl + "+ 5"))
        alpha = " ".join(alpha_mon)
        ret_string += "Your Alpha Pokemon is " + alpha
        if alpha_roll == 20:
            ret_string += " Option {0}".format(str(random.randint(1, 5)))
        if alpha_tuple[1] != "":
            ret_string += "\n{0[0]} Note: \n{0[1]}".format(alpha_tuple)
    if swarm_check and pl is not None:
        swarm = [find_mon(area, str(random.randint(2, 20)), pl)[0], find_mon(area, str(random.randint(2, 20)), pl)[0]]
        ret_string += "\nAdditional Swarm Pokemon are: {0[0]}, {0[1]}\n".format(swarm)
    return ret_string


def get_new_area_details(slot, event):
    van_var = 942329291549589544
    column = 0
    if slot not in range(1, 51) or (event is not None and event not in range(1, 21)):
        return "The encounter table slot or event slot are not valid choices. Please try again."
    if slot < 26:
        column = 10
    else:
        column = 12
    match = sunken.find(str(slot), in_column=column)
    if event is not None:
        e_match = sunken.find(str(event), in_column=15)
        event_cell = sunken.cell(e_match.row, 16)
        event_note = sunken_notes.cell((event_cell.row, event_cell.col))
    encounter = sunken.cell(match.row, column + 1)
    note_check = sunken_notes.cell((encounter.row, encounter.col))
    ret_string = ""
    ret_string += "Encounter in slot {0}: ".format(slot) + encounter.value + "\n"
    if note_check.note is not None:
        ret_string += "Note: " + note_check.note + "\n"
    if event is not None:
        ret_string += "\nEvent in slot {0}: ".format(event) + event_cell.value + "\n\n" + event_note.note
    ret_string += "\n" + f"<@&" + "{0}>".format(van_var)
    return ret_string
