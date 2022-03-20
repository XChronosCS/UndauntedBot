ability_desc = "!ability [ability name] - brings up the description for that ability" \
               "\n\nUsage Example: !ability serene grace"
adinfo_desc = "!adinfo [Area] [Encounter] [Event] - Brings up the encounter slot and event slot info from new " \
              "adventure/exploration areas which have question " \
              "mark slots. Will inform appropriate roles of which slots need to now be filled in on the public sheet." \
              "\n\nUsage Example: If new area was an adventure area called Diglett Land:  !adinfo diglett land 14 11"
admon_desc = "!admon [Area] [Encounter] - Brings up the encounter slot info from new adventure/exploration areas which have question " \
             "mark slots. Will inform appropriate roles of which slots need to now be filled in on the public sheet." \
             "\n\nUsage Example: If new area was an adventure area called Diglett Land: !adinfo diglett land 26"
adventure_desc = "!adventure [Area][Trainer Level][Pokemon Level] - Procedurally generates an Adventure Encounter by asking questsion in the posted channel. Results are posted in rolls-and-commands." \
                 "\n\nUsage Example: !adventure Toxic Spa 40 80"
amons_desc = "!amons [ability] - Lists every pokemon that gets this specific ability." \
             "\n\nUsage Example: !amons huge power"
arcana_desc = "!arcana [Legendary] - Lists every Arcana Edge that can be learned by someone following the patronage of inputted Legendary." \
              "\n\nUsage Example: !arcana meloetta"
areaevent_desc = "THIS COMMAND IS CURRENTLY NOT IN OPERATION. PLEASE COME BACK LATER."
autostat_desc = "!autostat [Pokemon][Level][Email or Autostatter Page Link] - (Note: You can only use an Auto Statter Page if it was created by the Bot). Performs an Autostatter function on the Document and returns a link for th resulting sheet which is shared to the email the user sent for editing permission.  If this link is used as the third argument later, subsequent statting will be added as tabs to the linked sheet." \
                "\n\nUsage Example (email): !autostat Porygon 80 fake_email@gmail.com" \
                "\nUsage Example (link): !autostat Jumpluff 80 htttps://link"
babystat_desc = "!babystat [Pokemon][Level][Email or Autostatter Page Link] - Same as Auto Statting but the Pokemon won't automatically Evolve." \
                "\n\nUsage Example (email): !babystat Porygon 80 fake_email@gmail.com" \
                "\nUsage Example (link): !babystat Jumpluff 80 htttps://link"
capa_desc = "!capa [Capability] - Retrieves the description of a capability." \
            "\n\nUsage Example: !capa threaded"
chaos_desc = "!chaos [Basic | Advanced | Fluff | Combat | Status] - Roll from one of the chaos tables listed" \
             "\n\nUsage Example: !chaos Basic"
cmons_desc = "!cmons [capability] - Lists all pokemon that have the listed capability. Putting 'Overland X' where x is a number will put the number of pokemon with that specific movement capability. Putting 'Harvest' as the search item will bring up a menu for the various harvestable item capabilities." \
             "\n\nUsage Example: !cmons gilled"
cond_desc = "!cond [Condition] - Retrieves the description of a Status Condition" \
            "\n\nUsage Example: !cond burned"
cookie_desc = "!cookie @[User] - Gives a cookie to the pinged person\n\nUsage Example: !cookie @XChronos"
details_desc = "!details - Rolls a Random Nature, Gender, and Ability choice for a pokemon."
diceroll_desc = "!droll [Dice String] #[Text] - Performs dice roll operations. Add R# to the end of the dice string where # is any number to perform multiple iterations of a singular dice roll" \
                "\n\nUsage Example: !droll 1d20R1+6 #Test Roll"
edge_desc = "!edge [Edge Name] - Retrieves the description of an Edge" \
            "\n\nUsage Example: !edge acrobat"
eggmove_desc = "!eggmove [Type]  - Rolls a random egg/Pokémon of the listed type with a random Tier 1 Egg Move" \
               "\n\nUsage Example: !eggmove Ice"
eggrandom_desc = "!eggrandom - Rolls a random egg from every possible Type"
eggroll_desc = "!eggroll [Type]  - Rolls a random egg/Pokémon of the listed type\n\nUsage Example: !eggroll Ice"
encounter_desc = "THIS COMMAND IS CURRENTLY NOT IN OPERATION. PLEASE COME BACK LATER."
erm_desc = "!erm - Rolls a Random Egg from every possible type with a random Tier 1 Egg Move"
exploration_desc = "THIS COMMAND IS CURRENTLY NOT IN OPERATION. PLEASE COME BACK LATER."
feature_desc = "!feature [Feature Name] - Retrieves the description of a Feature" \
               "\n\nUsage Example: !feature Paragon"
finance_desc = "!finance [Bank Balance] - This automates the Financial Investment roll, shows you how much you earned, and your new total." \
               "\n\nUsage Example: !finance 10300"
fossil_desc = "!fossil  - Roll a Random Fossil from the Fossil Table"
guardian_desc = "!guardian [Area] - Sends you a private message detailing the Guardian Encounter for an Area. This command is tracked." \
                "\n\nUsage Example: !guardian Toxic Spa"
habitat_desc = "!habitat [pokemon] - Displays every location that pokemon can be found in. Only works on the base forms." \
               "\n\nUsage Example - !habitat diglett"
items_desc = "!items [item name] - Brings up the description of the requested item" \
             "\n\nUsage Example: !items rare candy"
keymoves_desc = "!keymoves [Keyword] - Returns a list of all moves with that specific keyword." \
                "\n\nUsage Example: !keymove friendly"
keyword_desc = "!keyword [Keyword Name] - Brings up the description of that keyword" \
               "\n\nUsage Example: !keyword friendly"
lookup_desc = "!lookup [Search Term] - Brings up the description of any searchable item in the system which has that name. IF a feature and an edge have the same name for example, both will be displayed." \
              "\n\nUsage Example: !lookup illusionist"
lum_desc = "!lum [move] - Lists every pokemon that gets the requested move by level up." \
           "\n\nUsage Example: !lum counter"
manu_desc = "!manu [Maneuver Name] - Brings up the description of that Maneuver" \
            "\n\nUsage Example: !manu intercept melee"
mech_desc = "!mech - Brings up a menu with all the different class mechanics. You can then type in the one you want explained to you, which will bring up its description"
move_desc = "!move [Move Name] - Brings up the description of that Move" \
            "\n\nUsage Example: !move aqua ring"
muffin_desc = "!muffin - posts picture of muffin from a preset list."
mythos_desc = "!mythos [Legendary] - This command will give you just the personality information for a specific legendary pokemon." \
              "\n\nUsage Example: !mythos mew"
offerings_desc = "!offerings - This automates the deific offering roll, then displays the result."
order_desc = "!order [Order Name] - Brings up the description of that Order" \
             "\n\nUsage Example: !order brutal training"
patronage_desc = "!patronage [X] [Y]: X is what you're requesting of the Legend, which can be Task, Minor, Major or Pact, each of which giving you either a Task or one of the Requests. Y is the name of the Legendary" \
                 "\n\nUsage Example: !patronage mew task"
pokerandom_desc = "!pokerandom  - Rolls a random pokemon"
portal_desc = "!portal: Opens a random portal to an area in ultra space"
shards_desc = "!shards [dice results]: Counts up how many shards you got from an encounter. " \
              "\n\nUsage Example: !shards 2, 4, 3, 5, 2, 1, 6, 6, 6, 1, 6, 5, 6, 5, 5"
tech_desc = "!tech [Technique Name] - Brings up the description of that class technique (Weapon Master, Commander, Trickster, etc.)" \
            "\n\nUsage Example: !tech saw that coming"
tm_desc = "!tm [move] - Lists every pokemon that gets the requested move by tutor move." \
          "\n\nUsage Example: !tm stomping tantrum"
town_desc = "!town [Region] - Rolls a random NPC Town within the selected region." \
            "\n\nUsage Example: !town fathis"
townevent_desc = "!townevent - Rolls a random Town event"
treasure_desc = "!treasure [Minor/Major Treasure] - Lists the location where requested treasure can be found" \
                "\n\nUsage Example: !treasure mythical bait"
turbo_desc = "!turbo - Posts :WoolooTurbo: Emote"
uprising_desc = "!uprising - Roll one of the Uprising Events"
wander_desc = "!wander - Generates and Posts a random Wander Event for Explorations"
whenfreya_desc = "!whenfreya - states how many days until the release of the Freya Region"
whenkostrya_desc = "!whenkostrya - states how many days until the release of the Kostrya Region"

HELP_CATEGORIES = {
    "Info Lookup": {'ability': ability_desc, 'cmons': cmons_desc, 'amons': amons_desc, 'cond': cond_desc,
                    'capa': capa_desc, 'edge': edge_desc, 'feature': feature_desc, 'habitat': habitat_desc,
                    'items': items_desc, 'keymoves': keymoves_desc, 'keyword': keyword_desc,
                    'lookup': lookup_desc, 'lum': lum_desc, 'manu': manu_desc, 'mech': mech_desc,
                    'move': move_desc, 'order': order_desc, 'tech': tech_desc, 'tm': tm_desc,
                    'treasure': treasure_desc},
    "Patronage": {'patronage': patronage_desc, 'mythos': mythos_desc, 'arcana': arcana_desc},
    "Encounters": {'adinfo': adinfo_desc, 'admon': admon_desc, 'adventure': adventure_desc,
                   'areaevent': areaevent_desc, 'autostat': autostat_desc, 'babystat': babystat_desc,
                   'encounter': encounter_desc, 'exploration': exploration_desc, 'guardian': guardian_desc,
                   'wander': wander_desc},
    "RNG/Utilities": {'chaos': chaos_desc, 'fossil': fossil_desc, 'droll': diceroll_desc,
                      'portal': portal_desc, 'finance': finance_desc, 'shards': shards_desc, 'town': town_desc,
                      'townevent': townevent_desc, 'uprising': uprising_desc, 'offerings': offerings_desc},
    "Breeding": {'eggmove': eggmove_desc, 'eggrandom': eggrandom_desc, 'eggroll': eggroll_desc, 'erm': erm_desc,
                 'details': details_desc, 'pokerandom': pokerandom_desc},
    "Memes": {'cookie': cookie_desc, 'muffin': muffin_desc, 'whenfreya': whenfreya_desc,
              'whenkostrya': whenkostrya_desc, 'turbo': turbo_desc, 'potofgreed' : 'Nobody Knows What This Command Does.'}}


def get_cat_first():
    return HELP_CATEGORIES.keys()


def get_cat_second(category):
    return HELP_CATEGORIES.get(category).keys()


def command_help(category, command):
    return HELP_CATEGORIES.get(category).get(command)
