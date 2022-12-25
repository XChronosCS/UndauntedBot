import random
import re

import gspread
import pygsheets

import RollingCommands
from constants import TYPES
from gspread_credentials import *

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
    criteria = re.compile('(?i)' + p_type)
    type_col = eggs_temp.find(criteria).col
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
