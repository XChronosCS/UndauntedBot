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
