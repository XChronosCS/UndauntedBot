import random
import dice
import re
from constants import *

GENDER = ["Male", "Female"]
reroll = 0


def nature():
    index = random.randrange(0, len(NATURES))
    return NATURES[index]


def gender():
    index = random.randrange(0, 2)
    return GENDER[index]
  
def roll_flora(tier, amount):
    berries_list = []
    for i in range(int(amount)):
        berries_list.append(random.choice(BERRIES[tier]))
    ret_string = "Here are the rolled plants of tier " + tier + ": " + ", ".join(berries_list)
    return ret_string


def roll_calc(dice_string, modifier_string, exclude_string, text_string):
    ret_string = ''
    multiplier = 1
    reroll = 0

    def roll_reroll(match):
        a, b = match.group(1).split('d')
        ret_array = []
        for i in range(int(a)):
            roll = random.randint(1, 1 * int(b))
            if roll == reroll:
                ret_array.append("~~" + str(reroll) + "~~")
                roll = random.choice([i for i in range(1, int(b)) if i not in [reroll]])
            ret_array.append(str(roll))
        ret_string = '[' + ', '.join(ret_array) + ']'
        return ret_string

    if modifier_string is not None:
        multiplier = int(modifier_string)
        ret_string += "\nPerforming " + str(multiplier) + " iterations..."
    if exclude_string is not None:
        reroll = int(exclude_string)
        ret_string += "\nRerolling all " + exclude_string + "'s..."
    for i in range(multiplier):
        roll_string = re.sub("[^\d+\-*\/d]", '', dice_string)
        # turns the XdY rolls into the values being rolled
        rolls = re.sub('(\d+d\d+)', roll_vals, roll_string)
        # Takes the arrays of numbers in string and turns them into the sums       
        if reroll != 0:
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
        ret_array.append(str(roll))
    ret_string = '[' + ', '.join(ret_array) + ']'
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
               "(Ice) Frost-Touched", "(Normal) Prism", "(Poison) Miasmic", "(Psychic) Psionic", "(Rock) Stone Warrior",
               "(Steel) Steelheart", "(Water) Maelstrom"]
TYPE_ACE = ["Bug", "Dark", "Dragon", "Electric", "Fairy", "Fighting", "Fire", "Flying", "Ghost", "Grass", "Ground", "Ice", "Normal", "Poison", "Psychic", "Rock", "Steel", "Water"]
STYLE_ACE = ["Cool","Tough","Beauty","Smart","Cute"]
STAT_ACE = ["Attack","Defense","Special Attack","Special Defense", "Speed"]


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


def quaglatin_gen(sentence):
    words = sentence.lower().split()

    for i, word in enumerate(words):
        if word[0] in 'aeiou':
            words[i] = words[i] + "uag"
        else:
            '''
            else get vowel position and postfix all the consonants 
            present before that vowel to the end of the word along with "ay"
            '''
            has_vowel = False

            for j, letter in enumerate(word):
                if letter in 'aeiou':
                    words[i] = word[j:] + word[:j] + "uag"
                    has_vowel = True
                    break

            if not has_vowel:
                words[i] = words[i] + "uag"

    quag_latin = ' '.join(words)
    return quag_latin



