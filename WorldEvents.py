import random

from CollectData import worlddex
from Constants import *


class WorldEventGenerator:
    common_events = [
        "pokemon_swarm",
        "weather_report",
        "wild_attack",
        "requested_charity",
        "public_project",
    ]
    rare_events = [
        "seasonal_bloom",
        "gold_rush",
        "local_festival",
        "leyline_flux",
        "exotic_trader",
        "local_contagion",
        "regional_tournament",
    ]
    very_rare_events = ["guardian_insurgence"]
    event_types = [common_events, rare_events, very_rare_events]
    event_weights = [0.7, 0.25, 0.05]
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
