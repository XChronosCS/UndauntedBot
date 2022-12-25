import random
import re

import gspread

from gspread_credentials import *
from utilities import *

gc = gspread.service_account_from_dict(credentials)
sh = gc.open("Guardian and Patronage Doc")
patronage_tables = sh.worksheet("Patronage Tasks")
guardians = sh.worksheet("Guardian Table")
wander = sh.worksheet("Wander Events")


def get_legend_personality(legend):
    criteria = re.compile('(?i)^' + legend + "$")  # get all the cells with the name of the legend in them in column 1
    matches = patronage_tables.find(criteria, in_column=1)
    if matches is None:  # checks for a non-existent legend. Exits the code if so.
        return "A legend with this name could not be found. Please make sure that the legend's name is spelled correctly."
    selected_task = matches.row  # Selects random task row among the valid options
    personality = "__**" + legend.title() + "**__\n" + "**Personality:** " + patronage_tables.cell(selected_task,
                                                                                                   2).value
    return personality


def get_patronage_task(legend, category):
    criteria = re.compile('(?i)^' + legend + "$")  # get all the cells with the name of the legend in them in column 1
    matches = patronage_tables.findall(criteria, in_column=1)
    if len(matches) == 0:  # checks for a non-existent legend. Exits the code if so.
        return ["A legend with this name could not be found. Please make sure that the legend's name is spelled "
                "correctly."]
    # Continues with selection process.
    options = []  # Possible options for random selection
    for op in matches:
        if patronage_tables.cell(op.row, 3).value == category.title():
            options.append(op.row)  # Adds the row with the matching request category to the possible options
    selected_task = random.choice(options)  # Selects random task row among the valid options
    sub_tasks_l = patronage_tables.get_values("E{0}:V{0}".format(selected_task))
    sub_tasks = [item for sublist in sub_tasks_l for item in sublist]
    subtask = "**" + patronage_tables.cell(selected_task, 4).value + "**\n" + random.choice(
        sub_tasks)  # Selects the sub task
    personality = "__**" + legend.title() + "**__\n" + "**Personality:** " + patronage_tables.cell(selected_task,
                                                                                                   2).value
    subtask_array = segment_text(subtask, "Legend")
    personality_array = [personality]
    return personality_array + subtask_array


def get_guardian_info(area):
    criteria = re.compile('(?i)^' + area + "$")
    matches = guardians.findall(criteria, in_column=1)
    if len(matches) == 0:
        return "There is no location by this name with a guardian present."
    else:
        match = random.choice(matches)
        row = match.row
        ret_val = guardians.cell(row, 2).value
        ret_val += guardians.cell(row, 3).value
        return ret_val


def get_wander_event():
    wander_event_effects = wander.col_values(2)
    wander_event_names = wander.col_values(1)
    index = random.randrange(1, len(wander_event_names))
    name = "**" + wander_event_names[index] + "**"
    effect = "\n\n" + wander_event_effects[index]
    ret_string = name
    ret_string += effect
    return ret_string


"""
test_string = patronage_tables.cell(1, 1).value
test_array = test_string.split("\n")
for i in test_array:
    print(i)
"""
