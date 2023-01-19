import random
import time

from CollectData import worlddex
from utilities import *

harvests = worlddex['Harvest Slots']


def generate_forage(skill_rank, area, num_rolls):
    t1_start = time.perf_counter()
    criteria = re.compile('(?i)^' + area + "$")
    if any((match := criteria.search(item)) for item in harvests.keys()):
        data_block = harvests[match.group(0)]
        ret_string = ""
        desc_string = ""
        for i in range(int(num_rolls)):
            roll_list = []
            roll = random.randint(1, 10)
            roll_list.append(roll)
            if skill_rank > 3:
                roll_list.append(roll - 1 if roll != 1 else 1)
            if skill_rank > 5:
                roll_list.append(roll + 1 if roll != 10 else 10)
            ret_string += "HERE ARE THE ITEMS WHICH YOU CAN ENCOUNTER ON FORAGE NUMBER {0}:".format(i + 1)
            roll_list.sort()
            for item in roll_list:
                # print("{0}: {1}".format(item, math.floor(item / 2) + 1))
                slot_value = data_block[str(item)]
                slot_string = slot_value[0] + (" (Desc. at the End)" if slot_value[1] is not None else "")
                ret_string += "\nSlot {0}: {1}".format(item, slot_string)
                if slot_value[1] is not None:
                    slot_desc = slot_value[0] + "\nDescription: " + slot_value[1]
                    if "\nSlot {0}: {1}\n".format(item, slot_desc) not in desc_string:
                        desc_string += "\nSlot {0}: {1}\n".format(item, slot_desc)
            ret_string += "\n\n"
        t1_stop = time.perf_counter()
        ret_string += "\n\nSlot Descriptions:\n\n" + desc_string
        return ret_string
    else:
        similar_word = find_most_similar_string(harvests.keys(), area.lower())
        print(similar_word)
        return "There is no forage-able area with that name. Did you mean " + similar_word + "?"


def get_encounter_slot(encounter_table, adventure_details, forced_slot=None):
    encounter_key = random.choice(encounter_table.keys()) if forced_slot is None else forced_slot
    encounter_value = encounter_table[encounter_key]
    encounter_flag = encounter_table[encounter_key][2]
    if encounter_flag in ["Minor Treasure", "Major Treasure", "Alpha Aberration"]:
        if (adventure_details["Get Treasure"][0] is False) or (
                adventure_details["Get Treasure"][1] is False and encounter_flag == "Major Treasure"):
            # Triggers if a treasure slot is rolled but the treasure is invalid to add
            adventure_details = get_encounter_slot(encounter_table, adventure_details)
        else:
            adventure_details["Treasure Rolled"] = encounter_value  # Remember to Roll for a mon guarding it later.
            adventure_details["Get Treasure"] = (False, False)
    elif encounter_flag == "Guardian" and adventure_details["Get Treasure"][2] is True:
        adventure_details["Event"] = 20
        adventure_details["Get Treasure"][2] = False
    else:
        adventure_details["Encounters"].append(encounter_value)
    return adventure_details


def reveal_encounter_slot_only(area_name, encounter_slot):
    area_keys = worlddex["Encounter Slots"].keys()
    area_match = find_most_similar_string(area_keys, area_name.title())
    encounter_table = worlddex["Encounter Slots"][area_match]
    revealed_slot = encounter_table[encounter_slot]
    ret_string = "Encounter in slot {0}".format(str(encounter_slot)) + "  of area {0} is: ".format(area_match) + \
                 revealed_slot[0] + "\n"
    if revealed_slot[1] is not None:
        ret_string += "**Description:**\n" + revealed_slot[1]
    return ret_string


def get_event_slot(event_table, adventure_details, forced_slot=None):
    event_key = random.choice(event_table.keys()) if forced_slot is None else forced_slot
    event_slot = event_table[event_key]
    adventure_details["Event"] = event_slot
    return adventure_details


def generate_adventure(gm_info):
    area_dict = worlddex["Encounter Slots"][gm_info["Area"]]
    encounter_table = {key: val for key, val in area_dict.items() if key not in gm_info["Repel Array"]}
    event_table = worlddex["Event Slots"][gm_info["Area"]]
    area_details = worlddex["Effect Slots"][gm_info["Area"]]
    can_be_treasure_flag = (True, True if gm_info[
                                              "Avg Poke Lvl"] >= 45 else False,
                            True if gm_info["Avg Trainer Lvl"] >= 20 else False)  # (Can be a treasure at all, party
    # high enough level for major treasure, Can Still Role Guardian). True means available

    adventure_details = {
        "Encounters": [],
        "Get Treasure": can_be_treasure_flag,
        "Event": None,
        "Honor Spent": 0,
        "Treasure Rolled": None,
        "Treasure Guardian": None,
        "Area Description": ""
    }

    """
    Handles Treasure Hunting. Rolls treasure hunting dice based on information gained from gm_info. Sets Honor Spent to 
    number of roll attempts before success, if successful.
    """

    target = gm_info["TH Target"]
    num_encounters = gm_info["Num Players"] + gm_info["Extra Mons"] - gm_info["Forced Slot"]
    for num in range(gm_info["Num TH"]):
        if target in [random.choice(area_dict.keys()) for i in range(gm_info["Num Per TH"])]:
            adventure_details = get_encounter_slot(encounter_table, adventure_details, forced_slot=target)
            num_encounters -= 1
            adventure_details["Honor Spent"] = (num + 1)
            break

    # Getting all the encounters for the Adventure, including forced slots.
    if gm_info["Forced Slot"] != 0:  # Represents the case where a person forced an encounter slot.
        adventure_details = get_encounter_slot(encounter_table, adventure_details, gm_info["Forced Slot"])
    for i in range(num_encounters):
        adventure_details = get_encounter_slot(encounter_table, adventure_details)
    # Getting information on the Event for the Adventure
    if gm_info["Forced Event"] != 0 or adventure_details["Event"] is not None:
        adventure_details = get_event_slot(event_table, adventure_details,
                                           gm_info["Forced Slot"] if adventure_details["Event"]
                                                                     is None else adventure_details["Event"])
    else:
        adventure_details = get_event_slot(event_table, adventure_details)
    # Retrieves information about trial, features, and entry requirements.
    for key in area_details.keys():
        if area_details.get(key) is not None:
            adventure_details["Area Description"] += str(key) + ":\n " + str(area_details[key]) + "\n\n"

    # Clause for if Treasure Rolled is true
    if adventure_details["Treasure Rolled"] is not None:
        adventure_details["Treasure Guardian"] = get_encounter_slot(encounter_table, adventure_details)

    return(str(adventure_details))



# def get_mon(area, slot, sheet, note_sheet, non_treasure_flag=True):
#     criteria = re.compile('(?i)^' + area + "$")
#     area_match = sheet.find(criteria, in_row=1)
#     slot_match = sheet.find(str(slot), in_column=1)
#     if area_match is None:
#         return "There is no area with this name. Please try again"
#     if slot_match is None:
#         return "Please enter a valid encounter slot number."
#     match = sheet.cell(slot_match.row, area_match.col)
#     if match.value is None:
#         return "This area does not have that many slots. Please try again."
#     note_check = note_sheet.cell((match.row, match.col))
#     ret_string = "Encounter in slot {0}".format(slot) + "  of area {0} is: ".format(area) + match.value + "\n"
#     if note_check.note is not None:
#         ret_string += "**Note:**\n" + note_check.note + "\n"
#         if "treasure" in note_check.note.lower() or "abberation" in note_check.note.lower():
#             if not non_treasure_flag:
#                 ret_string += "\nPokemon accompanying Treasure / Pokemon that is Abberated is {0}\n\n".format(
#                     get_non_treasure(area_match.col, sheet, note_sheet))
#             else:
#                 new_mon = sheet.find(get_non_treasure(area_match.col, sheet, note_sheet), in_column=area_match.col)
#                 return get_mon(area, new_mon.row, sheet, note_sheet)
#
#         if "Check Note" in match.value:
#             ret_string += "\nThe d5 roll for the Rare Pokemon is {0}\n\n".format(random.randint(1, 5))
#     return ret_string

#
# def get_event(area, slot, sheet, note_sheet):
#     criteria = re.compile('(?i)^' + area + "$")
#     area_match = sheet.find(criteria, in_row=1)
#     slot_match = sheet.find(slot, in_column=1)
#     if area_match is None:
#         return "There is no area with this name. Please try again."
#     if slot_match is None:
#         return "Please enter a valid event slot number."
#     match = sheet.cell(slot_match.row, area_match.col)
#     if match.value is None:
#         return "This area does not have that many events. Please try again."
#     note_check = note_sheet.cell((match.row, match.col))
#     ret_string = ""
#     ret_string += "Event in slot {0}".format(slot) + " of area {0} is: ".format(area) + match.value + "\n"
#     if note_check.note is not None:
#         ret_string += "\n**Description:** " + note_check.note + "\n"
#     return ret_string
#
#
# def get_non_treasure(area_col, sheet, notes_sheet, min_lim=1, max_lim=100, slot_rev=False):
#     slot_num = str(random.randint(min_lim, max_lim))
#     slot_match = sheet.find(slot_num, in_column=1)
#     match = sheet.cell(slot_match.row, area_col)
#     while (notes_sheet.cell((match.row, match.col)).note is not None and "treasure" in notes_sheet.cell(
#             (match.row, match.col)).note.lower()) or match.value is None:
#         slot_num = random.randint(min_lim, max_lim)
#         slot_match = sheet.find(str(slot_num), in_column=1)
#         match = sheet.cell(slot_match.row, area_col)
#     ret_string = ""
#     if slot_rev:
#         ret_string += "Slot Number {0}: ".format(slot_num)
#     ret_string += match.value
#     return ret_string
#
#
# def get_hidden_slot_adventure(area, slot):
#     if any(area.lower() == val.lower() for val in adven_names):
#         return get_mon(area, slot, secret_adventures, sa_notes, False)
#     return get_mon(area, slot, secret_explorations, sx_notes, False)
#
#
# def get_hidden_event_adventure(area, slot):
#     return get_event(area, slot, secret_events, se_notes)
#
#
# def roll_hidden_adventure(area, tl, pl, luck_roll=None, event=None, rep_array=None, bait_mons=0, extra_players=0,
#                           th_attempts=None, th_target=None):
#     treasure_flag = False
#     ret_string = ''
#     guardianFlag = True if int(tl) >= 20 else False
#     majorTreasureFlag = True if int(pl) >= 45 else False
#     th_hits = None
#     max_val = 100
#     min_val = 1 if majorTreasureFlag else 2
#     criteria = re.compile('(?i)^' + area + "$")
#     area_match = secret_adventures.find(criteria, in_row=1)
#     if area_match is None:
#         return "There is no area with this name. Please try again"
#     if luck_roll is None:
#         luck_roll = str(random.randint(min_val, max_val))
#         slot_match = secret_adventures.find(luck_roll, in_column=area_match.col)
#         if slot_match is None:
#             max_val = 50
#             luck_roll = str(random.randint(min_val, max_val))
#             slot_match = secret_adventures.find(luck_roll, in_column=area_match.col)
#         if rep_array is not None:
#             while luck_roll in rep_array:
#                 luck_roll = str(random.randint(min_val, max_val))
#         if th_attempts is not None:
#             th_hits = []
#             for i in range(0, int(th_attempts)):
#                 th_roll = np.random.randint(min_val, max_val, 3)
#                 th_hits += th_roll.tolist()
#                 if int(th_target) in th_roll:
#                     luck_roll = str(th_target)
#                     break
#     ret_string += get_mon(area, luck_roll, secret_adventures, sa_notes)
#     if "treasure" in ret_string.lower():
#         treasure_flag = True
#     if extra_players != 0 or bait_mons != 0:
#         extra_mons = bait_mons + extra_players
#         for i in range(0, extra_mons):
#             if i == 3:
#                 time.sleep(60)
#             ret_string += "Extra Encounter {0} of {1} is: ".format(i + 1, extra_mons) + get_mon(area,
#                                                                                                 str(random.randint(
#                                                                                                     min_val,
#                                                                                                     max_val)),
#                                                                                                 secret_adventures,
#                                                                                                 sa_notes,
#                                                                                                 treasure_flag) + "\n"
#             if "treasure" in ret_string.lower() and treasure_flag == False:
#                 treasure_flag = True
#     if event is None:
#         event = str(random.randint(1, 20))
#     event_rolled = get_event(area, event, secret_events, se_notes)
#     swarm_addition = ""
#     if "Guardian Encounter" in event_rolled and not guardianFlag:
#         event_rolled = get_event(area, str(random.randint(1, 20)), secret_events, se_notes)
#     if "Major Pokemon Swarm" in event_rolled:
#         for i in range(0, (int(math.ceil(int(tl) / 15)))):
#             swarm_addition += "Swarm Pokemon {0} of {1} is: ".format(i + 1,
#                                                                      (int(math.ceil(int(tl) / 15)))) + get_non_treasure(
#                 area_match.col,
#                 secret_adventures,
#                 sa_notes,
#                 min_val,
#                 max_val, True) + "\n"
#     ret_string += event_rolled + swarm_addition + find_disposition(area)
#     if th_hits is not None:
#         ret_string += "\n\nHere are the treasure hunt rolls: " + ", ".join([str(num) for num in th_hits])
#     return ret_string
#
#
# def roll_exploration(area, tl, pl, luck_roll=None, event=None, rep_array=None, bait_mons=0, extra_players=0):
#     ret_string = ""
#     max_val = 30
#     min_val = 1 if tl >= 16 else 2
#     criteria = re.compile('(?i)^' + area + "$")
#     area_match = exploration_table.find(criteria, in_row=1)
#     if area_match is None:
#         return "There is no area with this name. Please try again"
#     if luck_roll is None:
#         luck_roll = str(random.randint(min_val, max_val))
#         slot_match = exploration_table.find(luck_roll, in_column=area_match.col)
#         if slot_match is None:
#             max_val = 20
#             luck_roll = str(random.randint(min_val, max_val))
#             slot_match = exploration_table.find(luck_roll, in_column=area_match.col)
#             if slot_match is None:
#                 max_val = 15
#                 luck_roll = str(random.randint(min_val, max_val))
#         if rep_array is not None:
#             while luck_roll in rep_array:
#                 luck_roll = str(random.randint(1, max_val))
#     ret_string += get_mon(area, luck_roll, exploration_table, et_notes)
#     if extra_players != 0 or bait_mons != 0:
#         extra_mons = bait_mons + extra_players
#         for i in range(0, extra_mons):
#             ret_string += "Extra Pokemon {0} of {1} is: ".format(i + 1, extra_mons) + get_non_treasure(area_match.col,
#                                                                                                        exploration_table,
#                                                                                                        et_notes,
#                                                                                                        min_val,
#                                                                                                        max_val) + "\n"
#     if event is None:
#         event = str(random.randint(1, 10))
#     ret_string += get_event(area, event, ex_events, ex_event_notes) + find_disposition(area)
#     if "Pokemon Swarm" in ret_string:
#         for i in range(0, 2):
#             ret_string += "Swarm Pokemon {0} of {1} is: ".format(i + 1, 2) + get_non_treasure(area_match.col,
#                                                                                               exploration_table,
#                                                                                               et_notes,
#                                                                                               min_val,
#                                                                                               max_val) + "\n"
#     return ret_string
#
#
# def roll_adventure(area, tl, pl, luck_roll=None, event=None, rep_array=None, bait_mons=0, extra_players=0,
#                    th_attempts=None, th_target=None):
#     treasure_flag = False
#     ret_string = ''
#     guardianFlag = True if int(tl) >= 20 else False
#     majorTreasureFlag = True if int(pl) >= 45 else False
#     th_hits = None
#     max_val = 100
#     min_val = 1 if majorTreasureFlag else 2
#     criteria = re.compile('(?i)^' + area + "$")
#     area_match = adventure_table.find(criteria, in_row=1)
#     if area_match is None:
#         return "There is no area with this name. Please try again"
#     if luck_roll is None:
#         luck_roll = str(random.randint(min_val, max_val))
#         slot_match = adventure_table.find(luck_roll, in_column=area_match.col)
#         if slot_match is None:
#             max_val = 50
#             luck_roll = str(random.randint(min_val, max_val))
#             slot_match = adventure_table.find(luck_roll, in_column=area_match.col)
#         if rep_array is not None:
#             while luck_roll in rep_array:
#                 luck_roll = str(random.randint(min_val, max_val))
#         if th_attempts is not None:
#             th_hits = []
#             for i in range(0, int(th_attempts)):
#                 th_roll = np.random.randint(min_val, max_val, 3)
#                 th_hits += th_roll.tolist()
#                 if int(th_target) in th_roll:
#                     luck_roll = str(th_target)
#                     break
#     ret_string += get_mon(area, luck_roll, adventure_table, ad_notes)
#     if "treasure" in ret_string.lower():
#         treasure_flag = True
#     if extra_players != 0 or bait_mons != 0:
#         extra_mons = bait_mons + extra_players
#         for i in range(0, extra_mons):
#             if i == 3:
#                 time.sleep(60)
#             ret_string += "Extra Encounter {0} of {1} is: ".format(i + 1, extra_mons) + get_mon(area,
#                                                                                                 str(random.randint(
#                                                                                                     min_val,
#                                                                                                     max_val)),
#                                                                                                 adventure_table,
#                                                                                                 ad_notes,
#                                                                                                 treasure_flag) + "\n"
#             if "treasure" in ret_string.lower() and treasure_flag == False:
#                 treasure_flag = True
#     if event is None:
#         event = str(random.randint(1, 20))
#     event_rolled = get_event(area, event, ad_events, ad_event_notes)
#     swarm_addition = ""
#     if "Guardian Encounter" in event_rolled and not guardianFlag:
#         event_rolled = get_event(area, str(random.randint(1, 20)), ad_events, ad_event_notes)
#     if "Major Pokemon Swarm" in event_rolled:
#         for i in range(0, (int(math.ceil(int(tl) / 15)))):
#             swarm_addition += "Swarm Pokemon {0} of {1} is: ".format(i + 1,
#                                                                      (int(math.ceil(int(tl) / 15)))) + get_non_treasure(
#                 area_match.col,
#                 adventure_table,
#                 ad_notes,
#                 min_val,
#                 max_val) + "\n"
#     ret_string += event_rolled + swarm_addition + find_disposition(area)
#     if th_hits is not None:
#         ret_string += "\n\nHere are the treasure hunt rolls: " + ", ".join([str(num) for num in th_hits])
#     return ret_string
#
#
# def roll_harvest_table(area):
#     criteria = re.compile('(?i)^' + area + "$")
#     area_match = harvest.find(criteria, in_row=1)
#     match = harvest.cell(random.randint(2, 11), area_match.col)
#     if match is None:
#         return "This area does not exist. Please try again."
#     ret_string = match.value + "\n"
#     harvest_desc = h_notes.cell((match.row, match.col))
#     if harvest_desc.note is not None:
#         ret_string += "\nDescription: " + harvest_desc.note + "\n"
#     return ret_string
#
#
# def find_disposition(area):
#     criteria = re.compile('(?i)^' + area + "$")
#     area_match = disp_sheet.find(criteria, in_row=1)
#     roll = random.randint(2, 6)
#     match = disp_sheet.cell(roll, area_match.col)
#     if match is None:
#         return "This area does not exist. Please try again"
#     return "\nThe starting disposition of this encounter is " + match.value + "\n"

