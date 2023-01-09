import random

import fitz
import gspread
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from CollectData import infodex, worlddex, bossdex
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
books = infodex["books"]
weathers = infodex["weathers"]
affiliations = infodex["affiliations"]
heritages = infodex["heritages"]
influences = infodex["influences"]
habitat = gc.open("Data Habitat Areas").worksheet("Data")
patrons = bossdex["Patrons"]
guardians = bossdex["Guardians"]

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
    if prereq_list == "" or legend == "":
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

def get_domain_edges(domain):
    edges_array = []
    criteria = re.compile('(?i)' + domain)
    if any((match := criteria.search(item["Prerequisites"])) for item in edges.values()):
        data_blocks = match.groups()
        for dict in data_blocks:
            data_block = edges[match.group(0)]
            arcana_edge = data_block["Name"]
            arcana_edge += "\n" + data_block["Prerequisites"]
            arcana_edge += "\n" + data_block["Effect"]
            edges_array.append(arcana_edge)
        return edges_array
    else:
        similar_word = find_most_similar_string(DOMAINS, domain.title())
        return ["There is no domain by that name. Did you mean " + similar_word + "?"]

def get_ability_data(name):
    """
    Recurses through ability dictionary in the larger infodex dictionary to find matching ability name, then returns
    matching description.
    :param name: String name of the ability in question
    :return: Description of the ability.
    """
    criteria = re.compile(
        '(?i)^' + re.escape(name) + "$")  # Searches for the entered name regardless of capitalization and formatting.
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
    criteria = re.compile('(?i)^' + re.escape(name).replace("(", "\(").replace(")", "\)") + "$")
    if any((match := criteria.search(item)) for item in features.keys()):
        data_block = features[match.group(0)]
        feature_name = data_block["Name"]
        feature_pre = "\n" + data_block["Prerequisites"]
        feature_tag = "\n" + data_block["Tags"]
        feature_freq = "\n" + data_block["Frequency - Action"]
        feature_eff = "\n" + data_block["Effects"]
        return [feature_name, feature_pre, feature_tag, feature_freq, feature_eff]
    else:
        similar_word = find_most_similar_string(features.keys(), name.lower())

        return ["There is no feature by that name. Did you mean " + similar_word + "?"]


def get_item_data(name):
    criteria = re.compile('(?i)^' + re.escape(name) + "$")
    if any((match := criteria.search(item)) for item in items.keys()):
        data_block = items[match.group(0)]
        item_name = data_block["Name"]
        item_eff = "\n" + data_block["Effect"]
        return [item_name, item_eff]
    else:
        similar_word = find_most_similar_string(items.keys(), name.lower())

        return ["There is no item by that name. Did you mean " + similar_word + "?"]


def get_edge_data(name):
    criteria = re.compile('(?i)^' + re.escape(name) + "$")
    if any((match := criteria.search(item)) for item in edges.keys()):
        data_block = edges[match.group(0)]
        edge_name = data_block["Name"]
        edge_prereq = "\n" + data_block["Prerequisites"]
        edge_eff = "\n" + data_block["Effect"]
        return [edge_name, edge_prereq, edge_eff]
    else:
        similar_word = find_most_similar_string(edges.keys(), name.lower())

        return ["There is no edge by that name. Did you mean " + similar_word + "?"]


def get_trait_data(name):
    criteria = re.compile('(?i)^' + re.escape(name) + "$")
    if any((match := criteria.search(item)) for item in edges.keys()):
        data_block = edges[match.group(0)]
        edge_name = data_block["Name"]
        edge_prereq = "\n" + data_block["Prerequisites"]
        edge_eff = "\n" + data_block["Effect"]
        return [edge_name, edge_prereq, edge_eff]
    else:
        similar_word = find_most_similar_string(edges.keys(), name.lower())

        return ["There is no trait by that name. Did you mean " + similar_word + "?"]


def get_move_data(name):
    criteria = re.compile('(?i)^' + re.escape(name) + "$")
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

        return ["There is no move by that name. Did you mean " + similar_word + "?"]


def list_habitats(name):
    criteria = re.compile('(?i)^' + re.escape(name) + "$")
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
    criteria = re.compile('(?i)^' + re.escape(name) + "$")
    if any((match := criteria.search(item)) for item in mechanics.keys()):
        data_block = mechanics[match.group(0)]
        ret_string = "Mechanic: " + data_block["Mechanic"] + "\n\nEffect: " + data_block["Effect"]
        return ret_string


def get_technique(name):
    criteria = re.compile('(?i)^' + re.escape(name) + "$")
    if any((match := criteria.search(item)) for item in techniques.keys()):
        data_block = techniques[match.group(0)]
        ret_string = data_block["Name"]
        ret_string += "\nPrerequisities: " + data_block["Prerequisites"]
        ret_string += "\nFrequency / Cost: " + data_block["Frequency / Cost"]
        ret_string += "\n\n" + data_block["Effect"]
        return ret_string
    else:
        similar_word = find_most_similar_string(techniques.keys(), name.lower())

        return "There is no technique by that name. Did you mean " + similar_word + "?"


def get_order(name):
    criteria = re.compile('(?i)^' + re.escape(name) + "$")
    if any((match := criteria.search(item)) for item in orders.keys()):
        data_block = orders[match.group(0)]
        ret_string = data_block["Name"]
        ret_string += "\n" + data_block["Frequency - Action"]
        ret_string += "\n\n" + data_block["Effects"]
        return ret_string
    else:
        similar_word = find_most_similar_string(features.col_values(6), name.lower())
        return "There is no general order by that name. Did you mean " + similar_word + "?"


def get_keyword_moves(name):
    criteria = re.compile('(?i)^' + re.escape(name) + "$")
    if any((match := criteria.search(item)) for item in keywords.keys()):
        ret_array = []
        for item in moves.values():
            if re.search(criteria, item.get("Range", "")) is not None:
                ret_array.append(item["Attack Name"])
        if len(ret_array) != 0:
            ret_string = "Here is a list of all moves with that keyword: " + ", ".join(ret_array)
            return ret_string
        else:
            return "No moves were found with that keyword."
    else:
        similar_word = find_most_similar_string(keywords.keys(), name.lower())
        return ["There is no keyword by that name. Did you mean " + similar_word + "?"]


def get_flair_moves(name, typing):
    criteria = re.compile('(?i)' + name)
    ret_array = []
    for item in moves.values():
        if (re.search(criteria, item["Flair Battle Type / Effect"]) is not None) and (item["Type"] == typing.title()):
            ret_array.append(item["Attack Name"])
    if len(ret_array) != 0:
        ret_string = "Here is a list of all moves of type " + typing.title() + " with the style tag " + name.title() + ": " + ", ".join(
            ret_array)
        return ret_string
    else:
        return "That is not a valid style tag. Please try again"


def poke_ability(name):
    basic_array = [pokemon['name'].title() for pokemon in ALLPOKEMON.values() if
                   name.lower() in (item.lower() for item in pokemon['abilities'])]
    adv_array = [pokemon['name'].title() for pokemon in ALLPOKEMON.values() if
                 name.lower() in (item.lower() for item in pokemon['advabilities'])]
    high_array = [pokemon['name'].title() for pokemon in ALLPOKEMON.values() if
                  name.lower() in (item.lower() for item in pokemon['highabilities'])]
    ret_string = "**__Here is a list of all the pokemon with the ability " + name.title() + ":__**\n**Obtained as a Basic Ability:** " + ", ".join(
        basic_array) + "\n\n**Obtained as an Advanced Ability:** " + ", ".join(
        adv_array) + "\n\n**Obtained as a High Ability:** " + ", ".join(high_array)
    return ret_string


def learn_move(name):
    criteria = re.compile('(?i)^' + re.escape(name) + "$")
    if any((match := criteria.search(item)) for item in moves.keys()):
        tm_array = [pokemon['name'].title() for pokemon in ALLPOKEMON.values() for full_name in pokemon["moves"] if
                    name.lower() in full_name.lower() if "Tutor" in full_name]
        lvl_array = [pokemon['name'].title() for pokemon in ALLPOKEMON.values() for full_name in pokemon["moves"] if
                     name.lower() in full_name.lower() if "Tutor" not in full_name]
        tm_array.sort()
        lvl_array.sort()
        ret_string = "**__Here is a list of all the pokemon who can learn the move " + name.title() + ":__** \n**Can Learn by Level Up:** " + ", ".join(
            lvl_array) + "\n\n**Can learn through Move Tutor:** " + ", ".join(tm_array)
        return ret_string
    else:
        similar_word = find_most_similar_string(moves.keys(), name.lower())
        return "There is no move by that name. Did you mean " + similar_word + "?"


def poke_capability(name):
    criteria = re.compile('(?i)^' + re.escape(name) + "$")
    if any((match := criteria.search(item)) for item in capabilities.keys()):
        capa_array = [pokemon['name'].title() for pokemon in ALLPOKEMON.values() for full_name in pokemon["Capabilities"] if
                    name.title() == full_name.title()]
        capa_array.sort()
        ret_string = "**__Here is a list of all the pokemon who can have the capability " + name.title() + ":__** \n" + ", ".join(
            capa_array)
        return ret_string
    else:
        similar_word = find_most_similar_string(capabilities.keys(), name.lower())
        return "There is no move by that name. Did you mean " + similar_word + "?"


def poke_flair(name, flair):
    criteria = re.compile('(?i)^' + re.escape(name) + "$")
    if any((match := criteria.search(item)) for item in ALLPOKEMON.keys()):
        data_block = ALLPOKEMON[match.group(0)]
        level_list = [full_name.split(" ", maxsplit=1)[1] for full_name in data_block["moves"] if
                      "Tutor" not in full_name]
        tutor_list = [full_name.split(" ", maxsplit=1)[1] for full_name in data_block["moves"] if "Tutor" in full_name]
        level_flair_moves = [move_name for move_name in level_list if
                             moves[move_name]["Flair Battle Type / Effect"] == flair.title()]
        tm_flair_moves = [move_name for move_name in tutor_list if
                          moves[move_name]["Flair Battle Type / Effect"] == flair.title()]
        ret_string = "**__Here is a list of all moves learned by " + name.title() + " with the style tag " + flair.title() + ":__** \n**Can Learn by Level Up:** " + ", ".join(
            level_flair_moves) + "\n\n**Can learn through Move Tutor:** " + ", ".join(tm_flair_moves)
        return ret_string

    else:
        similar_word = find_most_similar_string(ALLPOKEMON.keys(), name.upper())
        return ["There is no pokemon by that name. Did you mean " + similar_word.title() + "?"]


def get_info_categories(name):
    criteria = re.compile('(?i)^' + re.escape(name) + "$")
    categories = []
    for key, value in infodex.items():
        if any((match := criteria.search(item)) for item in value.keys()):
            categories.append(key.title())
    if categories != []:
        ret_string = "**__Entries of that name can be found within the following classifications:__** \n" + ", ".join(categories)
        return ret_string
    else:
        similar_words = []
        for key, value in infodex.items():
            similar_words.append(find_most_similar_string(value.keys(), name.lower()))
        similar_word = find_most_similar_string(similar_words, name.lower())
        return "There is no entry by that name. Did you mean " + similar_word + "?"


def get_man_data(name):
    criteria = re.compile('(?i)^' + re.escape(name) + "$")
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
        return ["There is no move by that name. Did you mean " + similar_word + "?"]


def get_cap_data(name):
    criteria = re.compile('(?i)^' + re.escape(name) + "$")
    if any((match := criteria.search(item)) for item in capabilities.keys()):
        data_block = capabilities[match.group(0)]
        item_name = data_block["Capability"]
        item_eff = "\n" + data_block["Description"]
        return [item_name, item_eff]
    else:
        similar_word = find_most_similar_string(capabilities.keys(), name.lower())
        return ["There is no capability by that name. Did you mean " + similar_word + "?"]


def get_keyword_data(name):
    criteria = re.compile('(?i)^' + re.escape(name) + "$")
    if any((match := criteria.search(item)) for item in keywords.keys()):
        data_block = keywords[match.group(0)]
        item_name = data_block["Attack Keyword"]
        item_eff = "\n" + data_block["Effect"]
        return [item_name, item_eff]
    else:
        similar_word = find_most_similar_string(keywords.keys(), name.lower())
        return ["There is no keyword by that name. Did you mean " + similar_word + "?"]


def get_status_data(name):
    criteria = re.compile('(?i)^' + re.escape(name) + "$")
    if any((match := criteria.search(item)) for item in statuses.keys()):
        data_block = statuses[match.group(0)]
        item_name = data_block["Status"]
        item_eff = "\n" + data_block["Effect"]
        item_boss = "\n" + data_block["Boss Effect"]
        return [item_name, item_eff, item_boss]
    else:
        similar_word = find_most_similar_string(statuses.keys(), name.lower())
        return ["There is no status by that name. Did you mean " + similar_word + "?"]


def get_book_data(name):
    criteria = re.compile('(?i)^' + re.escape(name) + "$")
    if any((match := criteria.search(item)) for item in books.keys()):
        data_block = books[match.group(0)]
        book_name = data_block["Book Name"]
        book_eff = "\n" + data_block["Book Effect"]
        book_topic = "\nTopic: " + data_block["Book Topic"]
        book_enc = "\nEncryption Type: " + data_block["Encryption Type"]
        book_enc_dc = "\nEncryption DC: " + data_block["Encryption DC"]
        book_type = "\nBook Type: " + data_block["Book Type"]
        book_dc = "\nBook DC: " + data_block["Book DC"]
        return [book_name, book_eff, book_topic, book_enc, book_enc_dc, book_type, book_dc]
    else:
        similar_word = find_most_similar_string(books.keys(), name.lower())
        return ["There is no book by that name. Did you mean " + similar_word + "?"]


def get_weather_data(name):
    criteria = re.compile('(?i)^' + re.escape(name) + "$")
    if any((match := criteria.search(item)) for item in weathers.keys()):
        data_block = weathers[match.group(0)]
        weather_name = data_block["Weather"]
        weather_eff = "\n" + data_block["Effect"]
        return [weather_name, weather_eff]
    else:
        similar_word = find_most_similar_string(weathers.keys(), name.lower())
        return ["There is no weather by that name. Did you mean " + similar_word + "?"]


def get_heritage_data(name):
    criteria = re.compile('(?i)^' + re.escape(name) + "$")
    if any((match := criteria.search(item)) for item in heritages.keys()):
        data_block = heritages[match.group(0)]
        heritage_name = data_block["Heritage Name"]
        heritage_eff = "\n" + data_block["Heritage Benefits"]
        heritage_topic = "\nDescription: " + data_block["Heritage Description"]
        return [heritage_name, heritage_eff, heritage_topic]
    else:
        similar_word = find_most_similar_string(heritages.keys(), name.lower())
        return ["There is no heritage by that name. Did you mean " + similar_word + "?"]


def get_affiliation_data(name):
    criteria = re.compile('(?i)^' + re.escape(name) + "$")
    if any((match := criteria.search(item)) for item in affiliations.keys()):
        data_block = affiliations[match.group(0)]
        affiliation_name = data_block["Affiliation Name"]
        affiliation_eff = "\nExamples: " + data_block["Affiliation Examples"]
        affiliation_benefits = "\n" + data_block["Affiliation Benefits"]
        affiliation_desc = "\nDescription: " + data_block["Affiliation Description"]
        return [affiliation_name, affiliation_eff, affiliation_benefits, affiliation_desc]
    else:
        similar_word = find_most_similar_string(affiliations.keys(), name.lower())
        return ["There is no affiliation by that name. Did you mean " + similar_word + "?"]


def get_influence_data(name):
    criteria = re.compile('(?i)^' + re.escape(name) + "$")
    if any((match := criteria.search(item)) for item in influences.keys()):
        data_block = influences[match.group(0)]
        influence_name = data_block["Influence Name"]
        influence_eff = "\n" + data_block["Influence Effects"]
        return [influence_name, influence_eff]
    else:
        similar_word = find_most_similar_string(influences.keys(), name.lower())
        return ["There is no influence by that name. Did you mean " + similar_word + "?"]


def get_treasure_spot(name):
    match = search_cell_value(worlddex, name)
    if match[0] == "NO MATCH FOUND":
        return "No Treasure of that name can be found. Did you mean " + match[1] + "?"
    else:
        ret_val = "**That treasure can be found in the following adventures areas:** " + ", ".join(match)
        return ret_val


def get_dex_entry(name):
    pix = pokedex[ALLPOKEMON[name.upper()]["Page Num"]].get_pixmap()
    pix.save("{0}.png".format(name.lower()))


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

def get_wander_event():
    wander_event = random.choice(infodex["wanders"].values())
    name = "**" + wander_event["Event Name"] + "**"
    effect = "\n\n" + wander_event["Details"]
    ret_string = name
    ret_string += effect
    return ret_string


def get_legend_personality(legend):
    criteria = re.compile('(?i)^' + legend + "$")  # get all the cells with the name of the legend in them in column 1
    if any((match := criteria.search(item)) for item in patrons.keys()):
        legend_name = match[0]
        legend_personality = patrons[legend_name]['Personality']
        personality = "__**" + legend_name.title() + "**__\n" + "**Personality:** " + legend_personality
        return personality

    else:
        similar_word = find_most_similar_string(patrons.keys(), legend.title())
        return "A legend with this name could not be found. Did you mean " + similar_word + "?"


def get_patronage_task(legend, category):
    criteria = re.compile('(?i)^' + legend + "$")  # get all the cells with the name of the legend in them in column 1
    if any((match := criteria.search(item)) for item in patrons.keys()):
        legend_name = match[0]
        legend_personality = patrons[legend_name]['Personality']
        personality = "__**" + legend_name.title() + "**__\n" + "**Personality:** " + legend_personality
        subtask_variant = random.choice(list(patrons[legend_name][category.title()].keys()))
        subtask = "**" + subtask_variant + "**\n" + random.choice(patrons[legend_name][category.title()][subtask_variant])  # Selects the sub task
        subtask_array = segment_text(subtask, "Legend")
        personality_array = [personality]
        return personality_array + subtask_array

    else:
        similar_word = find_most_similar_string(patrons.keys(), legend.title())
        return "A legend with this name could not be found. Did you mean " + similar_word + "?"


def get_guardian_info(area):
    criteria = re.compile('(?i)^' + area + "$")  # get all the cells with the name of the legend in them in column 1
    if any((match := criteria.search(item)) for item in guardians.keys()):
        data_block = guardians[match.group(0)]
        guardian_string = data_block["Guardian"]
        guardian_string += "\n" + data_block["Details"]
        return guardian_string

    else:
        similar_word = find_most_similar_string(guardians.keys(), area.title())
        return "An area with that name that has a guardian could not be found. Did you mean " + similar_word + "?"


# def generate_tutor_list():
#     pokedict = {}
#     for item in ALLPOKEMON:
#         pokedict[item["name"]] = item
#     for entry in pokedex.pages(11, max_page):
#         tutor_rect = fitz.Rect(360, 386, 576, 690)
#         name_rect = fitz.Rect(28, 0, 457, 60)
#         word_page = entry.get_text("words")
#         tutor_temp = [w for w in word_page if fitz.Rect(w[:4]) in tutor_rect]
#         tutor_moves = make_text(tutor_temp)
#         temp = [w for w in word_page if fitz.Rect(w[:4]) in name_rect]
#         poke_name = make_text(temp)
#         index = poke_name.find(" - ")
#         name_search = poke_name if index == -1 else poke_name[index + 3:]
#         tutor_moves = tutor_moves.replace(" Unique:", ",")
#         tutor_moves = tutor_moves.replace("Unique: ", "")
#         tutor_moves = tutor_moves.replace(" Generic:", ",")
#         tm_list = tutor_moves.split(", ")
#         criteria = re.compile('(?i)^' + re.escape(name)_search + "$")
#         if any((match := criteria.search(item)) for item in pokedict.keys()):
#             data_block = pokedict[match.group(0)]
#             for attack in tm_list:
#                 data_block["moves"].append("Tutor " + attack)
#
#     # Iterate over the rows of data and add them to the dictionary
#     with open('Uncommited Files/pokemon.txt', 'w', encoding='utf-8') as f:
#         # Write the dictionary to the file as a string
#         f.write(str(pokedict))

# def generate_dex_info():
#     pokedict = {}
#     pokedata = pokemon_data.get_all_values()
#     for item in ALLPOKEMON.values():
#         pokedict[item["name"]] = item
#     key_row = pokedata[0][0:33]
#     for i, row in enumerate(pokedata):
#         if i == 0:
#             continue
#         pokemon_name = row[0].upper()
#         if pokedict.get(pokemon_name) is not None:
#             for j in range(len(key_row)):
#                 pokedict[pokemon_name][key_row[j]] = row[j]
# 
#     # Iterate over the rows of data and add them to the dictionary
#     with open('Uncommited Files/pokemon.py', 'w', encoding='utf-8') as f:
#         # Write the dictionary to the file as a string
#         f.write(str(pokedict))
#

# def get_dex_page_numbers():
#     pokedict = ALLPOKEMON
#     page_num = 12
#     for entry in pokedex.pages(12, max_page):
#         cap_rect = fitz.Rect(10, 450, 311, 532)
#         name_rect = fitz.Rect(28, 0, 457, 60)
#         word_page = entry.get_text("words")
#         temp = [w for w in word_page if fitz.Rect(w[:4]) in name_rect]
#         poke_name = make_text(temp)
#         if poke_name.upper() in ALLPOKEMON.keys():
#             pokedict[poke_name.upper()]["Page Num"] = page_num
#         else:
#             print(poke_name)
#         page_num += 1
#     with open('pokemon.py', 'w', encoding='utf-8') as f:
#         # Write the dictionary to the file as a string
#         f.write(str(pokedict))

# def add_missing_page_numbers():
#     pokedict = ALLPOKEMON
#     for key in ALLPOKEMON.keys():
#         pokedict[key]["Capabilities"] = [v for k, v in pokedict[key].items() if k.startswith("Capability ") and v != "-"]
#         for i in range(10):
#             if pokedict[key].get("Capability " + str(i + 1)) is not None:
#                 del pokedict[key]["Capability " + str(i + 1)]
#             else:
#                 print(key)
#                 break
#     with open('Uncommited Files/pokemon.py', 'w', encoding='utf-8') as f:
#         # Write the dictionary to the file as a string#
#         f.write(str(pokedict))
#
#
# add_missing_page_numbers()

