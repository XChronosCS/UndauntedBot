import random
import dice
import re
from constants import *

GENDER = ["Male", "Female"]


def nature():
    index = random.randrange(0, len(NATURES))
    return NATURES[index]


def gender():
    index = random.randrange(0, 2)
    return GENDER[index]


def roll_vals(match):
    a, b = match.group(1).split('d')
    ret_array = []
    for i in range(int(a)):
        ret_array.append(str(random.randint(1, 1 * int(b))))
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
