import gspread
import re
import fitz
from constants import *

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from oauth2client.service_account import ServiceAccountCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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

creds = ServiceAccountCredentials.from_json_keyfile_name('UndauntedBot/service_account_credentials.json', scopes="https://www.googleapis.com/auth/documents.readonly")
service = build('docs', 'v1', credentials=creds)

gc = gspread.service_account_from_dict(credentials)

sh = gc.open("Data Get Test Sheet")
abilities = sh.worksheet("Abilities Data")
features = sh.worksheet("Features Data")
items = sh.worksheet("Inventory Data")
edges = sh.worksheet("Edges Data")
moves = sh.worksheet("Moves Data")
pokedex = fitz.Document("Documents/Phemenon Pokedex.pdf")
extras = sh.worksheet("Class Data")
misc = sh.worksheet("Misc Data")
des = gc.open("Data Encounter Sheet")
encounters = des.worksheet("Encounter Tables")
arcana = service.documents().get(documentId="154zQ3HyIuffxfnFV6QLTkUAPE0ta590mQXXstJtQILA").execute()

def read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.

        Args:
            element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')

  
def read_strucutural_elements(elements):
    """Recurses through a list of Structural Elements to read a document's text where text may be
        in nested elements.

        Args:
            elements: a list of Structural Elements.
    """
    text = []
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            temp = ''
            for elem in elements:
                temp += read_paragraph_element(elem)
            if "Prerequisite:" in temp and not temp.startswith("P"):
                temp_t = temp.split("Prerequisite:")
                text.append(temp_t[0][:-1])
                temp = "\nPrerequisite:" + temp_t[1]
            text.append(temp)
    return text


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
        if i+1 != len(par_list):
            if "Prerequisite:" in par_list[i] and ("Effect:" in par_list[i+1] or "Trigger:" in par_list[i+1] or "Target:" in par_list[i+1]) and any(aspect in par_list[i] for aspect in prereqs):
                ret_string = "**" + par_list[i-2] + "**" + par_list[i-1] + par_list[i] + par_list[i+1]
                if "Trigger:" in par_list[i+1] or "Target:" in par_list[i+1] or "Bonus:" in par_list[i+2]:
                    ret_string += par_list[i+2]
                if "Bonus:" in par_list[i+3]:
                    ret_string += par_list[i+3]
                ret_string += "\n"
                ret_array.append(ret_string)
    return ret_array
        


def get_ability_data(name):
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
    criteria = re.compile('(?i)^' + name + "$")
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


habitat = gc.open("Data Habitat Areas").worksheet("Data")


def get_habitat(name):
    criteria = re.compile('(?i)^' + name + "$")
    match = habitat.find(criteria, in_column=1)
    if match is None:
        return "This is either not the species's basic form or it cannot be found anywhere at the moment."
    else:
        row = match.row
        ret_array = []
        areas = habitat.range(row, 3, row, 12)
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
    for entry in pokedex.pages(12, 963):
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
    for entry in pokedex.pages(12, 963):
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
      
      
      
