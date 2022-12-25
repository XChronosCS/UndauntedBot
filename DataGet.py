import random
import re

import fitz
import gspread
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from constants import *
from gspread_credentials import *
from utilities import *

creds = ServiceAccountCredentials.from_json_keyfile_name('UndauntedBot/service_account_credentials.json',
                                                         scopes="https://www.googleapis.com/auth/documents.readonly")
service = build('docs', 'v1', credentials=creds)

gc = gspread.service_account_from_dict(credentials)

sh = gc.open("Data Get Test Sheet")

abilities = sh.worksheet("Abilities Data")
features = sh.worksheet("Features Data")
items = sh.worksheet("Inventory Data")
edges = sh.worksheet("Edges Data")
moves = sh.worksheet("Moves Data")
pokedex = fitz.Document("Documents/Phemenon Pokedex.pdf")
lore_doc = fitz.Document("Documents/Phemenon Lore Book.pdf")
compendium = fitz.Document("Documents/Mythology Compendium.pdf")
extras = sh.worksheet("Class Data")
misc = sh.worksheet("Misc Data")
des = gc.open("Data Encounter Sheet")
encounters = des.worksheet("Encounter Tables")
arcana = service.documents().get(documentId="1gc6eTktgcQo9zViLghnWfxWmNrFzKKH6Y4QWMlwMzlo").execute()
red = gc.open("them beans")
pos = red.worksheet("Positive")
neg = red.worksheet("Negative")
intro = red.worksheet("Intro")
habitat = gc.open("Data Habitat Areas").worksheet("Data")

max_page = 1100


def get_arcana_edges(legend):
    ret_array = []
    prereq_list = ""
    doc_content = arcana.get('body').get('content')
    par_list = read_strucutural_elements(doc_content)
    with open("Documents/LegendData.txt", "r+") as f:
        for line in f:
            if legend.title() in line:
                prereq_list += f.readline().rstrip() + ", "
                prereq_list += f.readline().rstrip()
                break
    if prereq_list == "":
        return ["There is no legend by that name. Please try again."]
    prereqs = prereq_list.split(", ")
    for i in range(len(par_list)):
        if "\\n" in par_list[i]:
            par_list[i].replace("\\n", "\n")
        if i + 1 != len(par_list):
            if any(aspect in par_list[i] for aspect in prereqs) and "Prerequisites:" in par_list[i]:
                ret_string = "**" + par_list[i - 1] + "**" + par_list[i] + par_list[i + 1] + par_list[i + 2]
                if "Trigger:" in par_list[i + 2] or "Target:" in par_list[i + 2] or "Bonus:" in par_list[i + 3]:
                    ret_string += par_list[i + 3]
                if "Bonus:" in par_list[i + 4]:
                    ret_string += par_list[i + 4]
                ret_string += "\n"
                ret_array.append(ret_string)
    return ret_array


def get_ability_data(name):
    """
    Recurses through ability column on Data sheet to find matching ability name, then returns matching description.
    :param name: String name of the ability in question
    :return: Description of the ability.
    """
    criteria = re.compile('(?i)^' + name + "$")
    match = abilities.find(criteria, in_column=1)
    if match is None:
        return ["There is no ability by that name"]
    else:
        row = match.row
        ability_name = abilities.cell(row, 1).value
        ability_freq = "\n" + abilities.cell(row, 2).value
        ability_eff = "\n" + abilities.cell(row, 3).value
        return [ability_name, ability_freq, ability_eff]


def get_feature_data(name):
    criteria = re.compile('(?i)^' + name.replace("(", "\(").replace(")", "\)") + "$")
    match = features.find(criteria, in_column=1)
    if match is None:
        return ["There is no feature by that name"]
    else:
        row = match.row
        feature_name = features.cell(row, 1).value
        feature_pre = "\n" + features.cell(row, 2).value
        feature_tag = "\n" + features.cell(row, 3).value
        feature_freq = "\n" + features.cell(row, 4).value
        feature_eff = "\n" + features.cell(row, 5).value
        return [feature_name, feature_pre, feature_tag, feature_freq, feature_eff]


def get_item_data(name):
    criteria = re.compile('(?i)^' + name + "$")
    match = items.find(criteria, in_column=28)
    if match is None:
        return ["There is no item by that name"]
    else:
        row = match.row
        item_name = items.cell(row, 28).value
        item_eff = "\n" + items.cell(row, 29).value
        return [item_name, item_eff]


def get_edge_data(name):
    criteria = re.compile('(?i)^' + name + "$")
    match = edges.find(criteria, in_column=1)
    if match is None:
        return ["There is no edge by that name"]
    else:
        row = match.row
        edge_name = edges.cell(row, 1).value
        edge_freq = "\n" + edges.cell(row, 2).value
        edge_eff = "\n" + edges.cell(row, 3).value
        return [edge_name, edge_freq, edge_eff]


def get_move_data(name):
    criteria = re.compile('(?i)^' + name + "$")
    match = moves.find(criteria, in_column=1)
    if match is None:
        return ["There is no move by that name"]
    else:
        row = match.row
        move_name = "Name: " + moves.cell(row, 1).value
        move_type = "\nType: " + moves.cell(row, 2).value
        move_class = "\n" + moves.cell(row, 3).value
        move_freq = "\n" + moves.cell(row, 4).value
        move_range = "\n" + moves.cell(row, 5).value
        move_ac = "\nAC: " + str(moves.cell(row, 6).value)
        move_db = "\nDB: " + str(moves.cell(row, 7).value)
        move_eff = "\nEffect: " + moves.cell(row, 8).value
        move_tag = "\nStyle Tag: " + moves.cell(row, 9).value
        return [move_name, move_type, move_class, move_freq, move_range, move_ac, move_db, move_eff, move_tag]


def get_habitat(name):
    criteria = re.compile('(?i)^' + name + "$")
    match = habitat.find(criteria, in_column=1)
    if match is None:
        return "This is either not the species's basic form or it cannot be found anywhere at the moment."
    else:
        row = match.row
        ret_array = []
        areas = habitat.range(row, 3, row, 32)
        for x in areas:
            if x.value is not None and x.value != '':
                ret_array.append(x.value)
        ret_string = "This pokemon is found in the following locations: " + ", ".join(ret_array)
        return ret_string


def show_mechanics():
    options = extras.col_values(1)
    del options[:2]
    return options


def get_mechanic(name):
    criteria = re.compile('(?i)^' + name + "$")
    match = extras.find(criteria, in_column=1)
    row = match.row
    ret_string = "Mechanic: " + extras.cell(row, 2).value + "\n\nEffect: " + extras.cell(row, 3).value
    return ret_string


def get_technique(name):
    criteria = re.compile('(?i)^' + name + "$")
    match = extras.find(criteria, in_column=4)
    if match is None:
        return "There is no technique by that name"
    else:
        row = match.row
        ret_string = extras.cell(row, 4).value
        ret_string += "\nPrerequisities: " + extras.cell(row, 5).value
        ret_string += "\nFrequency / Cost: " + extras.cell(row, 6).value
        ret_string += "\n\n" + extras.cell(row, 7).value
        return ret_string


def get_order(name):
    criteria = re.compile('(?i)^' + name + "$")
    match = features.find(criteria, in_column=6)
    if match is None:
        match = features.find(criteria, in_column=9)
        if match is None:
            return "There is no general order by that name"
        else:
            row = match.row
            col = match.col
            ret_string = features.cell(row, col).value
            ret_string += "\n" + features.cell(row, col + 1).value
            ret_string += "\n\n" + features.cell(row, col + 2).value
            return ret_string
    else:
        row = match.row
        col = match.col
        ret_string = features.cell(row, col).value
        ret_string += "\n" + features.cell(row, col + 1).value
        ret_string += "\n\n" + features.cell(row, col + 2).value
        return ret_string


def get_keyword_moves(name):
    criteria = re.compile('(?i)' + name)
    match = moves.findall(criteria, in_column=5)
    if len(match) != 0:
        ret_array = []
        for x in match:
            ret_array.append(moves.cell(x.row, 1).value)
        ret_string = "Here is a list of all moves with that keyword: " + ", ".join(ret_array)
        return ret_string
    else:
        return "That is not a valid attack Keyword. Please try again"


def get_flair_moves(name, typing):
    criteria = re.compile('(?i)' + name)
    match = moves.findall(criteria, in_column=9)
    if len(match) != 0:
        ret_array = []
        move_typings = moves.col_values(2)
        for x in match:
            if move_typings[x.row - 1] == typing.title():
                ret_array.append(moves.cell(x.row, 1).value)
        ret_string = "Here is a list of all moves of type " + typing.title() + " with the style tag " + name.title() + ": " + ", ".join(
            ret_array)
        return ret_string
    else:
        return "That is not a valid style tag. Please try again"


def poke_ability(name):
    temp_name = name.title() if name.lower() != "power of alchemy" else "Power of Alchemy"
    ret_array = [pokemon['name'].title() for pokemon in ALLPOKEMON if
                 temp_name in pokemon['abilities'] or temp_name in pokemon['advabilities'] or temp_name in pokemon[
                     'highabilities']]
    ret_string = "**Here is a list of all the pokemon with the ability " + temp_name + ":** " + ", ".join(ret_array)
    return ret_string


def poke_moves(name):
    first_name = name.title() if name.lower() != "roar of time" else "Roar of Time"
    temp_name = first_name.title() if first_name.lower() != "light of ruin" else "Light of Ruin"
    ret_array = [pokemon['name'].title() for pokemon in ALLPOKEMON if
                 any(temp_name in full_name for full_name in pokemon["moves"])]
    ret_string = "**Here is a list of all the pokemon with the level up move " + temp_name + ":** " + ", ".join(
        ret_array)
    return ret_string


def make_text(words):
    """Return textstring output of get_text("words").
    Word items are sorted for reading sequence left to right,
    top to bottom.
    """
    line_dict = {}  # key: vertical coordinate, value: list of words
    words.sort(key=lambda w: w[0])  # sort by horizontal coordinate
    for w in words:  # fill the line dictionary
        y1 = round(w[3], 1)  # bottom of a word: don't be too picky!
        word = w[4]  # the text of the word
        line = line_dict.get(y1, [])  # read current line content
        line.append(word)  # append new word
        line_dict[y1] = line  # write back to dict
    lines = list(line_dict.items())
    lines.sort()  # sort vertically
    return " ".join([" ".join(line[1]) for line in lines])


def poke_tutor(name):
    temp_name = name.title() if name.lower() != "light of ruin" else "Light of Ruin"
    mon_names = []
    for entry in pokedex.pages(11, max_page):
        tutor_rect = fitz.Rect(360, 386, 576, 690)
        name_rect = fitz.Rect(28, 0, 457, 60)
        word_page = entry.get_text("words")
        tutor_temp = [w for w in word_page if fitz.Rect(w[:4]) in tutor_rect]
        tutor_moves = make_text(tutor_temp)
        if temp_name in tutor_moves:
            temp = [w for w in word_page if fitz.Rect(w[:4]) in name_rect]
            poke_name = make_text(temp)
            mon_names.append(poke_name)
    ret_string = "**List of pokemon with the tutor move " + temp_name + ":** " + ", ".join(
        mon_names)
    return ret_string


def poke_capability(name):
    temp_name = name.title()
    mon_names = []
    for entry in pokedex.pages(12, max_page):
        cap_rect = fitz.Rect(10, 450, 311, 532)
        name_rect = fitz.Rect(28, 0, 457, 60)
        word_page = entry.get_text("words")
        cap_temp = [w for w in word_page if fitz.Rect(w[:4]) in cap_rect]
        caps = make_text(cap_temp)
        if temp_name in caps:
            temp = [w for w in word_page if fitz.Rect(w[:4]) in name_rect]
            poke_name = make_text(temp)
            mon_names.append(poke_name)
    ret_string = "**List of all pokemon with capability " + temp_name + ":** " + ", ".join(
        mon_names)
    return ret_string


def get_data(name):
    final_string = ''
    num_hits = 0
    ret_string = ''.join(get_feature_data(name))
    if ret_string != "There is no feature by that name":
        num_hits += 1
        final_string += "Class: Feature\n" + ret_string + "\n\n"
    ret_string = ''.join(get_ability_data(name))
    if ret_string != "There is no ability by that name":
        num_hits += 1
        final_string += "Class: Ability\n" + ret_string + "\n\n"
    ret_string = ''.join(get_edge_data(name))
    if ret_string != "There is no edge by that name":
        num_hits += 1
        final_string += "Class: Edge\n" + ret_string + "\n\n"
    ret_string = ''.join(get_item_data(name))
    if ret_string != "There is no item by that name":
        num_hits += 1
        final_string += "Class: Item\n" + ret_string + "\n\n"
    ret_string = ''.join(get_move_data(name))
    if ret_string != "There is no move by that name":
        num_hits += 1
        final_string += "Class: Move\n" + ret_string + "\n\n"
    ret_string = get_technique(name)
    if ret_string != "There is no technique by that name":
        num_hits += 1
        final_string += "Class: Technique\n" + ret_string + "\n\n"
    ret_string = ''.join(get_cap_data(name))
    if ret_string != "There is no capability by that name":
        num_hits += 1
        final_string += "Class: Capability\n" + ret_string + "\n\n"
    ret_string = get_status_data(name)
    if ret_string != "There is no status condition by that name":
        num_hits += 1
        final_string += "Class: Status Condition\n" + ret_string + "\n\n"
    ret_string = get_order(name)
    if ret_string != "There is no general order by that name":
        num_hits += 1
        final_string += "Class: Order\n" + ret_string + "\n\n"
    if num_hits == 0:
        return "There is no Move, Feature, Ability, Edge, Item, Class Technique, Capability, " \
               "Status Condition, or Order by that name"
    else:
        return "Number of possible matches: " + str(num_hits) + "\n\n" + final_string


def get_man_data(name):
    criteria = re.compile('(?i)^' + name + "$")
    match = moves.find(criteria, in_column=10)
    if match is None:
        return ["There is no manuever by that name"]
    else:
        row = match.row
        move_name = "Name: " + moves.cell(row, 10).value
        move_type = "\nClass: " + moves.cell(row, 11).value
        move_freq = "\nAction: " + moves.cell(row, 12).value
        move_range = "\nRange " + moves.cell(row, 13).value
        move_ac = "\nAC: " + str(moves.cell(row, 14).value)
        move_db = "\nEffect: " + str(moves.cell(row, 15).value)
        return [move_name, move_type, move_freq, move_range, move_ac, move_db]


def get_cap_data(name):
    criteria = re.compile('(?i)^' + name + "$")
    match = misc.find(criteria, in_column=7)
    if match is None:
        return ["There is no capability by that name"]
    else:
        row = match.row
        cap_name = misc.cell(row, 7).value
        cap_eff = "\n" + misc.cell(row, 8).value
        return [cap_name, cap_eff]


def get_keyword_data(name):
    criteria = re.compile('(?i)^' + name + "$")
    match = misc.find(criteria, in_column=17)
    if match is None:
        return "There is no keyword by that name"
    else:
        row = match.row
        ret_string = misc.cell(row, 17).value
        ret_string += "\n" + misc.cell(row, 18).value
        return ret_string


def get_status_data(name):
    criteria = re.compile('(?i)^' + name + "$")
    match = misc.find(criteria, in_column=9)
    if match is None:
        return "There is no status condition by that name"
    else:
        row = match.row
        ret_val = misc.cell(row, 9).value
        ret_val += "\nRegular Effect: " + misc.cell(row, 10).value
        ret_val += "\nBoss Effect: " + misc.cell(row, 11).value
        return ret_val


def get_treasure_spot(name):
    criteria = re.compile('(?i)^' + name + "$")
    match = encounters.findall(criteria)
    if len(match) == 0:
        return "No Treasure of that name can be found. Please make sure you are spelling it correctly."
    else:
        areas = []
        for item in match:
            col = item.col
            areas.append(encounters.cell(2, col).value)
        ret_val = "**That treasure can be found in the following adventures areas:** " + ", ".join(areas)
        return ret_val


def get_dex_entry(name):
    for entry in pokedex.pages(11, max_page):
        name_rect = fitz.Rect(28, 0, 457, 60)
        word_page = entry.get_text("words")
        temp = [w for w in word_page if fitz.Rect(w[:4]) in name_rect]
        poke_name = make_text(temp)
        if poke_name.lower() == name.lower():
            pix = entry.get_pixmap()  # render page to an image
            pix.save("{0}.png".format(name.lower()))
            break


def get_lore_entry(name):
    matching = False
    matching_pages = []
    for entry in lore_doc.pages(3, 214):
        name_rect = fitz.Rect(0, 144, 600, 220)
        word_page = entry.get_text("words")
        temp = [w for w in word_page if fitz.Rect(w[:4]) in name_rect]
        lore_name = make_text(temp)
        if lore_name.lower() == name.lower():
            matching = True
        if matching is True:
            if lore_name.lower() != name.lower():
                break
            pix = entry.get_pixmap()  # render page to an image
            file_name = "{0}_{1}.png".format(name.lower(), len(matching_pages))
            pix.save(file_name)
            matching_pages.append(file_name)
    return matching_pages


def get_legend_entry(name):
    matching = False
    matching_pages = []
    for entry in compendium.pages(3, 125):
        name_rect = fitz.Rect(0, 144, 600, 220)
        word_page = entry.get_text("words")
        temp = [w for w in word_page if fitz.Rect(w[:4]) in name_rect]
        lore_name = make_text(temp)
        if name.lower() in lore_name.lower():
            matching = True
        if matching is True:
            if name.lower() not in lore_name.lower():
                break
            pix = entry.get_pixmap()  # render page to an image
            file_name = "{0}_{1}.png".format(name.lower(), len(matching_pages))
            pix.save(file_name)
            matching_pages.append(file_name)
    return matching_pages


def get_beans():
    bean_list = neg if random.randint(1, 4) == 4 else pos
    intro_choice = intro.col_values(1)
    bean_options = bean_list.col_values(1)
    bean_taste = random.choice(bean_options)
    intro_text = random.choice(intro_choice)
    return intro_text + " " + bean_taste
