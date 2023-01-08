import random

from CollectData import eggdex, infodex, town_list
from Constants import *
from utilities import *

GENDER = ["Male", "Female"]
reroll = 0


def roll_nature():
    index = random.randrange(0, len(NATURES))
    return NATURES[index]


def roll_gender():
    index = random.randrange(0, 2)
    return GENDER[index]


def roll_details():
    nature = roll_nature()
    gender = roll_gender()
    ability = random.randint(1, 2)
    result_array = [nature, gender, ability]
    return "This pokemon has a {0[0]} nature, is a {0[1]} gender if allowed, and has ability option {0[2]} " \
           "if there are multiple options.".format(result_array)


def roll_flora(tier, amount):
    flora_list = []
    for i in range(int(amount)):
        flora_list.append(random.choice(FLORA[tier]))
    ret_string = "Here are the rolled plants of tier " + tier + ": " + ", ".join(flora_list)
    return ret_string


def roll_calc(dice_string, modifier_string, exclude_string, text_string):
    ret_string = ''
    multiplier = 1
    calc_reroll = 0

    def roll_reroll(match):
        a, b = match.group(1).split('d')
        ret_array = []
        for i in range(int(a)):
            roll = random.randint(1, 1 * int(b))
            if roll == calc_reroll:
                ret_array.append("~~" + str(calc_reroll) + "~~")
                roll = random.choice([i for i in range(1, int(b)) if i not in [calc_reroll]])
            ret_array.append(str(roll))
        sub_string = '[' + ', '.join(ret_array) + ']'
        return sub_string

    if modifier_string is not None:
        multiplier = int(modifier_string)
        ret_string += "\nPerforming " + str(multiplier) + " iterations..."
    if exclude_string is not None:
        calc_reroll = int(exclude_string)
        ret_string += "\nRerolling all " + exclude_string + "'s..."
    for i in range(multiplier):
        roll_string = re.sub("[^\d+\-*\/d]", '', dice_string)
        # turns the XdY rolls into the values being rolled
        rolls = re.sub('(\d+d\d+)', roll_vals, roll_string)
        # Takes the arrays of numbers in string and turns them into the sums       
        if calc_reroll != 0:
            temp_rolls = re.sub('(\d+d\d+)', roll_reroll, roll_string)
            rolls = temp_rolls
        result_string = re.sub('\[.*\]', roll_result, rolls)
        result = eval(result_string)
        ret_string += "\n**" + dice_string + "**\n" + text_string + rolls + " = " + str(result)
        return ret_string


def roll_vals(match):
    a, b = match.group(1).split('d')
    ret_array = []
    for i in range(int(a)):
        roll = random.randint(1, 1 * int(b))
        if roll == reroll:
            ret_array.append("~~" + str(reroll) + "~~")
            roll = random.randint(reroll + 1, 1 * int(b))
        ret_array.append(str(roll))
    ret_string = '[' + ', '.join(ret_array) + ']'
    return ret_string


def roll_result(match):
    ret_val = 0
    arr = match.group(0)
    num_string = ''
    for x in list(arr):
        if x.isnumeric():
            num_string += x
        else:
            if num_string == '':
                ret_val += 0
            else:
                ret_val += int(num_string)
                num_string = ''
    return str(ret_val)


def roll_interest(bank):
    interest_rate = (random.randint(1, 4) + random.randint(1, 4)) / 100
    interest = bank * interest_rate
    if interest > 2500.0:
        interest = 2500.0
    return "Through the power of savings, you have earned $" + str(interest) + ", meaning you" \
                                                                               " now have $" + str(bank + interest)


def roll_deity():
    dice_roll = random.randint(1, 50)
    cash = dice_roll * 100
    stamina = 0
    patron_points = 0
    if dice_roll >= 40:
        stamina = 3
    if dice_roll == 50:
        stamina = 6
        patron_points = 3
    format_string = "You rolled a {dice}, which means...\n You gain ${money}\nYou gain {stam} Stamina\nYou gain {pp} " \
                    "Patron Points"
    return format_string.format(dice=dice_roll, money=cash, stam=stamina, pp=patron_points)


def roll_dim():
    return "You have opened a portal to the " + ULTRA_DIM[random.randrange(0, len(ULTRA_DIM))] + " Dimension!"


ALL_CLASSES = ["Ace Trainer", "Capture Specialist", "Cheerleader", "Commander", "Coordinator", "Hobbyist", "Duelist",
               "Enduring Soul", "Juggler", "Medic", "Rider", "Taskmaster", "Trickster", "Stat Ace", "Style Ace",
               "Type Ace", "Alchemist", "Artificer", "Backpacker", "Chef", "Chronicler", "Fashionista", "Gadgeteer",
               "Hobbyist", "Saboteur", "(Bug) Swarmlord", "(Dark) Shade Caller", "(Dragon) Herald of Pride",
               "(Electric) Spark Master", "(Fairy) Glamour Weaver", "(Fighting) Disciple", "(Fire) Fire Bringer",
               "(Flying) Wind Runner", "(Ghost) Apparition", "(Grass) Druid", "(Ground) Earth Shaker",
               "(Ice) Frost-Touched", "(Normal) Prism", "(Poison) Miasmic", "(Psychic) Psionic", "(Rock) Stone Warrior",
               "(Steel) Steelheart", "(Water) Maelstrom", "Athlete", "Berserker", "Dancer", "Fortress", "Hunter",
               "Marksman", "Martial Artist", "Musician", "Ninja", "Provocateur", "Rogue", "Roughneck", "Samurai",
               "Skirmisher", "Tumbler", "Weapon Master", "Arcanist", "Astral Mage", "Aura Guardian", "Channeler",
               "Chaos Mage", "Chronomancer", "Crimson Mage", "Geomancer", "Hex Mage", "Illusionist", "Oracle",
               "Paladin", "Paragon", "Rune Master", "Sage", "Tempest Mage", "Warper"]
ELEMENTALISTS = ["(Bug) Swarmlord", "(Dark) Shade Caller", "(Dragon) Herald of Pride",
                 "(Electric) Spark Master", "(Fairy) Glamour Weaver", "(Fighting) Disciple", "(Fire) Fire Bringer",
                 "(Flying) Wind Runner", "(Ghost) Apparition", "(Grass) Druid", "(Ground) Earth Shaker",
                 "(Ice) Frost-Touched", "(Normal) Prism", "(Poison) Miasmic", "(Psychic) Psionic",
                 "(Rock) Stone Warrior",
                 "(Steel) Steelheart", "(Water) Maelstrom"]
TYPE_ACE = ["Bug", "Dark", "Dragon", "Electric", "Fairy", "Fighting", "Fire", "Flying", "Ghost", "Grass", "Ground",
            "Ice", "Normal", "Poison", "Psychic", "Rock", "Steel", "Water"]
STYLE_ACE = ["Cool", "Tough", "Beauty", "Smart", "Cute"]
STAT_ACE = ["Attack", "Defense", "Special Attack", "Special Defense", "Speed"]


def random_build():
    classes_temp = ALL_CLASSES.copy()
    elementalists_temp = ELEMENTALISTS.copy()
    style_temp = STYLE_ACE.copy()
    stat_temp = STAT_ACE.copy()
    type_temp = TYPE_ACE.copy()

    def ace_checker(pos_ace):
        if pos_ace == "Type Ace":
            mod = random.choice(type_temp)
            type_temp.remove(mod)
            return pos_ace + " - " + mod
        if pos_ace == "Stat Ace":
            mod = random.choice(stat_temp)
            stat_temp.remove(mod)
            return pos_ace + " - " + mod
        if pos_ace == "Style Ace":
            mod = random.choice(style_temp)
            style_temp.remove(mod)
            return pos_ace + " - " + mod

    class_array = []
    for i in range(4):
        rand_class = random.choice(classes_temp)
        if rand_class == "Type Ace" or rand_class == "Stat Ace" or rand_class == "Style Ace":
            class_ace = ace_checker(rand_class)
            rand_class = class_ace
        elif rand_class in elementalists_temp:
            temp_set = set(classes_temp) ^ set(elementalists_temp)
            classes_temp = list(temp_set)
        else:
            classes_temp.remove(rand_class)
        class_array.append(rand_class)

    return "Your 4 Randomly Chosen Classes are: {0[0]}, {0[1]}, {0[2]} and {0[3]}".format(class_array)


def roll_mon():
    return random.choice(ALLPOKEMON.keys()).title()


def roll_egg(p_type, egg_move=False):
    chosen_type = ""
    if p_type == 'Random':
        chosen_type = TYPES[random.randrange(0, len(TYPES))].title()
    else:
        criteria = re.compile('(?i)' + p_type)
        if any((match := criteria.search(item)) for item in eggdex.keys()):
            chosen_type = match.group[0].title()
        else:
            chosen_type = find_most_similar_string(eggdex.keys(), p_type.title())
    mon_index = random.choice(eggdex[chosen_type])
    mon = eggdex[chosen_type][mon_index]
    ret_string = "Congratulations! Your pokemon egg hatched into a {0}".format(mon[0])
    if egg_move:
        ret_string += " with the egg move {0}".format(random.choice[mon[1]])

    return ret_string + "!"


def chaos_roller(choice_entered):
    choice = choice_entered.title()
    ret_string = None
    array_choice = None
    if choice == "Basic":
        array_choice = BASIC_MAGIC
    elif choice == "Advanced":
        array_choice = ADVANCED_MAGIC
    elif choice == "Fluff":
        array_choice = FLUFF_CHAOS_MAGIC
    elif choice == "Combat":
        array_choice = CHAOS_COMBAT
    elif choice == "Status":
        array_choice = CHAOS_STATUS
    else:
        ret_string = "No chaos could be summoned. Please try again."
        return ret_string
    array_length = len(array_choice)
    index = random.randint(0, array_length)
    ret_string = array_choice[index]['type'] + array_choice[index]['effect']
    return ret_string


def fossil_roller():
    array_length = len(FOSSIL)
    index = random.randrange(0, array_length)
    ret_string = FOSSIL[index]['fossil'] + ", which revives into a(n) " + FOSSIL[index]['poke']
    return ret_string


def roll_town_event():
    name = random.choice(list(infodex["townevents"].keys()))
    effect = infodex["townevents"][name]["Effects"]
    name = "**" + name + "**"
    effect = effect.replace("Martial Modifier", "**Martial Modifier**")
    effect = effect.replace("Cultural Modifier", "**Cultural Modifier**")
    effect = effect.replace("Spiritual Modifier", "**Spiritual Modifier**")
    effect = effect.replace("Communal Modifier", "**Communal Modifier**")
    effect = effect.replace("Industrial  Modifier", "**Industrial Modifier**")
    effect = effect.replace("Mercantile Modifier", "**Mercantile Modifier**")
    effect = effect.replace("Academic Modifier", "**Academic Modifier**")
    return name, effect


def roll_uprising_event():
    name = random.choice(list(infodex["uprisings"].keys()))
    effect = infodex["uprisings"][name]["Effects"]
    name = "**" + name + "**"
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
