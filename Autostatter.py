import math
import random

import gspread
import pygsheets

from Constants import *
from gspread_credentials import credentials
from utilities import *

gc = gspread.service_account_from_dict(credentials)
pg = pygsheets.authorize(service_file='service_account_credentials.json')
update_details = {
    "level": {
        "range": "H3",
        "values": [[]]
    },
    "species": {
        "range": "D3",
        "values": [[]]
    },
    "moves": {
        "range": "B44:C68",
        "values": [[]]
    },
    "abilities": {
        "range": "B71:B73",
        "values": [[]]
    },
    "levelup": {
        "range": "G11:G16",
        "values": [[]]
    },
    "nature": {
        "range": "D5",
        "values": [[]]
    },
    "gender": {
        "range": "B5",
        "values": [[]]
    },

}


# write command so that it sends in the mon's name with the first letter capitalized

def initialize(pokemon, level):
    criteria = re.compile('(?i)^' + pokemon + "$")
    if any((match := criteria.search(item)) for item in ALLPOKEMON.keys()):
        poke_data = ALLPOKEMON[match.group(0)]
        evo_levels = [int(i) for i in poke_data['evolutions'].keys()]
        max_evo = find_largest_smaller_number(evo_levels, level)
        if max_evo is not None:
            evo = poke_data['evolutions'][str(max_evo)]
            if isinstance(evo, list):
                chosen_evo = random.choice(evo)
                evo = chosen_evo.replace("(Male)" if "(Male)" in chosen_evo else "(Female)", "")
            poke_data = ALLPOKEMON[evo]
        update_details["level"]["values"][0].append(level)
        return poke_data
    else:
        return None


def clear_cells(statter):
    statter.batch_clear(['B44:B68', 'B71:B75', 'L71:L75', 'B97:B104', 'D11:D16', 'J11:J16', 'H87:K94'])


def convert_row_to_column(row_list):
    column_list = [[row[i]] for row in row_list for i in range(len(row))]
    return column_list


def get_gender(mon):
    if mon['male'] == -1:
        return 'Genderless'
    else:
        return 'Male' if random.random() < mon['male'] else 'Female'


def assign_moves(pokemon, level):
    for move in pokemon["moves"]:
        if 'Tutor' not in move:
            move_details = move.split(" ", maxsplit=1)
            if int(move_details[0]) <= level:
                update_details["moves"]["values"][0].append(move_details[1])


def assign_abilities(pokemon, level):
    update_details["abilities"]["values"][0].append(random.choice(pokemon['abilities']))
    if level >= 20:
        update_details["abilities"]["values"][0].append(random.choice(pokemon['advabilities']))
    if level >= 40:
        update_details["abilities"]["values"][0].append(random.choice(pokemon['highabilities']))


def getValid(bonusStats, baseStats):
    valid = []
    for stat in bonusStats.keys():
        good = True
        for ostat in bonusStats.keys():
            if baseStats['b' + stat] < baseStats['b' + ostat] and (
                    int(bonusStats[stat]) + int(baseStats['b' + stat]) + 1) >= (
                    int(bonusStats[ostat]) + int(baseStats['b' + ostat])):
                good = False
        if good:
            valid.append(stat)
    return valid


def setStats(bonusStats, baseStats):
    valid = getValid(bonusStats, baseStats)
    raisable = []
    for vstat in valid:
        weight = math.ceil(math.sqrt(baseStats['b' + vstat]) * 10)
        while weight > 0:
            raisable.append(vstat)
            weight -= 1
    raiseStat = random.choice(raisable)
    bonusStats[raiseStat] += 1
    return bonusStats


def distribute_stats(pokemon, level):
    level_up_stats = 10 + level
    bonusStats = {
        "hp": 0,
        "atk": 0,
        "def": 0,
        "satk": 0,
        "sdef": 0,
        "spd": 0
    }

    baseStats = {
        "bhp": int(pokemon['HP']),
        "batk": int(pokemon['Attack']),
        "bdef": int(pokemon['Defense']),
        "bsatk": int(pokemon['Special Attack']),
        "bsdef": int(pokemon['Special Defense']),
        "bspd": int(pokemon['Speed'])
    }
    for i in range(level_up_stats):
        bonusStats = setStats(bonusStats, baseStats)

    update_details["levelup"]["values"][0] = list(bonusStats.values())


def generate_pokemon(pokename, level, sheet):
    data_block = initialize(pokename, level)
    if data_block is None:
        similar_word = find_most_similar_string(ALLPOKEMON.keys(), pokename.upper())
        return "There is no pokemon by that name. Did you mean " + similar_word.title() + "?"
    update_details["species"]["values"][0].append(data_block['name'])
    update_details["gender"]["values"][0].append(get_gender(data_block))
    update_details["nature"]["values"][0].append(random.choice(NATURES))
    assign_moves(data_block, level)
    assign_abilities(data_block, level)
    distribute_stats(data_block, level)
    update_details["moves"]["values"] = convert_row_to_column(update_details["moves"]["values"])
    update_details["abilities"]["values"] = convert_row_to_column(update_details["abilities"]["values"])
    update_details["levelup"]["values"] = convert_row_to_column(update_details["levelup"]["values"])
    sheet.batch_update(list(update_details.values()))
    return "Autostatting Successful"


def autostatter(pokename, level, link):
    statter = gc.open_by_url(link.replace("?usp=sharing", ""))
    template_sheet = statter.worksheet("Duplicate Me!")
    stated_sheet = template_sheet.duplicate()
    clear_cells(stated_sheet)
    lvl = int(level)
    ret_string = generate_pokemon(pokename, lvl, stated_sheet)
    return ret_string


print(autostatter("Mankey", "30",
                  "https://docs.google.com/spreadsheets/d/1Q6CoAFiWgyVZ68LFCj2W_A5VDJvDPdKxG7RsLELr4IQ/edit?usp=sharing"))
