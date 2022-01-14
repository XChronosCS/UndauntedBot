import gspread
import random
import pygsheets
import numpy
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

sh = gc.open("Data Encounter Sheet")
ws = pg.open("Data Encounter Sheet")
encounters = sh.worksheet("Encounter Tables")
notesheet = ws.worksheet_by_title("Encounter Tables")
events = sh.worksheet("Area Events")
event_notes = ws.worksheet_by_title("Area Events")
disp_sheet = sh.worksheet("Disposition")
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


def find_disposition(area):
    dispo = ''
    ret_string = ''
    # Altar of Dreams 3 roll is roll again
    if area in area_names:
        area_cell = disp_sheet.find(area)
        roll = random.randint(1, 5)
        dispo += disp_sheet.cell(roll+1, area_cell.col).value
    else:
        return "This area does not exist. Please try again"
    return "\n\nThe starting disposition of this encounter is " + dispo


def roll_exploration(area, sk, tl, pl, author_note):
    luck_roll = random.randint(1, 20)
    note_roll = random.randint(1, 5)
    swarm_flag = True if int(tl) > 15 else False
    if swarm_flag:
        luck_roll = random.randint(2, 20)
    swarm_check = True if luck_roll == 1 else False
    note_flag = True if luck_roll == 20 else False
    sc_array = [False, False, False]  # in order: 1 Below, 1 Above, 2 Above
    note_array = ["", "", "", ""]
    ret_string = 'Encounter Stating Results:\nYou Rolled a {0} for your luck roll.\n\nYour Options are '.format(
        str(luck_roll))
    skill = int(sk)
    if 11 > skill > 6:
        sc_array[0] = True
        note_array[0] = str(note_roll - 1)
    if 16 > skill > 10:
        sc_array[1] = True
        note_array[1] = str(note_roll + 1)
    if 21 > skill > 15:
        sc_array[0] = True
        sc_array[1] = True
        note_array[0] = str(note_roll - 1)
        note_array[1] = str(note_roll + 1)
    if skill > 20:
        sc_array[0] = True
        sc_array[1] = True
        sc_array[2] = True
        note_array[0] = str(note_roll - 1)
        note_array[1] = str(note_roll + 1)
        note_array[2] = str(note_roll + 2)
    if sc_array[0] and luck_roll > 1:
        t1 = luck_roll - 1
        if t1 == 1:
            swarm_check = True
        mon_tuple = find_mon(area, str(t1), pl)
        ret_string += mon_tuple[0] + ", "
        if mon_tuple[1] != "":
            author_note[0] += "{0[0]} Note: \n{0[1]}".format(mon_tuple)
    mon_tuple = find_mon(area, str(luck_roll), pl)
    ret_string += mon_tuple[0]
    if mon_tuple[1] != "":
        author_note[0] += "\n{0[0]} Note: \n{0[1]}".format(mon_tuple)
    if note_flag:
        note_array[3] = str(note_roll)
        note_string = ", ".join(note_array)
        ret_string += " Option {0}".format(note_string)
    if sc_array[1] and luck_roll < 20:
        t2 = str(luck_roll + 1)
        mon_tuple = find_mon(area, str(t2), pl)
        ret_string += ", " + mon_tuple[0]
        if mon_tuple[1] != "":
            author_note[0] += "\n{0[0]} Note: \n{0[1]}".format(mon_tuple)
    if sc_array[2] and luck_roll < 19:
        t3 = str(luck_roll + 2)
        mon_tuple = find_mon(area, str(t3), pl)
        ret_string += ", " + mon_tuple[0]
        if mon_tuple[1] != "":
            author_note[0] += "\n{0[0]} Note: \n{0[1]}".format(mon_tuple)
    if swarm_flag and swarm_check:
        ret_string += "\n\n You are a high enough level to qualify for a swarm encounter. If chosen, have your GM " \
                      "roll 2 " \
                      "more pokemon for the encounter."
        swarm = [find_mon(area, str(random.randint(2, 20)), pl)[0], find_mon(area, str(random.randint(2, 20)), pl)[0]]
        author_note[0] += "\nAdditional Swarm Pokemon are: {0[0]}, {0[1]}\n".format(swarm)
    author_note[0] += "\n\nArea Event: " + choose_event(area, pl, swarm_check)
    author_note[0] += find_disposition(area)
    return ret_string


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
            if dice_roll - EVENT_MOD == 10:
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


def roll_exclude():
    randInt = random.randint(1, 50)
    return roll_exclude() if randInt in TREASURE_SLOTS else randInt


def roll_adventure(area, tl, pl, th=None, target=None, force_mon=None, force_event=None, extra_players=0):
    encounter_roll = None
    treasure_guardian = None
    encounter = None
    event = None
    disposition = None
    treasure_flag = False
    ex_treasure_flag = False
    ret_string = ''
    alpha_flag = False
    num_treasure_hunts = 0
    guardianFlag = True if int(tl) >= 20 else False
    majorTreasureFlag = True if int(pl) >= 45 else False
    if force_mon is None:
        if majorTreasureFlag:
            encounter_roll = random.randint(1, 50)
        else:
            encounter_roll = random.randint(2, 50)
        if encounter_roll in TREASURE_SLOTS:
            treasure_flag = True
            if encounter_roll == 50:
                alpha_flag = True
            else:
                treasure_guardian = find_mon(area, str(roll_exclude()), pl)
        if th is not None and target is not None and str(encounter_roll) != target:
            starting_val = 1 if majorTreasureFlag else 2
            treasure_array = numpy.random.randint(starting_val, 50, size=int(th) * 3)
            if int(target) in treasure_array:
                if int(target) == 50:
                    alpha_flag = True
                else:
                    alpha_flag = False
                encounter_roll = int(target)
                num_treasure_hunts = int(math.ceil(treasure_array.tolist().index(int(target)) / 3))
            else:
                num_treasure_hunts = int(th)
    else:
        encounter_roll = int(force_mon)
        if encounter_roll in TREASURE_SLOTS:
            treasure_flag = True
            if encounter_roll == 50:
                alpha_flag = True
            else:
                treasure_guardian = find_mon(area, str(roll_exclude()), pl)

    encounter = find_mon(area, str(encounter_roll), pl)
    ret_string += "Encounter 1: " + encounter[0]
    if encounter[1] != "":
        ret_string += encounter[1]
    if treasure_flag:
        if alpha_flag:
            alpha_mon = find_mon(area, str(roll_exclude()), pl)
            ret_string += "\nAlpha Mon Selected is: " + alpha_mon[0] + alpha_mon[1]
            alpha_flag = False
        else:
            ret_string += "\nThe treasure guardian is: " + treasure_guardian[0] + treasure_guardian[1]
    if extra_players > 0:
        ret_string += "\n\nNow rolling encounters for additional players...\n"
        encounter_num = int(extra_players)
        additional_mons = None
        if treasure_flag:
            additional_mons = [roll_exclude() for i in range(encounter_num)]
            treasure_flag = False
        else:
            additional_mons = [roll_exclude() for i in range(encounter_num - 1)]
            if majorTreasureFlag:
                additional_mons.append(random.randint(1, 50))
            else:
                additional_mons.append(random.randint(2, 50))
            if additional_mons[-1] == 50:
                alpha_flag = True
            else:
                treasure_guardian = find_mon(area, str(roll_exclude()), pl)
        i = 2
        print(additional_mons)
        for x in additional_mons:
            if x in TREASURE_SLOTS:
                ex_treasure_flag = True
            additional_encounter = find_mon(area, str(x), pl)
            ret_string += "Encounter {0}: ".format(i) + additional_encounter[0] + additional_encounter[1] + "\n"
            i += 1
            if ex_treasure_flag:
                if alpha_flag:
                    alpha_mon = find_mon(area, str(roll_exclude()), pl)
                    ret_string += "\nAlpha Mon Selected is: " + alpha_mon[0] + alpha_mon[1] + "\n"
                else:
                    ret_string += "\nThe treasure guardian is: " + treasure_guardian[0] + treasure_guardian[1] + "\n"
    if force_event is not None:
        ret_string += "\n\nArea Event: " + choose_event(area, pl, tl, force_event)
    else:
        ret_string += "\n\nArea Event: " + choose_event(area, pl, tl)
    if th is not None:
        ret_string += "\n\nYou Treasure Hunted {0} times and got these results".format(num_treasure_hunts)
    ret_string += find_disposition(area)
    return ret_string
