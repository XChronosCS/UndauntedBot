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


@bot.command(name='townevent', aliases=['town'])
async def townevent(ctx):
    result = get_town_event()
    ret_string = "Event Invoked By: " + ctx.author.mention + "\n" + result[0] + "\n" + result[1]
    await ctx.send(ret_string)
    await ctx.message.delete()

@bot.command(name="portal")
async def portal(ctx):
    await ctx.send(roll_dim())


@bot.command(name='uprising')
async def uprising(ctx):
    result = get_uprising_event()
    ret_string = "Event Invoked By: " + ctx.author.mention + "\n" + result[0] + "\n" + result[1]
    await ctx.send(ret_string)
    await ctx.message.delete()


@bot.command(name='ability', aliases=['abil'])
async def ability(ctx, *arg):
    arg_full = ' '.join(arg)
    result = get_ability_data(arg_full)
    ret_string = ''.join(result)
    await ctx.send(ret_string)


@bot.command(name='feature', aliases=['feats'])
async def feature(ctx, *arg):
    arg_full = ' '.join(arg)
    result = get_feature_data(arg_full)
    ret_string = ''.join(result)
    await ctx.send(ret_string)


@bot.command(name='items')
async def items(ctx, *arg):
    arg_full = ' '.join(arg)
    result = get_item_data(arg_full)
    ret_string = ''.join(result)
    await ctx.send(ret_string)

    
@bot.command(name='capa')
async def capa(ctx, *arg):
    arg_full = ' '.join(arg)
    result = get_cap_data(arg_full)
    ret_string = ''.join(result)
    await ctx.send(ret_string)



@bot.command(name='edge')
async def edge(ctx, *arg):
    arg_full = ' '.join(arg)
    result = get_edge_data(arg_full)
    ret_string = ''.join(result)
    await ctx.send(ret_string)


@bot.command(name='move')
async def move(ctx, *arg):
    arg_full = ' '.join(arg)
    result = get_move_data(arg_full)
    ret_string = ''.join(result)
    await ctx.send(ret_string)
    
@bot.command(name='manu')
async def manu(ctx, *arg):
    arg_full = ' '.join(arg)
    result = get_man_data(arg_full)
    ret_string = ''.join(result)
    await ctx.send(ret_string)

@bot.command(name='habitat', aliases=['habit'])
async def habitat(ctx, *arg):
    arg_full = ' '.join(arg)
    result = get_habitat(arg_full)
    await ctx.send(result)
    
@bot.command(name='tfind', aliases=['treasure'])
async def tfind(ctx, *args):
    arg_full = ' '.join(args)
    result = get_treasure_spot(arg_full)
    await ctx.send(result)
    
@bot.command(name='tech')
async def tech(ctx, *arg):
    arg_full = ' '.join(arg)
    result = get_technique(arg_full)
    await ctx.send(result)

@bot.command(name='skill')
async def skill(ctx, *arg):
    arg_full = ' '.join(arg)
    result = get_skill(arg_full)
    await ctx.send(result)

@bot.command(name='order')
async def tech(ctx, *args):
    arg_full = ' '.join(args)
    result = get_order(arg_full)
    await ctx.send(result)

@bot.command(name='mech')
async def mech(ctx):
    channel = ctx.channel
    user = ctx.author
    ops = "Please type out one of the following options: "
    ops += ", ".join(show_mechanics())
    await ctx.send(ops)
    
    def check(m):
        return m.author == user and m.channel == channel and m.content.lower() in (string.lower() for string in show_mechanics())
    
    msg = await bot.wait_for("message", check=check)
    await ctx.send(get_mechanic(msg.content.lower()))


@bot.command(name='keymoves', aliases=['kmoves'])
async def keymoves(ctx, *arg):
    arg_full = ' '.join(arg)
    result = get_keyword_moves(arg_full)
    await ctx.send(result)
    
@bot.command(name='cond')
async def cond(ctx, *arg):
    arg_full = ' '.join(arg)
    result = get_status_data(arg_full)
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


@bot.command(name='pokerandom', aliases=['prand'])
async def pokerandom(ctx):
    ret_string = "You have encountered a wild " + roll_mon() + "!"
    await ctx.send(ret_string)


@bot.command(name='eggrandom', aliases=['erand'])
async def eggrandom(ctx):
    result = roll_egg('Random')
    ret_string = "Your egg hatched into a " + result + "!"
    await ctx.send(ret_string)


@bot.command(name='eggroll', aliases=['eroll'])
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

@bot.command(name='shards')
async def shards(ctx, *args):
    shard_array = ''.join(args).split(',')
    shards = [0, 0, 0, 0, 0, 0]
    for shard in shard_array:
        shards[int(shard) - 1] += 1
    ret_string = "You found:\n{0[0]} Red Shards\n{0[1]} Orange Shards\n{0[2]} Yellow Shards\n{0[3]} Green Shards\n{0[4]} Blue Shards\n{0[5]} Violet Shards".format(shards)
    await ctx.send(ret_string)

@bot.command(name='fossil')
async def fossil(ctx):
    result = fossil_roller()
    ret_string = "You have unearthed a " + result + "!"
    await ctx.send(ret_string)


@bot.command(name='eggmove', aliases=['emove'])
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


@bot.command(name="whenfreya")
async def whenfreya(ctx):
    a_file = open("Documents/days.txt", "r")
    list_of_lines = a_file.readlines()
    num_days = int(list_of_lines[0])
    list_of_lines[0] = str(num_days + random.randint(20, 40))
    a_file = open("Documents/days.txt", "w")
    a_file.writelines(list_of_lines)
    a_file.close()
    ret_string = "Freya comes out in " + str(num_days) + " days."
    await ctx.send(ret_string)


@bot.command(name="whenkostrya")
async def whenkostrya(ctx):
    await ctx.send("After Freya is released. Please use the command !whenfreya to check how close it is to release.")


# Dice Rolling Command
@bot.command(aliases=['droll', 'dr'])
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


@bot.command(name='exploration', aliases=['explo'])
async def exploration(ctx, *arg):
    pl = arg[-1]
    tl = arg[-2]
    list_arg = list(arg)
    post_channel = bot.get_channel(565626984709881886)
    channel = ctx.channel
    user = ctx.author
    extra_players = 0
    bait_mons = 0
    repel_array = []
    skill_used = None
    skill_key = 0
    skill_roll = 0
    force_mon = None
    force_event = None
    luck_roll = 0
    del list_arg[-2:]

    def extra_bait_check(m):
        return user == m.author and m.channel == channel and m.content in ['1', '2', '3']

    def skill_check(m):
        return user == m.author and m.channel == channel and m.content.title() in EXPLO_SKILLS.keys()

    def roll_check(m):
        return user == m.author and m.channel == channel and m.content.isdigit()

    def repel_check(m):
        pattern = re.compile("(\d*, )*")
        return user == m.author and m.channel == channel and bool(re.match(pattern, m.content))

    def f_event_check(m):
        return user == m.author and m.channel == channel and int(m.content) in range(1, 11)

    def f_mon_check(m):
        return user == m.author and m.channel == channel and int(m.content) in range(1, 21)

    def check(m):
        return m.author == user and m.channel == channel and m.content.lower() in ["y", "n"]

    def gen_ed_check(m):
        return m.author == user and m.channel == channel and int(m.content) in range(1, 7)

    area = ' '.join(list_arg)
    note_message = ['']
    # Checking the Skill for later input
    await ctx.send("Which skill did they use for their skill roll? Please enter a valid skill now. Note: For the "
                   "education skills, end the skill name with 'Edu'")
    msg = await bot.wait_for("message", check=skill_check)
    skill_used = msg.content.title()
    # Checking for the Skill roll Value
    await ctx.send("What was the value of the skill roll?")
    msg = await bot.wait_for("message", check=roll_check)
    skill_roll = int(msg.content)
    # Checking for the Luck Roll Value and seeing if Mon was forced
    await ctx.send("Are they forcing a pokemon slot? Respond with y for yes or n for no")
    msg = await bot.wait_for("message", check=check)
    if msg.content.lower() == "y":
        await ctx.send("What slot are they forcing? Please type a number between 1 and 20.")
        msg = await bot.wait_for("message", check=f_mon_check)
        force_mon = msg.content
    else:
        await ctx.send("What was the value of the luck roll?")
        msg = await bot.wait_for("message", check=roll_check)
        luck_roll = int(msg.content)
    await ctx.send("Are they using a repel? Respond with y for yes or n for no")
    msg = await bot.wait_for("message", check=check)
    if msg.content.lower() == "y":
        await ctx.send("Which slots are they repelling? Please type a list of numbers seperated by a comma space(ex. "
                       "15, 3)")
        msg = await bot.wait_for("message", check=repel_check)
        repel_array.append(msg.content.split(", "))
    await ctx.send("Are they forcing an event slot? Respond with y for yes or n for no")
    msg = await bot.wait_for("message", check=check)
    if msg.content.lower() == "y":
        await ctx.send("What slot are they forcing? Please type a number between 1 and 10.")
        msg = await bot.wait_for("message", check=f_event_check)
        force_event = msg.content
    await ctx.send("Is there more than one player in this party? Respond with y for yes or n for no")
    msg = await bot.wait_for("message", check=check)
    if msg.content.lower() == "y":
        await ctx.send("How many extra players? Please type a number between 1 and 3.")
        msg = await bot.wait_for("message", check=extra_bait_check)
        extra_players = int(msg.content)
    await ctx.send("Are they using a bait or bait-like ability? Respond with y for yes or n for no")
    msg = await bot.wait_for("message", check=check)
    if msg.content.lower() == "y":
        await ctx.send("How many successful bait rolls were there? Please type a number between 1 and 3. If they have "
                       "not rolled for bait yet, have them roll it now.")
        msg = await bot.wait_for("message", check=extra_bait_check)
        bait_mons = int(msg.content)
    await ctx.send("Now generating exploration...")
    skill_key = 5 * round(skill_roll / 5)
    if skill_used == "Pokemon Edu" and skill_key >= 20:
        bait_mons += 1
    # print([area, str(skill_roll), luck_roll, tl, pl, repel_array, bait_mons, extra_players, skill_used, skill_key, force_mon, force_event, note_message])
    ret_string = roll_exploration(area, str(skill_roll), luck_roll, tl, pl, repel_array, bait_mons, extra_players, skill_used, skill_key, force_mon, force_event, note_message)
    await ctx.send(ret_string)
    if skill_used == "General Edu" and 25 > skill_key >= 15:
        await ctx.send("You have the option to reroll your luck roll. Would you like to do so? Please enter y for yes "
                       "or n for no")
        msg = await bot.wait_for("message", check=check)
        if msg.content.lower() == "y":
            note_message[0] = ""
            ret_string = roll_exploration(area, str(skill_roll), random.randint(1,20), tl, pl, repel_array, bait_mons, extra_players, skill_used, skill_key, force_mon, force_event, note_message)
            await ctx.send(ret_string)
    if skill_used == "General Edu" and skill_key >= 25:
        await ctx.send("You have several options available to you. Please choose one of the following:"
                       "\nType 1 to reroll this luck roll"
                       "\nType 2 to increase the value of this luck roll by 1"
                       "\nType 3 to increase the value of this luck roll by 2"
                       "\nType 4 to decrease the value of this luck roll by 1"
                       "\nType 5 to decrease the value of this luck roll by 2"
                       "\nType 6 to keep as it.")
        msg = await bot.wait_for("message", check=gen_ed_check)
        op_array = [random.randint(1, 20), luck_roll + 1, luck_roll + 2, luck_roll - 1, luck_roll - 2]
        if int(msg.content) != 6:
            note_message[0] = ""
            ret_string = roll_exploration(area, str(skill_roll), op_array[int(msg.content) - 1], tl, pl, repel_array, bait_mons,
                                          extra_players,
                                          skill_used, skill_key, force_mon, force_event, note_message)
            await ctx.send(ret_string)
    if skill_used == "Occult Edu" and skill_key >= 20:
        print("This command is triggered")
        note_message[0] += roll_occult(area, pl)
    if note_message[0] != "":
        await post_channel.send(ctx.author.mention + "\n**" + area + "**\n" + note_message[0])

        
@bot.command(name='areaevent', aliases=['event'])
async def areaevent(ctx, *arg):
    area = ' '.join(arg)
    ret_string = choose_event(area)
    await ctx.send(ret_string)


@bot.command(name='adventure', aliases=['adven'])
async def adventure(ctx, *arg):
    pl = arg[-1]
    tl = arg[-2]
    list_arg = list(arg)
    del list_arg[-2:]
    area = ' '.join(list_arg)
    channel = ctx.channel
    user = ctx.author
    post_channel = bot.get_channel(565626984709881886)
    status = 0  # 1 means yes treasure hunting, 2 means yes forcing mons, 4 means yes forcing events, and 8 means yes
    # extra players
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
        return user == m.author and m.channel == channel and m.content in ['1', '2', '3', '4', '5', '6', '7', '8', '9']

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
        await ctx.send(
            "What slot are they Treasure Hunting for? Please type one of the following numbers: 1, 10, 20, 30, 40 and 50")
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
    ret_string = user.mention + "\n**" + area + "**\n" + roll_adventure(area, tl, pl, th, target, force_mon,
                                                                        force_event, extra_players)
    await post_channel.send(ret_string)


@bot.command(name='autostat', aliases=['astat'])
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


@bot.command(name='babystat', aliases=['bstat'])
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
    

@bot.command(name='lookup', aliases=['search'])
async def lookup(ctx, *args):
  arg_full = ' '.join(args)
  ret_string = get_data(arg_full)
  await ctx.send(ret_string)


bot.run(TOKEN)
