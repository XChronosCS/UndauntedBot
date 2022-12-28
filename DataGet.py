import fitz
import gspread
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from CollectData import infodex
from Constants import *
from gspread_credentials import *
from utilities import *

creds = ServiceAccountCredentials.from_json_keyfile_name('service_account_credentials.json',
                                                         scopes="https://www.googleapis.com/auth/documents.readonly")
service = build('docs', 'v1', credentials=creds)

gc = gspread.service_account_from_dict(credentials)

sh = gc.open("Data Get Test Sheet")

# Loading Worksheets for Primary Information Lookup
abilities = infodex["abilities"]
features = infodex["features"]
items = infodex["items"]
edges = infodex["edges"]
moves = infodex["moves"]
mechanics = infodex["mechanics"]
techniques = infodex["techniques"]
orders = infodex["orders"]
capabilities = infodex["capabilities"]
keywords = infodex["keywords"]
statuses = infodex["statuses"]
maneuvers = infodex["maneuvers"]
habitat = gc.open("Data Habitat Areas").worksheet("Data")

# Finding Treasure Sheets Loading
des = gc.open("Data Encounter Sheet")
encounters = des.worksheet("Encounter Tables")

# Loading Arcana Edges Information
arcana = service.documents().get(documentId="1gc6eTktgcQo9zViLghnWfxWmNrFzKKH6Y4QWMlwMzlo").execute()

# Red's April Fools Day Command Info
red = gc.open("them beans")
pos = red.worksheet("Positive")
neg = red.worksheet("Negative")
intro = red.worksheet("Intro")


# PDFs for PDF commands
pokedex = fitz.Document("Documents/Phemenon Pokedex.pdf")
lore_doc = fitz.Document("Documents/Phemenon Lore Book.pdf")
compendium = fitz.Document("Documents/Mythology Compendium.pdf")

max_page = 1211


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
        return ["There is no legend by that name. Did you mean  . Please try again."]
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
    Recurses through ability dictionary in the larger infodex dictionary to find matching ability name, then returns
    matching description.
    :param name: String name of the ability in question
    :return: Description of the ability.
    """
    criteria = re.compile('(?i)^' + name + "$")  # Searches for the entered name regardless of capitalization and formatting.
    if any((match := criteria.search(item)) for item in abilities.keys()):  # This code checks if any of the keys in
        # the abilities dictionary match the search criteria and assigns the match object to the variable "match" if
        # a match is found.
        data_block = abilities[match.group(0)]  # Stores matching dict entry in data block variable
        ability_name = data_block["Name"]  # retrieves ability name from dict entry
        ability_freq = "\n" + data_block["Frequency"]  # retrieves ability frequency from dict entry
        ability_eff = "\n" + data_block["Effect 2"]  # retrieves ability effect from dict entry
        return [ability_name, ability_freq, ability_eff]  # Returns information variables for the bot to format later.
    else:  # Activates in the case where no keys match the search criteria, meaning that no ability of that name exists.
        similar_word = find_most_similar_string(abilities.keys(),
                                                name.lower())  # Uses the find_most_similar_string function to locate
        # the key in abilities which can be transformed into the name parameter string in the fewest amount of
        # transformations.
        return ["There is no ability by that name. Did you mean " + similar_word + "?"]


''' 
Most get_x_data functions follow similar logic to get_ability_data in terms of how the code works. 
'''


def get_feature_data(name):
    criteria = re.compile('(?i)^' + name.replace("(", "\(").replace(")", "\)") + "$")
    if any((match := criteria.search(item)) for item in features.keys()):
        data_block = abilities[match.group(0)]
        feature_name = data_block["Name"]
        feature_pre = "\n" + data_block["Prerequisites"]
        feature_tag = "\n" + data_block["Tags"]
        feature_freq = "\n" + data_block["Frequency - Action"]
        feature_eff = "\n" + data_block["Effects"]
        return [feature_name, feature_pre, feature_tag, feature_freq, feature_eff]
    else:
        similar_word = find_most_similar_string(features.keys(), name.lower())
        print(similar_word)
        return ["There is no feature by that name. Did you mean " + similar_word + "?"]


def get_item_data(name):
    criteria = re.compile('(?i)^' + name + "$")
    if any((match := criteria.search(item)) for item in items.keys()):
        data_block = items[match.group(0)]
        item_name = data_block["Name"]
        item_eff = "\n" + data_block["Effect"]
        return [item_name, item_eff]
    else:
        similar_word = find_most_similar_string(items.keys(), name.lower())
        print(similar_word)
        return ["There is no item by that name. Did you mean " + similar_word + "?"]


def get_edge_data(name):
    criteria = re.compile('(?i)^' + name + "$")
    if any((match := criteria.search(item)) for item in edges.keys()):
        data_block = edges[match.group(0)]
        edge_name = data_block["Name"]
        edge_prereq = "\n" + data_block["Prerequisites"]
        edge_eff = "\n" + data_block["Effect"]
        return [edge_name, edge_prereq, edge_eff]
    else:
        similar_word = find_most_similar_string(edges.keys(), name.lower())
        print(similar_word)
        return ["There is no edge by that name. Did you mean " + similar_word + "?"]


def get_move_data(name):
    criteria = re.compile('(?i)^' + name + "$")
    if any((match := criteria.search(item)) for item in moves.keys()):
        data_block = moves[match.group(0)]
        move_name = "Name: " + data_block["Attack Name"]
        move_type = "\nType: " + data_block["Type"]
        move_class = "\n" + data_block["Class"]
        move_freq = "\n" + data_block["Frequency"]
        move_range = "\n" + data_block["Range"]
        move_ac = "\nAC: " + data_block["AC"]
        move_db = "\nDB: " + data_block["DB"]
        move_eff = "\nEffect: " + data_block["Effect"]
        move_tag = "\nStyle Tag: " + data_block["Flair Battle Type / Effect"]
        return [move_name, move_type, move_class, move_freq, move_range, move_ac, move_db, move_eff, move_tag]
    else:
        similar_word = find_most_similar_string(moves.keys(), name.lower())
        print(similar_word)
        return ["There is no move by that name. Did you mean " + similar_word + "?"]


def list_habitats(name):
    criteria = re.compile('(?i)^' + name + "$")
    match = habitat.find(criteria, in_column=1)
    if match is None:
        similar_word = find_most_similar_string(habitat.col_values(1), name.lower())
        return "This is either not the species's basic form, it cannot be found anywhere at the moment, or it is misspelled. Did you mean " + similar_word + "?"
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
    options = mechanics.keys()
    del options[:2]
    return options


def get_mechanic(name):
    criteria = re.compile('(?i)^' + name + "$")
    if any((match := criteria.search(item)) for item in mechanics.keys()):
        data_block = mechanics[match.group(0)]
        ret_string = "Mechanic: " + data_block["Mechanic"] + "\n\nEffect: " + data_block["Effect"]
        return ret_string


def get_technique(name):
    criteria = re.compile('(?i)^' + name + "$")
    if any((match := criteria.search(item)) for item in techniques.keys()):
        data_block = techniques[match.group(0)]
        ret_string = data_block["Name"]
        ret_string += "\nPrerequisities: " + data_block["Prerequisites"]
        ret_string += "\nFrequency / Cost: " + data_block["Frequency / Cost"]
        ret_string += "\n\n" + data_block["Effect"]
        return ret_string
    else:
        similar_word = find_most_similar_string(techniques.keys(), name.lower())
        print(similar_word)
        return "There is no technique by that name. Did you mean " + similar_word + "?"


def get_order(name):
    criteria = re.compile('(?i)^' + name + "$")
    if any((match := criteria.search(item)) for item in orders.keys()):
        data_block = orders[match.group(0)]
        ret_string = data_block["Name"]
        ret_string += "\n" + data_block["Frequency - Action"]
        ret_string += "\n\n" + data_block["Effects"]
        return ret_string
    else:
        similar_word = find_most_similar_string(features.col_values(6), name.lower())
        print(similar_word)
        return "There is no general order by that name. Did you mean " + similar_word + "?"


def get_keyword_moves(name):
    criteria = re.compile('(?i)' + name)
    ret_array = []
    for item in moves.values():
        if re.search(criteria, item.get("Range", "")) is not None:
            ret_array.append(item["Attack Name"])
    if len(ret_array) != 0:
        ret_string = "Here is a list of all moves with that keyword: " + ", ".join(ret_array)
        return ret_string
    else:
        return "That is not a valid attack Keyword. Please try again"


def get_flair_moves(name, typing):
    criteria = re.compile('(?i)' + name)
    ret_array = []
    for item in moves.values():
        if (re.search(criteria, item["Flair Battle Type / Effect"]) is not None) and (item["Type"] == typing.title()):
            ret_array.append(item["Attack Name"])
    if len(ret_array) != 0:
        ret_string = "Here is a list of all moves of type " + typing.title() + " with the style tag " + name.title() + ": " + ", ".join(ret_array)
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
    if any((match := criteria.search(item)) for item in maneuvers.keys()):
        data_block = maneuvers[match.group(0)]
        manu_name = "Name: " + data_block["Name"]
        manu_class = "\n" + data_block["Class"]
        manu_freq = "\n" + data_block["Action"]
        manu_range = "\n" + data_block["Range"]
        manu_ac = "\nAC: " + data_block["AC"]
        manu_eff = "\nEffect: " + data_block["Effect"]
        return [manu_name, manu_class, manu_freq, manu_range, manu_ac, manu_eff]
    else:
        similar_word = find_most_similar_string(moves.keys(), name.lower())
        print(similar_word)
        return ["There is no move by that name. Did you mean " + similar_word + "?"]


def get_cap_data(name):
    criteria = re.compile('(?i)^' + name + "$")
    if any((match := criteria.search(item)) for item in capabilities.keys()):
        data_block = capabilities[match.group(0)]
        item_name = data_block["Capability"]
        item_eff = "\n" + data_block["Description"]
        return [item_name, item_eff]
    else:
        similar_word = find_most_similar_string(capabilities.keys(), name.lower())
        print(similar_word)
        return ["There is no capability by that name. Did you mean " + similar_word + "?"]


def get_keyword_data(name):
    criteria = re.compile('(?i)^' + name + "$")
    if any((match := criteria.search(item)) for item in keywords.keys()):
        data_block = keywords[match.group(0)]
        item_name = data_block["Attack Keyword"]
        item_eff = "\n" + data_block["Effect"]
        return [item_name, item_eff]
    else:
        similar_word = find_most_similar_string(capabilities.keys(), name.lower())
        print(similar_word)
        return ["There is no keyword by that name. Did you mean " + similar_word + "?"]


def get_status_data(name):
    criteria = re.compile('(?i)^' + name + "$")
    if any((match := criteria.search(item)) for item in statuses.keys()):
        data_block = statuses[match.group(0)]
        item_name = data_block["Status"]
        item_eff = "\n" + data_block["Effect"]
        return [item_name, item_eff]
    else:
        similar_word = find_most_similar_string(statuses.keys(), name.lower())
        print(similar_word)
        return ["There is no status by that name. Did you mean " + similar_word + "?"]


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


"""


def get_beans():
    bean_list = neg if random.randint(1, 4) == 4 else pos
    intro_choice = intro.col_values(1)
    bean_options = bean_list.col_values(1)
    bean_taste = random.choice(bean_options)
    intro_text = random.choice(intro_choice)
    return intro_text + " " + bean_taste
"""
