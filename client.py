# client.py
import os
import string
import dice
import re
import discord
import random
from discord.ext import commands
from dotenv import load_dotenv
from TownEvents import *
from DataGet import *
from PokeRoller import *
from TableRoller import *
from RollingCommands import *
from EncounterRoller import *
from autostatter import *

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
    arg_full = ' '.join(arg)
    result = get_ability_data(arg_full)
    ret_string = ''
    for x in result:
        ret_string += x
    await ctx.send(ret_string)


@bot.command(name='feature')
async def feature(ctx, *arg):
    arg_full = ' '.join(arg)
    result = get_feature_data(arg_full)
    ret_string = ''
    for x in result:
        ret_string += x
    await ctx.send(ret_string)


@bot.command(name='items')
async def items(ctx, *arg):
    arg_full = ' '.join(arg)
    print(arg_full)
    result = get_item_data(arg_full)
    ret_string = ''
    for x in result:
        ret_string += x
    await ctx.send(ret_string)


@bot.command(name='edge')
async def edge(ctx, *arg):
    arg_full = ' '.join(arg)
    result = get_edge_data(arg_full)
    ret_string = ''
    for x in result:
        ret_string += x
    await ctx.send(ret_string)


@bot.command(name='move')
async def move(ctx, *arg):
    arg_full = ' '.join(arg)
    result = get_move_data(arg_full)
    ret_string = ''
    for x in result:
        ret_string += x
    await ctx.send(ret_string)

    
@bot.command(name='habitat')
async def habitat(ctx, *arg):
    arg_full = ' '.join(arg)
    result = get_habitat(arg_full)
    await ctx.send(result)
    

@bot.command(name='keymoves')
async def keymoves(ctx, *arg):
    arg_full = ' '.join(arg)
    result = get_keyword_moves(arg_full)
    await ctx.send(result)
    
    
@bot.command(name='amons')
async def amons(ctx, *arg):
    arg_full = ' '.join(arg)
    result = poke_ability(arg_full)
    await ctx.send(result)


@bot.command(name='lum')
async def lum(ctx, *arg):
    arg_full = ' '.join(arg)
    result = poke_moves(arg_full)
    await ctx.send(result)


@bot.command(name='tm')
async def tm(ctx, *arg):
    arg_full = ' '.join(arg)
    result = poke_tutor(arg_full)
    await ctx.send(result)


@bot.command(name='cmons')
async def cmons(ctx, *arg):
    arg_full = ' '.join(arg)
    result = poke_capability(arg_full)
    await ctx.send(result)


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
    
    
@bot.command(name="muffin")
async def muffin(ctx):
    muf_var = random.randint(1, 5)
    await ctx.send(file=discord.File("Images/muffin_{0}.png".format(muf_var)))


# Dice Rolling Command
@bot.command(aliases=['droll','dr'])
async def diceroll(ctx, *args):
    arg_full = ' '.join(args)
    text_string = ''
    modifier_string = None
    exclude_string = None
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
    if 'E' in dice_string:
        re_array = dice_string.split('E', 1)
        dice_string = re_array[0]
        exclude_string = re_array[1]
    ret_string += ctx.author.mention
    ret_string += roll_calc(dice_string, modifier_string, exclude_string, text_string)
    await ctx.send(ret_string)


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
    ret_string = find_mon(area, roll)[0]
    await ctx.send(ret_string)


@bot.command(name='exploration')
async def exploration(ctx, *arg):
    pl = arg[-1]
    tl = arg[-2]
    skill = arg[-3]
    list_arg = list(arg)
    post_channel = bot.get_channel(565626984709881886)
    del list_arg[-3:]
    area = ' '.join(list_arg)
    note_message = ['']
    ret_string = roll_exploration(area, skill, tl, pl, note_message)
    await ctx.send(ret_string)
    if note_message[0] != "":
        await post_channel.send(ctx.author.mention + "\n**" + area + "**\n" + note_message[0])


@bot.command(name='areaevent')
async def areaevent(ctx, *arg):
    area = ' '.join(arg)
    ret_string = choose_event(area)
    await ctx.send(ret_string)
    
@bot.command(name='adventure')
async def adventure(ctx, *arg):
    pl = arg[-1]
    tl = arg[-2]
    list_arg = list(arg)
    del list_arg[-2:]
    area = ' '.join(list_arg)
    channel = ctx.channel
    user = ctx.author
    post_channel = bot.get_channel(565626984709881886)
    status = 0 # 1 means yes treasure hunting, 2 means yes forcing mons, 4 means yes forcing events, and 8 means yes extra players
    th = None
    target = None
    force_mon = None
    force_event = None
    extra_players = 0
    
    def extra_check(m):
      return user == m.author and m.channel == channel and m.content in ['1', '2', '3']
    
    
    def target_check(m):
      return user == m.author and m.channel == channel and m.content in ['1', '10', '20', '30', '40', '50']
    
    def th_check(m):
      return user == m.author and m.channel == channel and m.content in ['1', '2', '3', '4', '5', '6','7','8','9']
    
    def f_mon_check(m):
      return user == m.author and m.channel == channel and int(m.content) in range(1, 51)
    
    
    def f_event_check(m): 
      return user == m.author and m.channel == channel and int(m.content) in range(1, 21)
    
    def check(m):
      return m.author == user and m.channel == channel and m.content.lower() in ["y", "n"]
    
    await ctx.send("Are they treasure hunting anything? Respond with y for yes or n for no")
    msg = await bot.wait_for("message", check=check)
    if msg.content.lower() == "y":
      await ctx.send("How many times are they treasure hunting? Please type a number between 1 and 9")
      msg = await bot.wait_for("message", check=th_check)
      th = msg.content
      await ctx.send("What slot are they Treasure Hunting for? Please type one of the following numbers: 1, 10, 20, 30, 40 and 50")
      msg = await bot.wait_for("message", check=target_check)
      target = msg.content
    await ctx.send("Are they forcing a pokemon slot or treasure slot? Respond with y for yes or n for no")
    msg = await bot.wait_for("message", check=check)
    if msg.content.lower() == "y":
      await ctx.send("What slot are they forcing? Please type a number between 1 and 50.")
      msg = await bot.wait_for("message", check=f_mon_check)
      force_mon = msg.content
    await ctx.send("Are they forcing an event slot? Respond with y for yes or n for no")
    msg = await bot.wait_for("message", check=check)
    if msg.content.lower() == "y":
      await ctx.send("What slot are they forcing? Please type a number between 1 and 20.")
      msg = await bot.wait_for("message", check=f_event_check)
      force_event = msg.content
    await ctx.send("Is there more than one player in this party? Respond with y for yes or n for no")
    msg = await bot.wait_for("message", check=check)
    if msg.content.lower() == "y":
      await ctx.send("How many extra players? Please type a number between 1 and 3.")
      msg = await bot.wait_for("message", check=extra_check)
      extra_players = int(msg.content)
    await ctx.send("Now generating adventure...")
    ret_string = user.mention + "\n**" + area + "**\n" + roll_adventure(area, tl, pl, th, target, force_mon, force_event, extra_players)
    await post_channel.send(ret_string)

@bot.command(name='autostat')
async def autostat(ctx, *args):
    linkmail = args[-1]
    level = args[-2]
    list_arg = list(args)
    del list_arg[-2:]
    name = ' '.join(list_arg)
    link = None
    email = None
    if '@' in linkmail:
        email = linkmail
    else:
        link = linkmail
    await ctx.send("Now statting automatically... Please wait...")
    ret_string = ctx.author.mention + "\n" + autostatter(name, level, email, link)
    await ctx.send(ret_string)
    
    
@bot.command(name='babystat')
async def babystat(ctx, *args):
    baby = True
    linkmail = args[-1]
    level = args[-2]
    list_arg = list(args)
    del list_arg[-2:]
    name = ' '.join(list_arg)
    link = None
    email = None
    if '@' in linkmail:
        email = linkmail
    else:
        link = linkmail
    await ctx.send("Now statting automatically... Please wait...")
    ret_string = ctx.author.mention + "\n" + autostatter(name, level, email, link, baby)
    await ctx.send(ret_string)
    


bot.run(TOKEN)
