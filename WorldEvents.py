import random

import utilities
from CollectData import worlddex
from Constants import *
from EncounterGenerator import generate_mon_from_area
from RollingCommands import roll_town


class WorldEventGenerator:
    common_events = [
        "pokemon_swarm",
        "weather_report",
        "wild_attack",
        "public_project",
    ]
    rare_events = [
        "seasonal_bloom",
        "local_festival",
        "leyline_flux",
        "local_contagion",
        "regional_tournament",
        "gold_rush"
    ]

    very_rare_events = ["guardian_insurgence"]
    event_types = [common_events, rare_events]
    event_weights = [0.7, 0.3]
    adventure_areas = [area for area in worlddex["Effect Slots"].keys() if
                       worlddex["Effect Slots"][area]["ExploCategory"] == "Adventure"]
    guardian_areas = [area for area in adventure_areas if worlddex["Event Slots"][area][20][0] == "Guardian Rising"]
    cave_areas = [area for area in worlddex["Effect Slots"].keys() if worlddex["Effect Slots"][area]["Biome"] == "Cave"]
    area_options = list(worlddex["Event Slots"].keys())
    aura_options = [
        "**Archaic Aura**: At the end of each Round, al Trainers gain +1 AP.",
        "**Celestial Aura**: All Save Checks during this Encounter have a +3 Modifier.",
        "**Chaotic Aura**: At the end of each Round, the Attack Metronome will be used, targeting a random "
        "Combatant. The Attack’s offensive Stat is based on 2 times the highest Trainer Level.",
        "**Dampening Aura**: Combat Stages cannot be increased in this Area.",
        "**Healing Aura**: At the end of each Round, all Combatants gain a Tick of HP and a Tick of "
        "Temporary HP.",
        "**Negative Aura**: All Combat Stage changed are reversed (Gain becomes Lose, Lose becomes Gain)",
        "**Oppressive Aura**: All Wild Combatants in this Area wll have the Very Hostile Disposition and "
        "cannot be changed.",
    ]
    weather_categories = [[' Dark', 'Electric', 'Fire', 'Flying', 'Normal', 'Water'],
                          ['Ghost', 'Grass', 'Ground', 'Ice', 'Rock'],
                          ['Bug', 'Dragon', 'Fairy', 'Fighting', 'Poison', 'Psychic', 'Steel']]
    swarm_variants = {
        'Basic Swarm': ('Common',
                        'All Encounters in this Area have +1 Pokemon of the Random Pokemon added, or +2 if there are '
                        '3 or more Trainers in the party. Whenever a Pokemon is defeated and removed from the area, '
                        'the Trainer who did (or whose Pokemon did), gains $1000'),
        'Vast Swarm': ('Rare',
                       'All Encounters in this Area can only have the Random Pokemon encountered.Whenever a Pokemon '
                       'is defeated and removed from the area, the Trainer who did (or whose Pokemon did), '
                       'gains $1000'),
        'Pokemon Den': ('Rare',
                        'All Encounters in this Area have +2 Pokemon of the Random Pokemon added, or +4 if there are '
                        '3 or more Trainers in the party. These Pokemon will be Level 5. Alternatively, there may be '
                        'a number of Pokemon eggs of that Species equal to the number of Players, each having 2 '
                        'Random Tier 1 Tutor Attacks'),
        'Massive Swarm': ('Rare',
                          'All Encounters in this Area have a Swarm Boss of the chosen Species added. whenever the '
                          'boss is defeated and removed from the area, the Player that did so gets $2,000 and +2 Fame '
                          'with Notoriety going to that region')
    }
    contagions_dict = {
        'Astral Contagion': 'Pokemon captured in this Area have been influenced by the Astral Plane somehow, either being affected visually by nightmares or dreams as if they were born in that Plane. While affected they have -1 Default CS to all Stats whenever they’re not in the Astral Plane (can’t be overwritten). When generated, determined if affected by Dream or Nightmare Plane. When curing the Battle Scar, 5 Fadeweave or Shroudveil need to be expended as well, respectively.',
        'Bloodrage Contagion': 'Pokemon captured in this Area are always Enraged and cannot be cured until this Contagion is cured. Wild Pokemon with this Contagion are always treated as Very Hostile and cannot be calmed. If the Wild Pokemon is level 60 or above, they also start with +3 CS in an Attack Stat of their Choice.',
        'Chromia Contagion': 'Pokemon captured in this Area will be a unique color compared to their normal species. When the GM creates Pokemon in this area, roll a d50 for each. On a 50, they will be an Aberration that makes most sense based on the area.',
        'Lethargic Contagion': 'Pokemon captured in this Area cannot be hostile and start with -2 Default CS in Attack and Special Attack until this is cured. (can’t be overwritten)',
        'Overcharged Contagion': 'Pokemon captured in this Area start with the Numbed Battle Scar, gaining its effects until cured. If the Pokemon is Electric, while Paralyzed this way they lose Hit Points per turn as if they were Badly Poisoned.',
        'Parasitic Contagion': 'Pokemon captured in this Area are always confused until cured. While confused this way, the Attack they use and the Targets they choose must be randomly determined from legal options.',
        'Pathogen Contagion': 'Pokemon captured in this Area start with the Infected Battle Scar, gaining its effects until cured. If an ally ends their turn adjacent to them, roll a d20. On a 4 or less they also gain this Battle Scar until cured.',
        'Pokerus Contagion': 'Pokemon captured in this Area gain the Pokerus Variant Effect. While a Pokemon is affected by the Pokerus Contagion they start with 6 Vitamins of the GM’s choice and have one Stat’s Default CS set at +1 CS.',
        'Spatial Contagion': 'Pokemon captured in this Area gain the Ultra Capability until cured.'}

    public_projects = {
        'Construction Project': ['Gadgeteer', 'Innovator', 'Saboteur', 'Adaptive Engineer', 'Metal Worker',
                                 'Expert Athletics or Tech Edu'],
        'Diplomatic Project': ['Empath', 'Provocateur', 'Paragon', 'Covert Network', 'Expert Charm', 'Command',
                               'Guile or Intuition'],
        'Festival Project': ['Musician', 'Cheerleader', 'Dancer', 'Coordinator', 'Illusionist', 'Fashionista',
                             'Fashion Stylist', 'Regional Celebrity', 'Expert Charm or Acrobatics'],
        'Healthcare Project': ['Alchemist', 'Medic', 'Herbalist', 'Chemical Disassembler', 'First Aid Training',
                               'Healthcare Professional', 'Expert Med Edu'],
        'Hunger Project': ['Chefs', 'Herbalist', 'Simple Meals', 'Fruit Connoisseur', 'Fisherman',
                           'Culinary Specialties', 'Green Thumb', 'Expert Survival or Gen Edu'],
        'Occult Project': ['Scribe', 'Any Supernatural Class', 'Arcane Sight', 'Expert Occult Edu'],
        'Training Project': ['Commander', 'Taskmaster', 'any Fighter Class', 'Any Smith Trait', 'Rising Warrior',
                             'Expert Combat'],
        'Tutoring Project': ['Any Profession Class', 'Adjunct Professor', 'Combat Mentor', 'Pokemon Professor',
                             'Expert Edu Skill'],
        'Wilderness Project': ['Herbalist', 'Chronicler', 'Geomancer', 'Anthropologist', 'Beast Master', 'Cartographer',
                               'Daring Explorer', 'Expert Perception or Survival']
    }
    weather_weights = [0.6, 0.3, 0.1]
    chosen_events = []

    def execute_event(self, method_name):
        if hasattr(self, method_name) and callable(getattr(self, method_name)):
            return getattr(self, method_name)()
        else:
            return (
                    "There was an error in the program. The world event "
                    + method_name
                    + "does not corrospond to any "
                      "class method. Please try "
                      "again."
            )

    def select_event(self):
        event_category = random.choices(self.event_types, self.event_weights)[0]
        event_selected = random.choice(
            [i for i in event_category if i not in self.chosen_events]
        )
        self.chosen_events.append(event_selected)
        return self.execute_event(event_selected)

    @staticmethod
    def seasonal_bloom():
        region_chosen = random.choice(REGIONS)
        return (
                "__**Seasonal Bloom!**__\n"
                + "*The flowers are in bloom!*\n"
                + "\n"
                + "All Farm Slots in {region} gain a +4 to Yield Rolls "
                  "until the end of the Game Week".format(region=region_chosen)
        )

    def leyline_flux(self):
        region_chosen = random.choice(REGIONS)
        random_aura = random.choice(self.aura_options)
        return (
                "__**Leyline Flux!**__\n"
                + "*Arcana from the ground has been fluxuated!*\n"
                + "\n"
                + "The following effect is present in all encounters in {region}: \n".format(region=region_chosen)
                + "{effect}".format(effect=random_aura)
        )

    def weather_report(self):
        possible_weathers = []
        region_chosen = random.choice(REGIONS)
        for area in worlddex["Effect Slots"].values():
            if area["Region"] == region_chosen:
                possible_weathers.append(area["Type1"])
                possible_weathers.append(area["Type2"])
                possible_weathers.append(area["Type3"])
        unique_weathers = utilities.unique(possible_weathers)
        weather_choices = utilities.intersection(unique_weathers,
                                                 random.choices(self.weather_categories, self.weather_weights)[0])
        weather_chosen = random.choice(weather_choices)
        weather_qualities = random.choices(["Damaging", "Boosting"], [0.25, 0.75])[0]
        return '**Weather Report: A storm is brewing**\nThe {Region} Region has been hit with a sudden storm. If ' \
               'an Encounter would occur within the {Region} Region, ' \
               '{Quality} {Type} Weather enters the Scene unless an ' \
               'Event or Area Effect would already cause Weather.'.format(
            Region=region_chosen, Quality=weather_qualities, Type=weather_chosen)

    @staticmethod
    def regional_tournament():
        region = random.choice(REGIONS)
        town = roll_town(region)
        return "**Regional Tournament**\nThe city/civilization " + town + "is hosting a Tournament or sparring event! " \
                                                                          "Whenever a clash encounter is performed in " \
                                                                          "the " + region + " region, the Winner will " \
                                                                                            "gain $3000 and Fame " \
                                                                                            "equal to double the " \
                                                                                            "Clash Trainer's Tier, " \
                                                                                            "with Notoriety going " \
                                                                                            "towards the " + region + \
            " region. Clash Trainers from this Event Encounter will usually be from " + town + ", however can be " \
                                                                                               "swapped out if deemed" \
                                                                                               " appropriate."

    @staticmethod
    def local_festival():
        region = random.choice(REGIONS)
        town = roll_town(region)
        return "**Local Festival**\nThe city/civilization " + town + "is hosting a festival of some sort! " \
                                                                     "Whenever a **Flair Battle [Minigame]** is performed in " \
                                                                     "the " + region + " region, the Winner gains $5,000. (Max 3 per Game Week). If the Battle had 4 or more Players, first Place gains $10,000 instead and second Place gains $5,000. The first Flair Battle a Player wins during this Game Week grants them 5 Fame with Notoriety going towards the " + region + \
            " region."

    def wild_attack(self):
        region = random.choice(REGIONS)
        town = roll_town(region)
        attacker_choices = [area for area in self.area_options if worlddex["Effect Slots"][area]["Region"] == region]
        attacker = random.choice(attacker_choices)
        ret_string = "**Wild Attack: The Wild is Attacking!**\n" + town + " is under attack by pokemon from " + \
                     attacker + "! Provided at least 3 Encounters in this Event are successful, " + town + \
                     " will manage to be unaffected. For each Failed Encounter or if 3 Encounters are not successful, " \
                     + town + " may be affected in some way.\n When GMing this Event, add 2 Pokemon from " + attacker + \
                     "for each member of the Party. This Encounter will have the [Defense] and [Survival] Objective (" \
                     "See: Encounter Objectives) and be successful at the end of Round 5. The Object requiring " \
                     "defending is the City Walls or a random building within the city and will have the Stat of a " \
                     "Platinum Tier Inanimate Object. If the Party is under Trainer Level 10, they will instead be " \
                     "defending something that is a Silver Tier Inanimate Object.\n**Note**: As a GM you can alter " \
                     "the statting of this Event in various ways such as using multiple defended Objects of a lower " \
                     "Tier and calculating their total HP loss for sake of Rewards. You can also add allied Clash " \
                     "Trainer NPCs but in return raise the number of Max Pokemon Enemies by an equivalent " \
                     "amount.\n**Unharmed (100%)** - 10 TXP | 5x PXP | $5,000 to each + 4 Fame\n**Harmed (50-99%)** - " \
                     "8 TXP | 4x PXP | $5,000 to each + 2 Fame\n**Injured (1-49%)** - 5 TXP | 4x PXP | $2," \
                     "500 to each\n**Destroyed (Fainted)** - 5 TXP | 0 PXP | No other Reward"
        return ret_string

    def pokemon_swarm(self):
        region = random.choice(REGIONS)  # First, Select a random region using the random region function
        curated_list = [area for area in self.area_options if worlddex["Effect Slots"][area]["Region"] == region]  #
        # Second, create a filtered list of every encounter area which lists that region in the Region key of its
        # Effect Slots entry.
        swarm_areas = random.sample(curated_list,
                                    k=2)  # Third, select 2 elements using random.sample(curated_list, k=2). This will return a list of two unique elements from the curated list. Name this list variable swarm_areas. Slot 0 is where the  swarm is taking place. Slot 1 is where the swarming pokemon is from.
        swarm_event = random.choices(list(self.swarm_variants.keys()), weights=[.7, .1, .1,
                                                                                .1])  # Fourth, select a swarm variant using  random.choices(list(swarm_variants.keys()), weights=[.7, .1, .1, .1])
        encounter_table = worlddex["Encounter Slots"][swarm_areas[
            1]]  # Fifth, create variable for encounter  table equal to worlddex["Encounter Slots"][swarm_areas[1]]
        swarm_mon = generate_mon_from_area(
            encounter_table)  # Sixth, use the generate_mon_from_area function to grab a pokemon from the area, Seventh, return event description
        return '__**Pokemon Swarm**__\n*A Swarm is threatening the native Pokemon*\nA Swarm of {Pokemon} has appeared ' \
               'in {Area}, located in the {Region}. The following Swarm Event has been rolled:\n*{EventName}*\n{EventDesc}'.format(
            Pokemon=swarm_mon, Area=swarm_areas[0], Region=region, EventName=swarm_event,
            EventDesc=self.swarm_variants[swarm_event][1])

    def local_contagion(self):
        area = random.choice(self.area_options)
        contagion = random.choice(list(self.contagions_dict))
        return "**__Local Contagion__**\n*A Disease has spread across " + area + " and is temporarily afflicting the Populace!*\nThe contagion in question is the **" + contagion + "**. Any Pokemon captured in " + area + " are afflicted with the Contagion until they are cured. The Contagion can be cured as if it were a Battle Scar, thereby removing all effects that were inflicted as a result of this Event. Upon being cured, the Pokemon will gain +20 Loyalty Points. The contagion has the following effects:\n" + \
            self.contagions_dict[contagion]

    def public_project(self):
        region = random.choice(REGIONS)
        city = roll_town(region)
        project = random.choice(list(self.public_projects.keys()))
        return "**__Public Project!__**\n*Hiring All Willing Workers*\n" + city + " is requesting assistance with a " + project + "**Moderator will come up with a Scenario as to the specifics of what the Project will be fluffed as.** A total of 50 Stamina needs to be invested in the Project by the end of the Game Week to be considered completed. (Players tell Moderators to keep a tracker). If the Project is completed, anyone who invested at least 5 Stamina will gain +5 Fame with Notoriety going towards the associated Region of that City. Whenever someone invests Stamina in this Project, they gain Money equal to 1.5x their Income value. Only individuals with one of the following qualifications can contribute:\n" + \
            ", ".join(self.public_projects[project])

    def gold_rush(self):
        chosen_cave = random.choice(self.cave_areas)
        return "**__Gold Rush__**\n*Diancie has refreshed a location!*\n The Cave Area {0} has been refreshed. At the end of a Successful Encounter in {0}, anyone with a Mining Kit may spend 3 Stamina to have a chance at gaining valuable ore and treasures. To do so, use the /mining command.".format(chosen_cave)
