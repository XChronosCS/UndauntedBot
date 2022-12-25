import math
import random

import gspread
import pygsheets

import RollingCommands
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
pg = pygsheets.authorize(service_file='UndauntedBot/service_account_credentials.json')
edges_sheet = gc.open("Data Get Test Sheet")
edges = edges_sheet.worksheet("Tutoring/Breeding").get_values('PokeEdges')
sh = gc.open("Bot Auto Statter")
template = sh.worksheet("Template")
statter = None

mon = None


# write command so that it sends in the mon's name with the first letter capitalized

def clear_cells():
    statter.batch_clear(['B44:B68', 'B71:B75', 'L71:L75', 'B97:B104', 'D11:D16', 'J11:J16', 'H87:K94'])


def get_gender():
    if mon['male'] == -1:
        return 'Genderless'
    else:
        return 'Male' if random.random() < mon['male'] else 'Female'


def move_evolve(level, known_moves, baby):
    global mon
    if level in mon['evolutions'] and not baby:
        if isinstance(mon['evolutions'][level], list):
            mon_name = pick_gender(mon['evolutions'][level])
            mon = next(pokemon for pokemon in ALLPOKEMON if pokemon['name'] == mon_name.upper())
        else:
            mon = next(pokemon for pokemon in ALLPOKEMON if pokemon['name'] == mon['evolutions'][level])
        statter.update('D3', mon['evolutions'][level].title())

    def condition(x, lvl):
        temp_array = x.split()
        return lvl in temp_array

    output = [" ".join(element.split()[1:]) for idx, element in enumerate(mon['moves']) if condition(element, level)]
    known_moves += output


def pick_gender(arr):
    gender = statter.acell('B5').value
    choice = next(op for op in arr if gender in op)  # op stands for option
    ret_val = choice.replace('(' + gender + ')', '')
    return ret_val


def pick_edges(lvl):
    level = int(lvl)
    temp_list = [item for sublist in edges for item in sublist]
    if level < 30:
        temp_list.remove('Attack Specialty')
    temp_list.remove('Realized Potential')
    if level >= 10:
        random.shuffle(temp_list)
        statter.update('B97', temp_list[-1])
        temp_list.pop()
    if level >= 30:
        random.shuffle(temp_list)
        statter.update('B98', temp_list[-1])
        temp_list.pop()
    if level >= 50:
        random.shuffle(temp_list)
        statter.update('B99', temp_list[-1])
        temp_list.pop()
    if level >= 60:
        random.shuffle(temp_list)
        statter.update('B100', temp_list[-1])
        temp_list.pop()
    if level >= 70:
        random.shuffle(temp_list)
        statter.update('B101', temp_list[-1])
        temp_list.pop()
    if level >= 80:
        random.shuffle(temp_list)
        statter.update('B102', temp_list[-1])
        temp_list.pop()


def set_abilities(level):
    ability = mon['abilities'][random.randint(0, len(mon['abilities']) - 1)]
    adv_ab = mon['advabilities'][random.randint(0, len(mon['advabilities']) - 1)]
    high_ab = mon['highabilities'][0]
    statter.update('B71', ability)
    if int(level) >= 20:
        statter.update('B72', adv_ab)
        if int(level) >= 40:
            statter.update('B73', high_ab)


def get_valid(bonus, base):
    valid = []
    for stat in bonus:
        good = True
        for ostat in bonus:
            if base['b' + stat] < base['b' + ostat] and \
                    bonus[stat] + base['b' + stat] + 1 >= bonus[ostat] + base['b' + ostat]:
                good = False
        if good:
            valid.append(stat)
    return valid


def set_stats(bonus, base):
    valid = get_valid(bonus, base)
    raisable = []
    for stat in valid:
        weight = math.sqrt(base['b' + stat] * 10)
        while weight > 0:
            raisable.append(stat)
            weight -= 1
    increase = raisable[random.randrange(0, len(raisable))]
    bonus[increase] += 1
    return bonus


def generate_mon(mon_name, level, index, b_check):
    statter.update('D3', mon_name)
    statter.update('H3', int(level))
    statter.update('G11:G16', 0)
    clear_cells()
    known_moves = []
    global mon
    mon = next(pokemon for pokemon in ALLPOKEMON if pokemon['name'] == mon_name.upper())
    statter.update('D5', RollingCommands.nature())
    statter.update('B5', get_gender())
    for i in range(int(level)):
        move_evolve(str(i), known_moves, b_check)
    # global known_moves
    # temp = known_moves
    # known_moves = [i for n, i in enumerate(temp) if i not in temp[:n]]
    set_abilities(level)
    pick_edges(level)
    offset = 44
    for i in known_moves:
        cell = 'B' + str(offset)
        statter.update(cell, i)
        offset += 1
    bonus_stats = {
        "hp": 0,
        "atk": 0,
        "def": 0,
        "satk": 0,
        "sdef": 0,
        "spd": 0
    }
    base_stats = {
        "bhp": int(statter.acell('F11').value),
        "batk": int(statter.acell('F12').value),
        "bdef": int(statter.acell('F13').value),
        "bsatk": int(statter.acell('F14').value),
        "bsdef": int(statter.acell('F15').value),
        "bspd": int(statter.acell('F16').value)
    }
    lvl_points = statter.acell('G17').value
    for i in range(int(lvl_points)):
        bonus_stats = set_stats(bonus_stats, base_stats)
    statter.update('G11', bonus_stats['hp'])
    statter.update('G12', bonus_stats['atk'])
    statter.update('G13', bonus_stats['def'])
    statter.update('G14', bonus_stats['satk'])
    statter.update('G15', bonus_stats['sdef'])
    statter.update('G16', bonus_stats['spd'])

    xp = XP_VALS[int(level) - 1]
    statter.update('I3', xp)
    statter.update('D3', mon['name'].title())
    statter.update_title(mon['name'].title() + " " + str(index))


def autostatter(mon_name, level, email=None, link=None, base_check=False):
    new_sheet = gc.copy('1M3O95FW3KRT1pOBUNfqQ2Yk1YcrogZgLDFkkwuGxL_M', 'Temp AutoStatter',
                        folder_id='11qO1Py6VJbBFdTSy3uCTJWoheLT4cDn2')
    global statter
    if link is None and email is not None:
        statter = gc.open_by_key(new_sheet.id).worksheet("Template")
        generate_mon(mon_name, level, len(gc.open_by_key(new_sheet.id).worksheets()), base_check)
        statted_sheet = gc.copy(new_sheet.id, 'Statted Mons (Keep this Link)',
                                folder_id='11qO1Py6VJbBFdTSy3uCTJWoheLT4cDn2')
        gc.del_spreadsheet(new_sheet.id)
        statted_sheet.share(email, perm_type='user', role='writer')
        return "https://docs.google.com/spreadsheets/d/%s" % statted_sheet.id
    elif link is not None and email is None:
        origin = gc.open_by_url(link)
        duplicate_sheet = origin.worksheet('Duplicate Me!')
        duplicate_sheet.duplicate(new_sheet_name='Template')
        statter = origin.worksheet("Template")
        generate_mon(mon_name, level, len(origin.worksheets()), base_check)
        return link
    else:
        return "Error!"
