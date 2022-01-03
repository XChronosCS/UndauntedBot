# client.py
import os
import string
import dice
import re
import discord
from discord.ext import commands
from dotenv import load_dotenv
from TownEvents import *
from DataGet import *
from PokeRoller import *
from TableRoller import *
from RollingCommands import *
from EncounterRoller import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)

bot = commands.Bot(command_prefix='!')


@bot.command(name='townevent')
async def townevent(ctx):
    result = get_town_event()
    ret_string = "Event Invoked By: " + ctx.author.mention + "\n" + result[0] + "\n" + result[1]
    await ctx.send(ret_string)
    await ctx.message.delete()


@bot.command(name='uprising')
async def uprising(ctx):
    result = get_uprising_event()
    ret_string = "Event Invoked By: " + ctx.author.mention + "\n" + result[0] + "\n" + result[1]
    await ctx.send(ret_string)
    await ctx.message.delete()


@bot.command(name='ability')
async def ability(ctx, *arg):
    arg_full = string.capwords(' '.join(arg).lower())
    result = get_ability_data(arg_full)
    ret_string = ''
    for x in result:
        ret_string += x
    await ctx.send(ret_string)


@bot.command(name='feature')
async def feature(ctx, *arg):
    arg_full = string.capwords(' '.join(arg).lower())
    result = get_feature_data(arg_full)
    ret_string = ''
    for x in result:
        ret_string += x
    await ctx.send(ret_string)


@bot.command(name='items')
async def items(ctx, *arg):
    arg_full = string.capwords(' '.join(arg).lower())
    print(arg_full)
    result = get_item_data(arg_full)
    ret_string = ''
    for x in result:
        ret_string += x
    await ctx.send(ret_string)


@bot.command(name='edge')
async def edge(ctx, *arg):
    arg_full = string.capwords(' '.join(arg).lower())
    result = get_edge_data(arg_full)
    ret_string = ''
    for x in result:
        ret_string += x
    await ctx.send(ret_string)


@bot.command(name='move')
async def move(ctx, *arg):
    arg_full = string.capwords(' '.join(arg).lower())
    result = get_move_data(arg_full)
    ret_string = ''
    for x in result:
        ret_string += x
    await ctx.send(ret_string)


@bot.command(name='pokerandom')
async def pokerandom(ctx):
    ret_string = "You have encountered a wild " + roll_mon() + "!"
    await ctx.send(ret_string)


@bot.command(name='eggrandom')
async def eggrandom(ctx):
    result = roll_egg('Random')
    ret_string = "Your egg hatched into a " + result + "!"
    await ctx.send(ret_string)


@bot.command(name='eggroll')
async def eggroll(ctx, *arg):
    arg_full = string.capwords(' '.join(arg).lower())
    result = roll_egg(arg_full)
    ret_string = "Your egg hatched into a " + result + "!"
    await ctx.send(ret_string)


@bot.command(name='chaos')
async def chaos(ctx, *arg):
    arg_full = string.capwords(' '.join(arg).lower())
    entry_string = "You summon the powers of chaos..."
    result = chaos_roller(arg_full)
    await ctx.send(entry_string)
    await ctx.send(result)


@bot.command(name='fossil')
async def fossil(ctx):
    result = fossil_roller()
    ret_string = "You have unearthed a " + result + "!"
    await ctx.send(ret_string)


@bot.command(name="eggmove")
async def eggmove(ctx, *arg):
    arg_full = string.capwords(' '.join(arg).lower())
    result = roll_egg_move(arg_full)
    ret_string = "Your egg hatched into a " + result + "!"
    await ctx.send(ret_string)


@bot.command(name='erm')
async def eggrandom(ctx):
    result = roll_egg_move('Random')
    ret_string = "Your egg hatched into a " + result + "!"
    await ctx.send(ret_string)


# command to post the WoolooTurbo emote
@bot.command(name="turbo")
async def turbo(ctx):
    emote = "<a:WoolooTurbo:701937147862843412>"
    await ctx.send(emote)
    await ctx.message.delete()


# Dice Rolling Command
@bot.command(aliases=['droll'])
async def diceroll(ctx, *args):
    arg_full = ' '.join(args)
    text_string = ''
    modifier_string = None
    multiplier = 1
    dice_string = None
    ret_string = ''
    # reroll_value = None
    if '#' in arg_full:
        args_array = arg_full.split('#', 1)
        dice_string = args_array[0]
        text_string = '**' + args_array[1] + ":** "
    else:
        text_string = '**Roll:** '
        dice_string = arg_full
    if 'R' in dice_string:
        mod_array = dice_string.split('R', 1)
        dice_string = mod_array[0]
        modifier_string = mod_array[1]
    ret_string += ctx.author.mention
    if modifier_string is not None:
        multiplier = int(modifier_string)
        ret_string += "\nPerforming " + str(multiplier) + " iterations..."
    for i in range(multiplier):
        roll_string = re.sub("[^\d+\-*\/d]", '', dice_string)
        # turns the XdY rolls into the values being rolled
        rolls = re.sub('(\d+d\d+)', roll_vals, roll_string)
        # Takes the arrays of numbers in string and turns them into the sums
        result_string = re.sub('\[.*\]', roll_result, rolls)
        result = eval(result_string)
        ret_string += "\n**" + dice_string + "**\n" + text_string + rolls + " = " + str(result)
    await ctx.send(ret_string)
    await ctx.message.delete()


@bot.command(name='details')
async def details(ctx):
    await ctx.send(roll_details())


@bot.command(name='finance')
async def finance(ctx, arg):
    try:
        sum_total = RollingCommands.roll_interest(int(arg))
        await ctx.send(sum_total)
    except TypeError:
        await ctx.send("This is not a valid amount of money. Please try again.")


@bot.command(name='offerings')
async def offerings(ctx):
    await ctx.send(roll_deity())


@bot.command(name='encounter')
async def encounter(ctx, *arg):
    roll = arg[-1]
    list_arg = list(arg)
    del list_arg[-1:]
    area = ' '.join(list_arg)
    ret_string = find_mon(area, roll)
    await ctx.send(ret_string)


@bot.command(name='exploration')
async def exploration(ctx, *arg):
    pl = arg[-1]
    tl = arg[-2]
    skill = arg[-3]
    list_arg = list(arg)
    del list_arg[-3:]
    area = ' '.join(list_arg)
    note_message = ['']
    ret_string = roll_exploration(area, skill, tl, pl, note_message)
    await ctx.send(ret_string)
    if note_message[0] != "":
        await ctx.author.send(note_message[0])


@bot.command(name='areaevent')
async def areaevent(ctx, *arg):
    area = ' '.join(arg)
    ret_string = choose_event(area)
    await ctx.send(ret_string)


bot.run(TOKEN)
