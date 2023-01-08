# client.py
import string
from datetime import datetime

from discord.ext import commands
from dotenv import load_dotenv
from pytz import timezone

from Autostatter import *
from DataGet import *
from RollingCommands import *
from UIElements import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', case_insensitive=True, intents=intents)
UNDAUNTED_GUILD_ID = discord.Object(id = 712378096229023825)

# LEGACY COMMANDS FROM PORYBOT 1.0

@bot.command(name='ability', aliases=['abil'])
async def ability(ctx, *arg):
    arg_full = ' '.join(arg)
    result = get_ability_data(arg_full)
    ret_string = ''.join(result)
    (await ctx.send(ret_string))


#
# @bot.command(name='adfull')
# async def adfull(ctx, *arg):
#     id_var = 942329291549589544
#     pl = arg[(- 1)]
#     tl = arg[(- 2)]
#     list_arg = list(arg)
#     del list_arg[(- 2):]
#     area = ' '.join(list_arg)
#     channel = ctx.channel
#     user = ctx.author
#     status = 0
#     th = None
#     target = None
#     extra_players = 0
#     bait_mons = 0
#     rep_array = None
#     luck_roll = None
#     event = None
#
#     def extra_bait_check(m):
#         return ((user == m.author) and (m.channel == channel) and (m.content in ['1', '2', '3']))
#
#     def repel_check(m):
#         pattern = re.compile('(\\d*, )*')
#         return ((user == m.author) and (m.channel == channel) and bool(re.match(pattern, m.content)))
#
#     def f_event_check(m):
#         return ((user == m.author) and (m.channel == channel) and (int(m.content) in range(1, 21)))
#
#     def th_check(m):
#         return ((user == m.author) and (m.channel == channel) and (int(m.content) in range(1, 4)))
#
#     def f_mon_check(m):
#         return ((user == m.author) and (m.channel == channel) and (int(m.content) in range(1, 101)))
#
#     def check(m):
#         return (m.author == user) and (m.channel == channel) and (m.content.lower() in ['y', 'n'])
#
#     sent = (await ctx.send('Are they treasure hunting anything? Respond with y for yes or n for no'))
#     msg = (await bot.wait_for('message', check=check))
#     if (msg.content.lower() == 'y'):
#         (await sent.delete())
#         (await msg.delete())
#         sent = (await ctx.send('How many times are they treasure hunting? Please type a number between 1 and 3'))
#         msg = (await bot.wait_for('message', check=th_check))
#         th = msg.content
#         (await sent.delete())
#         (await msg.delete())
#         sent = (await ctx.send(
#             'What slot are they Treasure Hunting for? Please type the number slot of the thing they want to encounter.'))
#         msg = (await bot.wait_for('message', check=f_mon_check))
#         target = msg.content
#     (await sent.delete())
#     (await msg.delete())
#     sent = (await ctx.send('Are they forcing a pokemon slot? Respond with y for yes or n for no'))
#     msg = (await bot.wait_for('message', check=check))
#     if (msg.content.lower() == 'y'):
#         (await sent.delete())
#         (await msg.delete())
#         sent = (await ctx.send('What slot are they forcing? Please type the number of the slot.'))
#         msg = (await bot.wait_for('message', check=f_mon_check))
#         luck_roll = msg.content
#     (await sent.delete())
#     (await msg.delete())
#     sent = (await ctx.send('Are they using a repel? Respond with y for yes or n for no'))
#     msg = (await bot.wait_for('message', check=check))
#     if (msg.content.lower() == 'y'):
#         (await sent.delete())
#         (await msg.delete())
#         sent = (await ctx.send(
#             'Which slots are they repelling? Please type a list of numbers seperated by a comma space(ex. 15, 3)'))
#         msg = (await bot.wait_for('message', check=repel_check))
#         rep_array.append(msg.content.split(', '))
#     (await sent.delete())
#     (await msg.delete())
#     sent = (await ctx.send('Are they forcing an event slot? Respond with y for yes or n for no'))
#     msg = (await bot.wait_for('message', check=check))
#     if (msg.content.lower() == 'y'):
#         (await sent.delete())
#         (await msg.delete())
#         sent = (await ctx.send('What slot are they forcing? Please type a number between 1 and 20.'))
#         msg = (await bot.wait_for('message', check=f_event_check))
#         event = msg.content
#     (await sent.delete())
#     (await msg.delete())
#     sent = (await ctx.send('Is there more than one player in this party? Respond with y for yes or n for no'))
#     msg = (await bot.wait_for('message', check=check))
#     if (msg.content.lower() == 'y'):
#         (await sent.delete())
#         (await msg.delete())
#         sent = (await ctx.send('How many extra players? Please type a number between 1 and 3.'))
#         msg = (await bot.wait_for('message', check=extra_bait_check))
#         extra_players = int(msg.content)
#     (await sent.delete())
#     (await msg.delete())
#     sent = (await ctx.send('Are they using a bait or bait-like ability? Respond with y for yes or n for no'))
#     msg = (await bot.wait_for('message', check=check))
#     if (msg.content.lower() == 'y'):
#         (await sent.delete())
#         (await msg.delete())
#         sent = (await ctx.send(
#             'How many successful bait rolls were there? Please type a number between 1 and 3. If they have not rolled for bait yet, have them roll it now.'))
#         msg = (await bot.wait_for('message', check=extra_bait_check))
#         bait_mons = int(msg.content)
#     (await sent.delete())
#     (await msg.delete())
#     (await ctx.send('Now generating adventure...'))
#     if ((bait_mons + extra_players) >= 4):
#         (await ctx.send(
#             'NOTICE: Due to the limitations of Google Sheets, this command will need an additional minute of operation to refresh sheet requests. Please be patient.'))
#     ret_string = ((((user.mention + '\n**') + area) + '**\n') + roll_hidden_adventure(area, tl, pl, luck_roll, event,
#                                                                                       rep_array, bait_mons,
#                                                                                       extra_players, th, target))
#     ret_string += (('\n' + f'<@&') + '{0}>'.format(id_var))
#     if (len(ret_string) > 2000):
#         g_array = segment_text(ret_string)
#         for msg in g_array:
#             (await ctx.send(msg))
#     else:
#         (await ctx.send(ret_string))
#
#
# @bot.command(name='adinfo')
# @commands.guild_only()
# async def adinfo(ctx, *arg):
#     id_var = 942329291549589544
#     event_slot = arg[(- 1)]
#     poke_slot = arg[(- 2)]
#     list_arg = list(arg)
#     del list_arg[(- 2):]
#     area = ' '.join(list_arg)
#     ret_string = get_hidden_slot_adventure(area, poke_slot)
#     ret_string += get_hidden_event_adventure(area, event_slot)
#     ret_string += (('\n' + f'<@&') + '{0}>'.format(id_var))
#     if (len(ret_string) > 2000):
#         g_array = segment_text(ret_string)
#         for msg in g_array:
#             (await ctx.send(msg))
#     else:
#         (await ctx.send(ret_string))
#
#
# @bot.command(name='admon')
# @commands.guild_only()
# async def admon(ctx, *arg):
#     id_var = 942329291549589544
#     poke_slot = arg[(- 1)]
#     list_arg = list(arg)
#     del list_arg[(- 1):]
#     area = ' '.join(list_arg)
#     ret_string = get_hidden_slot_adventure(area, poke_slot)
#     ret_string += (('\n' + f'<@&') + '{0}>'.format(id_var))
#     if (len(ret_string) > 2000):
#         g_array = segment_text(ret_string)
#         for msg in g_array:
#             (await ctx.send(msg))
#     else:
#         (await ctx.send(ret_string))
#
#
# @bot.command(name='adventure', aliases=['adven'])
# async def adventure(ctx, *arg):
#     pl = arg[(- 1)]
#     tl = arg[(- 2)]
#     list_arg = list(arg)
#     del list_arg[(- 2):]
#     area = ' '.join(list_arg)
#     channel = ctx.channel
#     user = ctx.author
#     status = 0
#     th = None
#     target = None
#     extra_players = 0
#     bait_mons = 0
#     rep_array = None
#     luck_roll = None
#     event = None
#
#     def extra_bait_check(m):
#         return ((user == m.author) and (m.channel == channel) and (m.content in ['1', '2', '3']))
#
#     def repel_check(m):
#         pattern = re.compile('(\\d*, )*')
#         return ((user == m.author) and (m.channel == channel) and bool(re.match(pattern, m.content)))
#
#     def f_event_check(m):
#         return ((user == m.author) and (m.channel == channel) and (int(m.content) in range(1, 21)))
#
#     def th_check(m):
#         return ((user == m.author) and (m.channel == channel) and (int(m.content) in range(1, 10)))
#
#     def f_mon_check(m):
#         return ((user == m.author) and (m.channel == channel) and (int(m.content) in range(1, 101)))
#
#     def check(m):
#         return ((m.author == user) and (m.channel == channel) and (m.content.lower() in ['y', 'n']))
#
#     sent = (await ctx.send('Are they treasure hunting anything? Respond with y for yes or n for no'))
#     msg = (await bot.wait_for('message', check=check))
#     if (msg.content.lower() == 'y'):
#         (await sent.delete())
#         (await msg.delete())
#         sent = (await ctx.send('How many times are they treasure hunting? Please type a number between 1 and 9'))
#         msg = (await bot.wait_for('message', check=th_check))
#         th = msg.content
#         (await sent.delete())
#         (await msg.delete())
#         sent = (await ctx.send(
#             'What slot are they Treasure Hunting for? Please type the number slot of the thing they want to encounter.'))
#         msg = (await bot.wait_for('message', check=f_mon_check))
#         target = msg.content
#     (await sent.delete())
#     (await msg.delete())
#     sent = (await ctx.send('Are they forcing a pokemon slot? Respond with y for yes or n for no'))
#     msg = (await bot.wait_for('message', check=check))
#     if (msg.content.lower() == 'y'):
#         (await sent.delete())
#         (await msg.delete())
#         sent = (await ctx.send('What slot are they forcing? Please type the number of the slot.'))
#         msg = (await bot.wait_for('message', check=f_mon_check))
#         luck_roll = msg.content
#     (await sent.delete())
#     (await msg.delete())
#     sent = (await ctx.send('Are they using a repel? Respond with y for yes or n for no'))
#     msg = (await bot.wait_for('message', check=check))
#     if (msg.content.lower() == 'y'):
#         (await sent.delete())
#         (await msg.delete())
#         sent = (await ctx.send(
#             'Which slots are they repelling? Please type a list of numbers seperated by a comma space(ex. 15, 3)'))
#         msg = (await bot.wait_for('message', check=repel_check))
#         rep_array.append(msg.content.split(', '))
#     (await sent.delete())
#     (await msg.delete())
#     sent = (await ctx.send('Are they forcing an event slot? Respond with y for yes or n for no'))
#     msg = (await bot.wait_for('message', check=check))
#     if (msg.content.lower() == 'y'):
#         (await sent.delete())
#         (await msg.delete())
#         sent = (await ctx.send('What slot are they forcing? Please type a number between 1 and 20.'))
#         msg = (await bot.wait_for('message', check=f_event_check))
#         event = msg.content
#     (await sent.delete())
#     (await msg.delete())
#     sent = (await ctx.send('Is there more than one player in this party? Respond with y for yes or n for no'))
#     msg = (await bot.wait_for('message', check=check))
#     if (msg.content.lower() == 'y'):
#         (await sent.delete())
#         (await msg.delete())
#         sent = (await ctx.send('How many extra players? Please type a number between 1 and 3.'))
#         msg = (await bot.wait_for('message', check=extra_bait_check))
#         extra_players = int(msg.content)
#     (await sent.delete())
#     (await msg.delete())
#     sent = (await ctx.send('Are they using a bait or bait-like ability? Respond with y for yes or n for no'))
#     msg = (await bot.wait_for('message', check=check))
#     if (msg.content.lower() == 'y'):
#         (await sent.delete())
#         (await msg.delete())
#         sent = (await ctx.send(
#             'How many successful bait rolls were there? Please type a number between 1 and 3. If they have not rolled for bait yet, have them roll it now.'))
#         msg = (await bot.wait_for('message', check=extra_bait_check))
#         bait_mons = int(msg.content)
#     (await sent.delete())
#     (await msg.delete())
#     (await ctx.send('Now generating adventure...'))
#     if ((bait_mons + extra_players) >= 4):
#         (await ctx.send(
#             'NOTICE: Due to the limitations of Google Sheets, this command will need an additional minute of operation to refresh sheet requests. Please be patient.'))
#     ret_string = (
#             (((user.mention + '\n**') + area) + '**\n') + roll_adventure(area, tl, pl, luck_roll, event, rep_array,
#                                                                          bait_mons, extra_players, th, target))
#     if (len(ret_string) > 2000):
#         g_array = segment_text(ret_string)
#         for msg in g_array:
#             (await ctx.send(msg))
#     else:
#         (await ctx.send(ret_string))
#

@bot.command(name='amons')
async def amons(ctx, *arg):
    arg_full = ' '.join(arg)
    result = poke_ability(arg_full)
    if len(result) >= 2000:
        m_array = segment_list(result)
        for msg in m_array:
            (await ctx.send(msg))
    else:
        (await ctx.send(result))


@bot.command(name='arcana')
async def arcana(ctx, *args):
    arg_full = ' '.join(args)
    ret_array = get_arcana_edges(arg_full)
    (await ctx.author.send('**Here are the following arcana edges you qualify for through that patron:**'))
    for i in ret_array:
        (await ctx.author.send(i))


@bot.command(name='autostat', aliases=['astat'])
async def autostat(ctx, *args):
    link = args[(- 1)]
    level = args[(- 2)]
    list_arg = list(args)
    del list_arg[(- 2):]
    name = ' '.join(list_arg)
    await ctx.send('Now statting automatically... Please wait...')
    ret_string = autostatter(name, level, link)
    await ctx.send(ret_string)


# @bot.command(name='babystat', aliases=['bstat'])
# async def babystat(ctx, *args):
#     baby = True
#     linkmail = args[(- 1)]
#     level = args[(- 2)]
#     list_arg = list(args)
#     del list_arg[(- 2):]
#     name = ' '.join(list_arg)
#     link = None
#     email = None
#     if ('@' in linkmail):
#         email = linkmail
#     else:
#         link = linkmail
#     (await ctx.send('Now statting automatically... Please wait...'))
#     ret_string = ((ctx.author.mention + '\n') + autostatter(name, level, email, link, baby))
#     (await ctx.send(ret_string))


'''
@bot.command(name='beans')
async def beans(ctx):
    (await ctx.send(get_beans()))
'''


@bot.command(name='capa')
async def capa(ctx, *arg):
    arg_full = ' '.join(arg)
    result = get_cap_data(arg_full)
    ret_string = ''.join(result)
    (await ctx.send(ret_string))


@bot.command(name='chaos')
async def chaos(ctx, *arg):
    arg_full = string.capwords(' '.join(arg).lower())
    entry_string = 'You summon the powers of chaos...'
    result = chaos_roller(arg_full)
    (await ctx.send(entry_string))
    (await ctx.send(result))


@bot.command(name='cmons')
async def cmons(ctx, *arg):
    arg_full = ' '.join(arg)
    result = poke_capability(arg_full)
    if (len(result) > 2000):
        m_array = segment_list(result)
        for msg in m_array:
            (await ctx.send(msg))
    else:
        (await ctx.send(result))


@bot.command(name='compendium')
async def compendium(ctx, *arg):
    name = ' '.join(arg).lower()
    pages = get_legend_entry(name)
    if pages:
        for page in pages:
            (await ctx.author.send(file=discord.File(page)))
            os.remove(page)
    else:
        (await ctx.send(
            'There is no legend with this name / topic with this name in the compendium. Please try again.'))


@bot.command(name='cond')
async def cond(ctx, *arg):
    arg_full = ' '.join(arg)
    result = get_status_data(arg_full)
    (await ctx.send(result))


@bot.command(name='cookie')
async def cookie(ctx, person: discord.Member = None):
    if (person is None):
        person = ctx.author
    msg = (((str(ctx.author.name) + ' has given ') + person.mention) + ' a cookie!')
    embed = discord.Embed(title='Cookie Given!', description=msg, color=16057729)
    (await ctx.send(embed=embed))


@bot.command(name='details')
async def details(ctx):
     (await ctx.send(roll_details()))


@bot.command(aliases=['droll', 'dr'])
async def diceroll(ctx, *args):
    arg_full = ' '.join(args)
    text_string = ''
    modifier_string = None
    exclude_string = None
    dice_string = None
    ret_string = ''
    if ('#' in arg_full):
        args_array = arg_full.split('#', 1)
        dice_string = args_array[0]
        text_string = (('**' + args_array[1]) + ':** ')
    else:
        text_string = '**Roll:** '
        dice_string = arg_full
    if ('R' in dice_string):
        mod_array = dice_string.split('R', 1)
        dice_string = mod_array[0]
        modifier_string = mod_array[1]
    if ('E' in dice_string):
        re_array = dice_string.split('E', 1)
        dice_string = re_array[0]
        exclude_string = re_array[1]
    ret_string += ctx.author.mention
    ret_string += roll_calc(dice_string, modifier_string, exclude_string, text_string)
    (await ctx.send(ret_string))


@bot.command(name='edge')
async def edge(ctx, *arg):
    arg_full = ' '.join(arg)
    result = get_edge_data(arg_full)
    ret_string = ''.join(result)
    (await ctx.send(ret_string))



@bot.command(name='eggmove', aliases=['emove'])
async def eggmove(ctx, *arg):
    arg_full = string.capwords(' '.join(arg).lower())
    result = roll_egg(arg_full, True)
    ret_string = result
    (await ctx.send(ret_string))


@bot.command(name='eggrandom', aliases=['erand'])
async def eggrandom(ctx):
    result = roll_egg('Random')
    ret_string = result
    (await ctx.send(ret_string))


@bot.command(name='erm')
async def erm(ctx):
    result = roll_egg('Random', True)
    ret_string = result
    (await ctx.send(ret_string))


@bot.command(name='eggroll', aliases=['eroll'])
async def eggroll(ctx, *arg):
    arg_full = string.capwords(' '.join(arg).lower())
    result = roll_egg(arg_full)
    ret_string = result
    (await ctx.send(ret_string))


"""
@bot.command(name='exploration', aliases=['explo'])
async def exploration(ctx, *arg):
    pl = arg[(- 1)]
    tl = int(arg[(- 2)])
    list_arg = list(arg)
    channel = ctx.channel
    user = ctx.author
    extra_players = 0
    bait_mons = 0
    repel_array = []
    luck_roll = None
    event = None
    del list_arg[(- 2):]

    def extra_bait_check(m):
        return ((user == m.author) and (m.channel == channel) and (m.content in ['1', '2', '3']))

    def repel_check(m):
        pattern = re.compile('(\\d*, )*')
        return ((user == m.author) and (m.channel == channel) and bool(re.match(pattern, m.content)))

    def f_event_check(m):
        return ((user == m.author) and (m.channel == channel) and (int(m.content) in range(1, 11)))

    def skill_level_check(m):
        return ((user == m.author) and (m.channel == channel) and (int(m.content) in range(1, 9)))

    def f_mon_check(m):
        return ((user == m.author) and (m.channel == channel) and (int(m.content) in range(1, 21)))

    def check(m):
        return ((m.author == user) and (m.channel == channel) and (m.content.lower() in ['y', 'n']))

    def intent_check(m):
        return ((m.author == user) and (m.channel == channel) and (m.content.lower() in ['h', 's', 'w', 't', 'n']))

    area = ' '.join(list_arg)
    sent = (await ctx.send(
        "What is the intent of the exploration? Please type 'H' if Hunting, 'S' if Scavenging, 'W' if Wandering, 'T' if Training, or 'N' if No Intent"))
    msg = (await bot.wait_for('message', check=intent_check))
    intent = msg.content.lower()
    (await sent.delete())
    (await msg.delete())
    sent = (await ctx.send('Are they forcing a pokemon slot? Respond with y for yes or n for no'))
    msg = (await bot.wait_for('message', check=check))
    if (msg.content.lower() == 'y'):
        (await sent.delete())
        (await msg.delete())
        sent = (await ctx.send('What slot are they forcing? Please type the number of the slot.'))
        msg = (await bot.wait_for('message', check=f_mon_check))
        luck_roll = msg.content
    (await sent.delete())
    (await msg.delete())
    sent = (await ctx.send('Are they using a repel? Respond with y for yes or n for no'))
    msg = (await bot.wait_for('message', check=check))
    if (msg.content.lower() == 'y'):
        (await sent.delete())
        (await msg.delete())
        sent = (await ctx.send(
            'Which slots are they repelling? Please type a list of numbers seperated by a comma space(ex. 15, 3)'))
        msg = (await bot.wait_for('message', check=repel_check))
        repel_array.append(msg.content.split(', '))
    (await sent.delete())
    (await msg.delete())
    sent = (await ctx.send('Are they forcing an event slot? Respond with y for yes or n for no'))
    msg = (await bot.wait_for('message', check=check))
    if (msg.content.lower() == 'y'):
        (await sent.delete())
        (await msg.delete())
        sent = (await ctx.send('What slot are they forcing? Please type a number between 1 and 10.'))
        msg = (await bot.wait_for('message', check=f_event_check))
        event = msg.content
    (await sent.delete())
    (await msg.delete())
    sent = (await ctx.send('Is there more than one player in this party? Respond with y for yes or n for no'))
    msg = (await bot.wait_for('message', check=check))
    if (msg.content.lower() == 'y'):
        (await sent.delete())
        (await msg.delete())
        sent = (await ctx.send('How many extra players? Please type a number between 1 and 3.'))
        msg = (await bot.wait_for('message', check=extra_bait_check))
        extra_players = int(msg.content)
    (await sent.delete())
    (await msg.delete())
    sent = (await ctx.send('Are they using a bait or bait-like ability? Respond with y for yes or n for no'))
    msg = (await bot.wait_for('message', check=check))
    if (msg.content.lower() == 'y'):
        (await sent.delete())
        (await msg.delete())
        sent = (await ctx.send(
            'How many successful bait rolls were there? Please type a number between 1 and 3. If they have not rolled for bait yet, have them roll it now.'))
        msg = (await bot.wait_for('message', check=extra_bait_check))
        bait_mons = int(msg.content)
    (await sent.delete())
    (await msg.delete())
    if (intent == 't'):
        extra_players += (1 if (extra_players < 3) else 2)
    (await ctx.send('Now generating exploration...'))
    ret_string = roll_exploration(area, tl, pl, luck_roll, event, repel_array, bait_mons, extra_players)
    if (intent == 'h'):
        sent = (await ctx.send('Please type the name of the hunted pokemon now. Make sure it is spelled correctly.'))
        temp = (await bot.wait_for('message'))
        target = temp.content
        (await sent.delete())
        (await temp.delete())
        sent = (await ctx.send("Please enter the trainer's Pokemon Edu Rank."))
        msg = (await bot.wait_for('message', check=skill_level_check))
        chances = (int(msg.content) - 2)
        (await sent.delete())
        (await msg.delete())
        if (target.lower() not in ret_string.split('Event in slot')[0].lower()):
            (await ctx.send(
                'Hunting Target was not found in roll. Would the player like spend stamina to reroll? Type y or n now to respond.'))
            msg = (await bot.wait_for('message', check=check))
            if (msg.content.lower() == 'y'):
                ret_string = roll_exploration(area, tl, pl, None, None, repel_array, bait_mons, extra_players)
                if (target.lower() not in ret_string.split('Event in slot')[0].lower()):
                    while (chances > 0):
                        chances -= 1
                        (await ctx.send(
                            'Hunting Target was not found in roll. Would the player like to reroll? Type y or n now to respond.'))
                        msg = (await bot.wait_for('message', check=check))
                        if (msg.content.lower() == 'y'):
                            ret_string = roll_exploration(area, tl, pl, None, None, repel_array, bait_mons,
                                                          extra_players)
                        else:
                            break
                        if (target.lower() in ret_string.split('Event in slot')[0].lower()):
                            break
    (await ctx.send(ret_string))
    if (intent == 'w'):
        (await ctx.send('\nNow Creating Wander Event...\n'))
        g_details = get_wander_event()
        g_array = segment_text(g_details)
        for par in g_array:
            (await ctx.send(par))
        (await ctx.send('Would you like to reroll this wandering event? Type y or n now to respond.'))
        msg = (await bot.wait_for('message', check=check))
        if (msg.content.lower() == 'y'):
            g_details = get_wander_event()
            g_array = segment_text(g_details)
            for par in g_array:
                (await ctx.send(par))
            (await ctx.send(
                'Would you like to reroll this wandering event? You will have no more rerolls after this. Type y or n now to respond.'))
            msg = (await bot.wait_for('message', check=check))
            if (msg.content.lower() == 'y'):
                g_details = get_wander_event()
                g_array = segment_text(g_details)
                for par in g_array:
                    (await ctx.send(par))
    if (intent == 't'):
        training_changes = '**Please make the following additions to the encounter:**\n\n» Choose one of the Encountered Pokemon to be the Leader of all the other Pokemon. The Leader will have its level increase by 1/2 of the highest Trainer Level in the Party and will start with +1 CS in all Stats.\n» You may choose to have the Encounter affected by an Attack with the Field Keyword that is known by one of the Encountered Pokemon. This effect persists until the end of the Scene unless overwritten.\n» You may choose to have one of the Encountered Pokemon gain a Raid Boss or Swarm Boss Template. '
        (await ctx.send(training_changes))
    if (intent == 's'):
        scav_string = ''
        for i in range(0, (1 + extra_players)):
            scav_string += ('You have scavenged the following: ' + roll_harvest_table(area))
        (await ctx.send(scav_string))

"""


@bot.command(name='feature', aliases=['feats'])
async def feature(ctx, *arg):
    arg_full = ' '.join(arg)
    result = get_feature_data(arg_full)
    ret_string = ''.join(result)
    (await ctx.send(ret_string))


@bot.command(name='finance')
async def finance(ctx, arg):
    try:
        sum_total = roll_interest(int(arg))
        (await ctx.send(sum_total))
    except TypeError:
        (await ctx.send('This is not a valid amount of money. Please try again.'))


@bot.command(name='flora')
async def flora(ctx, *args):
    tier = args[0]
    amt = args[1]
    ret_string = roll_flora(tier, amt)
    (await ctx.send(ret_string))


@bot.command(name='fossil')
async def fossil(ctx):
    result = fossil_roller()
    ret_string = (('You have unearthed a ' + result) + '!')
    (await ctx.send(ret_string))


@bot.command(name='guardian')
async def guardian(ctx, *args):
    area = ' '.join(args)
    g_details = get_guardian_info(area)
    if (len(g_details) > 2000):
        g_array = segment_text(g_details)
        for msg in g_array:
            (await ctx.author.send(msg))
    else:
        (await ctx.author.send(g_details))
    str_log = (((str(ctx.author.name) + ' used the guardian command with the parameter {0} on '.format(
        area)) + datetime.now().strftime('%m/%d/%Y %H:%M:%S')) + '\n')
    with open('Documents/log.txt', 'a') as logfile:
        logfile.write(str_log)


@bot.command(name='habitat', aliases=['habit'])
async def habitat(ctx, *arg):
    arg_full = ' '.join(arg)
    result = list_habitats(arg_full)
    (await ctx.send(result))


"""
@bot.command(name='poryhelp', aliases=['phelp'])
async def help(ctx):
    menu_one = list(get_cat_first())

    def menu_one_check(m):
        return ((user == m.author) and (m.channel == channel) and (int(m.content) in range(0, len(menu_one))))

    user = ctx.author
    channel = ctx.channel
    msg = 'Welcome to the Porybot Help Menu. Please select the category of command you are attempting to use by typing the number next to the category.'
    for i in range(len(menu_one)):
        msg += ((('\n' + str(i)) + '. ') + menu_one[i])
    embed = discord.Embed(title='Porybot Help Menu - Categories', description=msg, color=4260860)
    sent = (await ctx.send(embed=embed))
    choice = (await bot.wait_for('message', check=menu_one_check))
    (await sent.delete())
    menu_two = list(get_cat_second(menu_one[int(choice.content)]))

    def menu_two_check(m):
        return ((user == m.author) and (m.channel == channel) and (int(m.content) in range(0, len(menu_two))))

    msg = 'Please choose one of the following commands by typing the number next to it. The description of that command will then be displayed.'
    for i in range(len(menu_two)):
        msg += ((('\n' + str(i)) + '. ') + menu_two[i])
    embed = discord.Embed(title='Porybot Help Menu - Commands', description=msg, color=4260860)
    sent = (await ctx.send(embed=embed))
    choice_two = (await bot.wait_for('message', check=menu_two_check))
    (await sent.delete())
    descrip = command_help(menu_one[int(choice.content)], menu_two[int(choice_two.content)])
    embed = discord.Embed(title=('!' + menu_two[int(choice_two.content)]), description=descrip, color=4260860)
    (await ctx.send(embed=embed))
"""


@bot.command(name='items')
async def items(ctx, *arg):
    arg_full = ' '.join(arg)
    result = get_item_data(arg_full)
    ret_string = ''.join(result)
    (await ctx.send(ret_string))


@bot.command(name='keymoves', aliases=['kmoves'])
async def keymoves(ctx, *arg):
    arg_full = ' '.join(arg)
    result = get_keyword_moves(arg_full)
    if len(result) >= 2000:
        m_array = segment_list(result)
        for msg in m_array:
            (await ctx.send(msg))
    else:
        (await ctx.send(result))


@bot.command(name='keyword')
async def keyword(ctx, *arg):
    arg_full = ' '.join(arg)
    result = get_keyword_data(arg_full)
    (await ctx.send(result))


@bot.command(name='lookup', aliases=['search'])
async def lookup(ctx, *args):
    arg_full = ' '.join(args)
    ret_string = get_info_categories(arg_full)
    (await ctx.send(ret_string))


@bot.command(name='lorebook')
async def lorebook(ctx, *arg):
    name = ' '.join(arg).lower()
    pages = get_lore_entry(name)
    if pages:
        for page in pages:
            (await ctx.author.send(file=discord.File(page)))
            os.remove(page)
    else:
        (await ctx.send('There is no area with this name / topic with this name in the lore book. Please try again.'))


@bot.command(name='lum')
async def lum(ctx, *arg):
    arg_full = ' '.join(arg)
    result = learn_move(arg_full)
    if (len(result) > 2000):
        m_array = segment_list(result)
        for msg in m_array:
            (await ctx.send(msg))
    else:
        (await ctx.send(result))


@bot.command(name='manu')
async def manu(ctx, *arg):
    arg_full = ' '.join(arg)
    result = get_man_data(arg_full)
    ret_string = ''.join(result)
    (await ctx.send(ret_string))


@bot.command(name='mech')
async def mech(ctx):
    channel = ctx.channel
    user = ctx.author
    ops = 'Please type out one of the following options: '
    ops += ', '.join(show_mechanics())
    (await ctx.send(ops))

    def check(m):
        return ((m.author == user) and (m.channel == channel) and (
                m.content.lower() in (string.lower() for string in show_mechanics())))

    msg = (await bot.wait_for('message', check=check))
    (await ctx.send(get_mechanic(msg.content.lower())))


@bot.command(name='move')
async def move(ctx, *arg):
    arg_full = ' '.join(arg)
    result = get_move_data(arg_full)
    ret_string = ''.join(result)
    (await ctx.send(ret_string))


@bot.command(name='muffin')
async def muffin(ctx):
    muf_var = random.randint(1, 4)
    (await ctx.send(file=discord.File('Images/muffin_{0}.png'.format(muf_var))))


@bot.command(name='mythos')
@commands.guild_only()
async def mythos(ctx, *args):
    legend_tuple = args
    legend = ' '.join(legend_tuple)
    notice = ((str(ctx.author.name) + ' used the mythos command to search up info on ') + legend)
    (await ctx.send(notice))
    msg = get_legend_personality(legend)
    (await ctx.author.send(msg))
    eastern = timezone('US/Eastern')
    str_log = (((str(ctx.author.name) + ' used the mythos command with parameter {0} on '.format(
        legend)) + datetime.now(eastern).strftime('%m/%d/%Y %I:%M %p')) + '\n')
    with open('Documents/log.txt', 'a') as logfile:
        logfile.write(str_log)


@bot.command(name='offerings')
async def offerings(ctx):
    (await ctx.send(roll_deity()))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.CommandInvokeError):
        message = ('Command Error: Something went wrong. Please check command details and try again.\n' + str(error))
        print(error)
        print(('\nCommand User: ' + str(ctx.author)))
        (await ctx.send(message, delete_after=10))


@bot.command(name='patronage')
@commands.guild_only()
async def patronage(ctx, *args):
    category = args[0]
    legend_tuple = args[1:]
    legend = ' '.join(legend_tuple)
    if (category.title() not in PATRONAGE_CATEGORIES):
        (await ctx.send((category + ' is not a valid option. Please input Minor, Major, Pact, or Task')))
    else:
        notice = ((str(ctx.author.name) + ' used the patronage command to search up info on ') + legend)
        (await ctx.send(notice))
        ret_array = get_patronage_task(legend, category)
        for msg in ret_array:
            (await ctx.author.send(msg))
        eastern = timezone('US/Eastern')
        str_log = (((str(ctx.author.name) + ' used the patronage command with parameters [{0[0]}, {0[1]}] on '.format(
            [category, legend])) + datetime.now(eastern).strftime('%m/%d/%Y %I:%M %p')) + '\n')
        with open('Documents/log.txt', 'a') as logfile:
            logfile.write(str_log)


@bot.command(name='pokedex', aliases=['pokédex'])
async def pokedex(ctx, *arg):
    name = ' '.join(arg).lower()
    get_dex_entry(name)
    (await ctx.author.send(file=discord.File('{0}.png'.format(name))))
    os.remove('{0}.png'.format(name))


@bot.command(name='pokerandom', aliases=['prand'])
async def pokerandom(ctx):
    ret_string = (('You have encountered a wild ' + roll_mon()) + '!')
    (await ctx.send(ret_string))


@bot.command(name='portal')
async def portal(ctx):
    (await ctx.send(roll_dim()))


@bot.command(name='potofgreed')
async def potofgreed(ctx):
    (await ctx.send('You draw two cards.'))


@bot.command(name='randombuild')
async def randombuild(ctx):
    (await ctx.send(random_build()))


@bot.command(name='shards')
async def shards(ctx, *args):
    shard_array = ''.join(args).split(',')
    shards = [0, 0, 0, 0, 0, 0]
    for shard in shard_array:
        shards[(int(shard) - 1)] += 1
    ret_string = 'You found:\n{0[0]} Red Shards\n{0[1]} Orange Shards\n{0[2]} Yellow Shards\n{0[3]} Green Shards\n{0[4]} Blue Shards\n{0[5]} Violet Shards'.format(
        shards)
    (await ctx.send(ret_string))


@bot.command(name='style', aliases=['smoves'])
async def style(ctx, *arg):
    style = arg[0]
    typing = arg[1]
    result = get_flair_moves(style, typing)
    if (len(result) > 2000):
        m_array = segment_list(result)
        for msg in m_array:
            (await ctx.send(msg))
    else:
        (await ctx.send(result))


@bot.command(name='tech')
async def tech(ctx, *arg):
    arg_full = ' '.join(arg)
    result = get_technique(arg_full)
    (await ctx.send(result))


@bot.command(name='order')
async def tech(ctx, *args):
    arg_full = ' '.join(args)
    result = get_order(arg_full)
    (await ctx.send(result))


@bot.command(name='town')
async def town(ctx, *arg):
    arg_full = ' '.join(arg)
    result = roll_town(arg_full)
    (await ctx.send(result))


@bot.command(name='townevent', aliases=['tevent'])
async def townevent(ctx):
    result = roll_town_event()
    ret_string = ((((('Event Invoked By: ' + ctx.author.mention) + '\n') + result[0]) + '\n') + result[1])
    (await ctx.send(ret_string))


@bot.command(name='trait')
async def trait(ctx, *arg):
    arg_full = ' '.join(arg)
    result = get_trait_data(arg_full)
    ret_string = ''.join(result)
    (await ctx.send(ret_string))


@bot.command(name='treasure', aliases=['tfind'])
async def treasure(ctx, *args):
    arg_full = ' '.join(args)
    result = get_treasure_spot(arg_full)
    (await ctx.send(result))


@bot.command(name='uprising')
async def uprising(ctx):
    result = roll_uprising_event()
    ret_string = ((((('Event Invoked By: ' + ctx.author.mention) + '\n') + result[0]) + '\n') + result[1])
    (await ctx.send(ret_string))


@bot.command(name='wander')
async def wander(ctx):
    g_details = get_wander_event()
    g_array = segment_text(g_details)
    for msg in g_array:
        (await ctx.send(msg))


# NEW COMMANDS FOR PORYBOT 2.0

# GUILD SPECIFIC COMMANDS:


# @bot.event
# async def on_ready():
#     bot.tree.copy_global_to(guild=UNDAUNTED_GUILD_ID)
#     await bot.tree.sync(guild=UNDAUNTED_GUILD_ID)
#
#
# @bot.tree.command(name='advgen')
# async def advgen(interaction: discord.Interaction):
#     view = AdventureModal()
#     await interaction.response.send_modal(view)
#     primary_details = view.enc_details
#     channel = interaction.channel
#     await channel.send(primary_details)


bot.run(TOKEN)
