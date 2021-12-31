# client.py
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from TownEvents import *
from DataGet import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)

bot = commands.Bot(command_prefix='!')


@bot.command(name='towneventtest')
async def towneventtest(ctx):
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


bot.run(TOKEN)
