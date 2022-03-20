import gspread
import random
import re
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

EXPLO_SKILLS = {
    "Acrobatics": {'15': 'Each Trainer and Pokémon gains +1 CS in Speed.',
                   '25': 'Each Pokémon in the Encounter will have “Advanced Mobility” Edge for free.'},
    "Athletics": {'15': 'Each Trainer and Pokémon gains one Tick of Temporary HP.',
                  '25': 'Each Trainer and Pokémon gains double their tick value in Temporary HP.'},
    "Charm": {'15': 'All attempts to Social Capture gain +2 as a Modifier.',
              '25': 'One Random Pokémon will be Infatuated with the Party Leader.'},
    "Combat": {
        '15': 'Each Encountered Pokémon gains +1 CS in either Attack and Defense, or Special Attack and Special '
              'Defense. However all participating Trainers gain +1 Additional TXP Reward if the Party battled against '
              'the Encountered Pokémon.',
        '30': 'Each Encountered Pokémon gains +2 CS in either Attack and Defense, or Special Attack and Special '
              'Defense. However all participating Trainers gain +2 Additional TXP Reward if the Party battled against '
              'the Encountered Pokémon.'},
    "Command": {'15': 'Each Party Pokémon can cure a Volatile Condition as a Shift Action once.',
                '25': 'Each Party Pokémon can cure a Volatile Condition and a Persistent Condition as a single Shift '
                      'Action once.'},
    "General Edu": {'15': 'The Leader can reroll their 1d20 Luck Roll.',
                    '25': 'The Leader can reroll their Luck Roll or add/subtract up to 2 from their Current Roll.'},
    "Medical Edu": {'20': 'All Pokémon captured within the Encounter will have their Injuries cured. Injuries cured '
                          'this way do not count towards the Maximum Limit of 5 Injuries per Week healed.'},
    "Pokemon Edu": {'20': 'There will be an extra Pokémon in this encounter. GM will roll another d20 for it.'},
    "Occult Edu": {'20': 'Roll a 1d10 and refer to the Occult Table on that Exploration Area. That Pokémon will also '
                         'show up and be equal to the Average Lead Level.'},
    "Tech Edu": {'15': 'have the Leader roll 4d4. Multiply it by 100 and they find that much Mechanical or Chemical '
                       'Scrap.'},
    "Focus": {'15': 'All Trainers and Pokémon gain the effects of Focused Training for the Encounter (It can stack '
                    'with itself.)',
              '25': 'Each Trainer or Pokémon in the Party may use Focus Energy as a Free Action.'},
    "Guile": {'15': "All Encountered Pokémon will have a Debuff based on their Disposition. If they’re Gullible they "
                    "will have 1 Less Evasion. If they’re Suspicious they will have 1 Less Accuracy."},
    "Intimidate": {'20': 'all Pokémon encountered will have -1 Attack and Special Attack CS, then roll a Focus check '
                         'for each Encountered Pokémon, if it doesn’t meet the Skill roll, they will start Fearful or '
                         'Very Hostile (Roll 1d2).'},
    "Intuition": {'15': 'All Encountered Pokémon can Increase or Decrease by 2 Levels.',
                  '25': 'All Encountered Pokémon can Increase or Decrease by 5 Levels. This overwrites the 2 Levels of '
                        '15+.'},
    "Perception": {'15': 'have the Leader roll 3d4. Multiply it by 100 and they find that muchScrap of their choice ('
                         'Mechanical, Chemical, Equipment, or Food).'},
    "Stealth": {'20': 'The Party will become stealthed to the Pokémon and they will be unaware. They can initiate '
                      'Combat with a surprise attack from one Pokémon. If below 20, each Pokémon rolls Opposed '
                      'Perception instead.'},
    "Survival": {'15': 'The Party will be able to choose one more option above their d20 on the Encounter Table.',
                 '25': 'The Party will instead be able to choose two more options above their d20 on the Encounter '
                       'Table.'}
}

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
occult = sh.worksheet("Occult Tables")
occult_notes = ws.worksheet_by_title("Occult Tables")
disp_sheet = sh.worksheet("Disposition")
area_names = encounters.row_values(2)
e_area_names = events.row_values(2)
o_area_names = occult.row_values(2)
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

def get_hidden_slot_adventure(area, slot):
    criteria = re.compile('(?i)^' + area + "$")
    area_match = secret_adventures.find(criteria, in_row=1)
    slot_match = secret_adventures.find(slot, in_column=1)
    if area_match is None:
        return "There is no adventure area with this name that has hidden slots."
    if slot_match is None:
        return "Please enter a valid encounter slot number."
    match = secret_adventures.cell(slot_match.row, area_match.col)
    if match.value is None:
        return "This area does not have that many slots. Please try again."
    note_check = sa_notes.cell((match.row, match.col))
    ret_string = ""
    ret_string += "Encounter in slot {0}".format(slot) + " of area {0} is: ".format(area) + match.value + "\n"
    if note_check.note is not None:
        ret_string += "Note: " + note_check.note + "\n"
        if "treasure" in note_check.note.lower():
            ret_string += get_treasure_guardian_hidden(area_match.col)
    return ret_string
  
  
def get_hidden_event_adventure(area, slot):
    criteria = re.compile('(?i)^' + area + "$")
    area_match = secret_events.find(criteria, in_row=1)
    slot_match = secret_events.find(slot, in_column=1)
    if area_match is None:
        return "There is no adventure area with this name that has hidden slots."
    if slot_match is None:
        return "Please enter a valid event slot number."
    match = secret_events.cell(slot_match.row, area_match.col)
    note_check = se_notes.cell((match.row, match.col))
    ret_string = ""
    ret_string += "Event in slot {0}".format(slot) + " of area {0} is: ".format(area) + match.value + "\n"
    if note_check.note is not None:
        ret_string += "Note: " + note_check.note + "\n"
    return ret_string

def get_treasure_guardian_hidden(area_col):
    slot_num = str(random.randint(1, 100))
    slot_match = secret_adventures.find(slot_num, in_column=1)
    match = secret_adventures.cell(slot_match.row, area_col)
    while (sa_notes.cell((match.row, match.col)).note != None and "treasure" in sa_notes.cell((match.row, match.col)).note.lower()) or match.value is None:
        slot_num = random.randint(1, 100)
        slot_match = secret_adventures.find(slot_num, in_column=1)
        match = secret_adventures.cell(slot_match.row, area_col)
    return "\nPokemon accompanying Treasure is {0}".format(match.value)
    
    
def get_skill(name):
    buff_list = EXPLO_SKILLS.get(name.title())
    if buff_list is None:
        return "That skill does not exist. Make sure to end all education skills with Edu and not Ed"
    else:
        ret_string = name.title()
        temp_list = buff_list.items()
        for item in temp_list:
            ret_string += "\nRoll a " + item[0] + "+: " + item[1]
        return ret_string
            

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


def roll_occult(area, pl=None):
    ret_string = None
    selection = None
    note = None
    level_mod = None
    roll = random.randint(1,10)
    modifier = EXPLO_MOD
    if area in o_area_names:
        area_cell = occult.find(area)
        select_cell = occult.cell(roll + modifier, area_cell.col)
        note_check = occult_notes.cell((select_cell.row, select_cell.col))
        if note_check.note is not None:
            note = "\nNote:\n" + note_check.note
        else:
            note = ''
        selection = select_cell.value
        level_mod = encounters.cell(select_cell.row, LEVEL_COLUMN).value
        if pl is not None:
            level_mod = eval(pl + level_mod)
    else:
        return "This encounter area does not exist. Please try again."
    ret_array = [selection, level_mod, note]
    ret_string = "\n\nYour Occult Table Pokemon is a {0[0]} Level {0[1]}".format(ret_array)
    return ret_string + "\n" +  ret_array[2]


def find_disposition(area):
    dispo = ''
    ret_string = ''
    # Altar of Dreams 3 roll is roll again
    if area in area_names:
        area_cell = disp_sheet.find(area)
        roll = random.randint(1, 5)
        dispo += disp_sheet.cell(roll + 1, area_cell.col).value
    else:
        return "This area does not exist. Please try again"
    return "\n\nThe starting disposition of this encounter is " + dispo


def roll_exploration(area, sk, luck_roll, tl, pl, rep_array, bait_mons, extra_players, skill_used, skill_key, force_mon, force_event, author_note):
    note_roll = random.randint(0, 4)
    extra_mons = 0 + bait_mons + extra_players
    swarm_flag = True if int(tl) > 15 else False
    swarm_check = True if luck_roll == 1 else False
    rare_flag = True if luck_roll == 20 else False
    sc_array = [False, False, False]  # in order: 1 Below, 1 Above, 2 Above
    guardian_flag = True if area.lower() in ["blanda woods", "frostwood forest", "illandy forest"] else False
    rare_array = ["", "", "", ""]
    rare_note_array = find_mon(area, str(20), pl)[1].split("\n")
    view_twenty = " ".join(rare_note_array).split()
    ret_string = 'Encounter Stating Results:\nYou Rolled a {0} for your luck roll.\n\nYour Options are '.format(
        str(luck_roll))
    skill = int(sk)
    if 11 > skill > 6:
        sc_array[0] = True
        rare_array[0] = str(((note_roll - 1) if note_roll != 0 else 4) + 1)
    if 16 > skill > 10:
        sc_array[1] = True
        rare_array[1] = str(((note_roll + 1) % 5) + 1)
    if 21 > skill > 15:
        sc_array[0] = True
        sc_array[1] = True
        rare_array[0] = str((note_roll - 1) if note_roll > 0 else 4)
        rare_array[1] = str(((note_roll + 1) % 5) + 1)
    if skill > 20:
        sc_array[0] = True
        sc_array[1] = True
        sc_array[2] = True
        rare_array[0] = str(((note_roll - 1) if note_roll > 0 else 4)+1)
        rare_array[1] = str((((note_roll + 1) % 5) + 1))
        rare_array[2] = str((((note_roll + 2) % 5) + 1))
    if guardian_flag and rare_flag:
        sc_array = [False, False, False]
    mon_tuple = find_mon(area, str(luck_roll), pl)
    ret_string += mon_tuple[0]
    if mon_tuple[1] != "":
        author_note[0] += "\n{0[0]} Note: \n{0[1]}".format(mon_tuple)
    if rare_flag and not guardian_flag:
        rare_array[3] = str(note_roll + 1)
        enc_array = []
        print(rare_array)
        for i in rare_array:
            if i != '':
                temp = next(line for line in rare_note_array if i + "." in line)
                i = temp
                enc_array.append(i)
        note_string = ", ".join(enc_array)
        ret_string += " Option {0}".format(note_string)
    if sc_array[0] and luck_roll > 1:
        t1 = luck_roll - 1
        while t1 != 1 and t1 in rep_array:
            t1 -= 1
        if t1 == 1:
            swarm_check = True
        mon_tuple = find_mon(area, str(t1), pl)
        ret_string += ", " + mon_tuple[0]
        if mon_tuple[1] != "":
            author_note[0] += "{0[0]} Note: \n{0[1]}".format(mon_tuple)
    if sc_array[1] and luck_roll < 20:
        t2 = luck_roll + 1
        while t2 != 20 and t2 in rep_array:
            t2 += 1
        mon_tuple = find_mon(area, str(t2), pl)
        ret_string += ", " + mon_tuple[0]
        if t2 == 20:
            ret_string += " (" + view_twenty[-1] + ")"
        if mon_tuple[1] != "":
            author_note[0] += "\n{0[0]} Note: \n{0[1]}".format(mon_tuple)
    if sc_array[2] and luck_roll < 19:
        t3 = luck_roll + 2
        while t3 != 20 and t3 in rep_array:
            t3 += 1
        mon_tuple = find_mon(area, str(t3), pl)
        ret_string += ", " + mon_tuple[0]
        if t3 == 20:
            ret_string += " (" + view_twenty[-1] + ")"
        if mon_tuple[1] != "":
            author_note[0] += "\n{0[0]} Note: \n{0[1]}".format(mon_tuple)
    if skill_used == "Survival" and int(skill_key) >= 15 and luck_roll < 18:
        t3 = luck_roll + 3
        while t3 != 20 and t3 in rep_array:
            t3 += 1
        mon_tuple = find_mon(area, str(t3), pl)
        ret_string += ", " + mon_tuple[0]
        if t3 == 20:
            ret_string += " (" + view_twenty[-1] + ")"
        if mon_tuple[1] != "":
            author_note[0] += "\n{0[0]} Note: \n{0[1]}".format(mon_tuple)
    if skill_used == "Survival" and int(skill_key) >= 25 and luck_roll < 17:
        t3 = luck_roll + 4
        while t3 != 20 and t3 in rep_array:
            t3 += 1
        mon_tuple = find_mon(area, str(t3), pl)
        ret_string += ", " + mon_tuple[0]
        if t3 == 20:
            ret_string += " (" + view_twenty[-1] + ")"
        if mon_tuple[1] != "":
            author_note[0] += "\n{0[0]} Note: \n{0[1]}".format(mon_tuple)
    if swarm_flag and swarm_check:
        ret_string += "\n\n You are a high enough level to qualify for a swarm encounter. If chosen, have your GM " \
                      "roll 2 " \
                      "more pokemon for the encounter."
        swarm = [find_mon(area, str(random.randint(2, 20)), pl)[0], find_mon(area, str(random.randint(2, 20)), pl)[0]]
        author_note[0] += "\nAdditional Swarm Pokemon are: {0[0]}, {0[1]}\n".format(swarm)
    if force_mon is not None:
        temp = find_mon(area, force_mon, pl)
        ret_string = "You have a forced the following encounter: " + temp[0]
        author_note[0] = "{0[0]} Note: \n{0[1]}".format(temp)
    for i in range(extra_mons):
        author_note[0] += "\n**Additional Mon " + str(i+1) + ":** {0[0]} Note: \n{0[1]}".format(
            find_mon(area, random.randint(1, 20), pl))
    if int(skill_key) >= 15:
        skill_bonus = EXPLO_SKILLS[skill_used].get(str(15), "None")
        if skill_bonus != "None":
            ret_string += "\n\nSkill Bonus: " + skill_bonus
    if int(skill_key) >= 20:
        skill_bonus = EXPLO_SKILLS[skill_used].get(str(20), "None")
        if skill_bonus != "None":
            ret_string += "\n\nSkill Bonus: " + skill_bonus
    if int(skill_key) >= 25:
        skill_bonus = EXPLO_SKILLS[skill_used].get(str(25), "None")
        if skill_bonus != "None":
            ret_string += "\n\nSkill Bonus: " + skill_bonus
    if int(skill_key) >= 30:
        skill_bonus = EXPLO_SKILLS[skill_used].get(str(30), "None")
        if skill_bonus != "None":
            ret_string += "\n\nSkill Bonus: " + skill_bonus
    author_note[0] += "\n\nArea Event: " + choose_event(area, pl, tl, force_event)
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
        ret_string += "\nHere are the treasure hunt rolls: " + ", ".join([str(num) for num in treasure_array.tolist()])
    ret_string += find_disposition(area)
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