import random
import re

import gspread

from gspread_credentials import *

gc = gspread.service_account_from_dict(credentials)

sh = gc.open("Test Town Tracker Sheet")
worksheet = sh.worksheet("Town Data")
town_list = sh.worksheet("Town List")


def get_town_event():
    town_event_effects = worksheet.col_values(8)
    town_event_names = worksheet.col_values(7)
    index = random.randrange(1, len(town_event_names))
    name = "**" + town_event_names[index] + "**"
    effect = town_event_effects[index]
    effect = effect.replace("Martial Modifier", "**Martial Modifier**")
    effect = effect.replace("Cultural Modifier", "**Cultural Modifier**")
    effect = effect.replace("Spiritual Modifier", "**Spiritual Modifier**")
    effect = effect.replace("Communal Modifier", "**Communal Modifier**")
    effect = effect.replace("Industrial  Modifier", "**Industrial Modifier**")
    effect = effect.replace("Mercantile Modifier", "**Mercantile Modifier**")
    effect = effect.replace("Academic Modifier", "**Academic Modifier**")
    return name, effect


def get_uprising_event():
    up_event_effects = worksheet.col_values(10)
    up_event_names = worksheet.col_values(9)
    index = random.randrange(1, len(up_event_names))
    name = "**" + up_event_names[index] + "**"
    effect = up_event_effects[index]
    effect = effect.replace("Martial Modifier", "**Martial Modifier**")
    effect = effect.replace("Cultural Modifier", "**Cultural Modifier**")
    effect = effect.replace("Spiritual Modifier", "**Spiritual Modifier**")
    effect = effect.replace("Communal Modifier", "**Communal Modifier**")
    effect = effect.replace("Industrial  Modifier", "**Industrial Modifier**")
    effect = effect.replace("Mercantile Modifier", "**Mercantile Modifier**")
    effect = effect.replace("Academic Modifier", "**Academic Modifier**")
    return name, effect


def roll_town(region):
    criteria = re.compile('(?i)^' + region + "$")
    match = town_list.find(criteria, in_row=1)
    if match is None:
        return "There is no region under this name. Please try again."
    else:
        towns = town_list.col_values(match.col)
        index = random.randrange(1, len(towns))
        return "The town you have randomly selected is " + towns[index] + "!"
