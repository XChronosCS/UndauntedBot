# client.py
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from TownEvents import *
from DataGet import *
from PokeRoller import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)

bot = commands.Bot(command_prefix='!')


@bot.command(name='townevent')
async def townevent(ctx):
    result = get_town_event()
    await ctx.send(result[0])
    await ctx.send(result[1])


@bot.command(name='ability')
async def ability(ctx, *arg):
    arg_full = ' '.join(arg).lower().title()
    result = get_ability_data(arg_full)
    for x in result:
        await ctx.send(x)


@bot.command(name='feature')
async def feature(ctx, *arg):
    arg_full = ' '.join(arg).lower().title()
    result = get_feature_data(arg_full)
    for x in result:
        await ctx.send(x)


@bot.command(name='items')
async def items(ctx, *arg):
    arg_full = ' '.join(arg).lower().title()
    result = get_item_data(arg_full)
    for x in result:
        await ctx.send(x)


@bot.command(name='pokerandom')
async def pokerandom(ctx):
    ret_string = "You have encountered a wild " + roll_mon() + "!"
    await ctx.send(ret_string)


@bot.command(name='eggroll')
async def eggroll(ctx, *arg):
    arg_full = ' '.join(arg).lower().title()
    result = roll_egg(arg_full)
    ret_string = "Your egg hatched into a " + result + "!"
    await ctx.send(ret_string)


@bot.command(name='edge')
async def edge(ctx, *arg):
    arg_full = ' '.join(arg).lower().title()
    result = get_edge_data(arg_full)
    for x in result:
        await ctx.send(x)


bot.run(TOKEN)
