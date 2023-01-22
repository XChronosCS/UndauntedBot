import discord

from EncounterGenerator import *


async def adventure_results_publish(adventure_results, interaction):
    no_note_mon_array = [poke[0] for poke in adventure_results["Encounters"] if poke[1] is None]
    note_mon_array = ["{0}: {1}\n".format(poke[0], poke[1]) for poke in adventure_results["Encounters"] if
                      poke[1] is not None]
    result = 'ADVENTURE GENERATION RESULTS:\n' + '\n' + '**Pokemon Encountered**: {pokemon}\n'.format(
        pokemon=", ".join(no_note_mon_array))
    if len(note_mon_array) != 0:
        result += '__Notes__: {Notes}\n'.format(Notes="".join(note_mon_array)) + '\n'
    else:
        result += '\n'
    result += '**Event Rolled**: {Event}\n'.format(Event=
                                                   adventure_results["Event"][
                                                       0]) + '__Description__: {EventDescription}\n'.format(
        EventDescription=adventure_results["Event"][1]) + '\n'
    if adventure_results["Treasure Rolled"] is not None:
        result += '**Treasure Rolled**: {Treasure}\n'.format(
            Treasure=adventure_results["Treasure Rolled"][0]) + '__Description__: {TreasureDescription}\n'.format(
            TreasureDescription=adventure_results["Treasure Rolled"][
                1]) + '__Defending Pokemon__: {TreasureDefender}\n'.format(
            TreasureDefender=adventure_results["Treasure Guardian"][0]) + ('__Notes__: {DefenderNotes}\n'.format(
            DefenderNotes=adventure_results["Treasure Guardian"][1]) if adventure_results["Treasure Guardian"][
                                                                            1] is not None else "\n") + '\n'
    if adventure_results["Honor Spent"] != 0:
        result += '**Number of Treasure Hunts Performed:** {NumHonor}\n'.format(NumHonor=
                                                                                str(adventure_results[
                                                                                        "Honor Spent"])) + '\n'
    area_details = adventure_results["Area Description"]
    result += '**Area Trial**: {Trial}\n\n**Area Features**: {Features}\n\n**Area Entry Requirements**: {Reqs}'.format(
        Trial=area_details[0].rstrip(), Features=area_details[1].rstrip(), Reqs=area_details[2].rstrip())
    channel = interaction.channel
    if (len(result) > 2000):
        m_array = segment_list(result)
        for msg in m_array:
            (await channel.send(msg))
    else:
        (await channel.send(result))


class OptionalDetails(discord.ui.Modal, title="Optional Details"):
    enc_details = {}

    def set_details(self, req_details):
        self.enc_details.update(req_details)

    treasure_target = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="What Slot are you Treasure Hunting?",
        required=False,
        default='0',
        placeholder="Leave Empty if None"
    )

    num_th = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Num TH, Rolls per TH?",
        required=False,
        default='0, 3',
        placeholder="Ex: 5, 5"
    )

    repelled_slots = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Repelled Slots? Comma Between",
        required=False,
        default='0',
        placeholder="Empty if None. Ex: 1, 4, 5"
    )

    forced_mon = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Forced Mon Slot?",
        required=False,
        default='0',
        placeholder="Leave Empty if None"
    )

    forced_event = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Forced Event Slot?",
        required=False,
        default='0',
        placeholder="Leave Empty if None"
    )

    async def on_submit(self, interaction: discord.Interaction):
        self.enc_details["TH Target"] = int(self.treasure_target.value)
        self.enc_details["Num TH"] = int(self.num_th.value.split(", ")[0])
        self.enc_details["Num Per TH"] = int(self.num_th.value.split(", ")[1])
        self.enc_details["Repel Array"] = [int(i) for i in self.repelled_slots.value.split(", ")]
        self.enc_details["Forced Slot"] = int(self.forced_mon.value)
        self.enc_details["Forced Event"] = int(self.forced_event.value)
        await adventure_results_publish(generate_adventure(self.enc_details), interaction)
        await interaction.response.defer()


class SimpleView(discord.ui.View):
    req_details = {}

    def assign_req(self, rd):
        self.req_details = rd

    @discord.ui.button(label="Add Optional Details",
                       style=discord.ButtonStyle.success)
    async def hello(self, interaction: discord.Interaction, button: discord.ui.Button):
        op_modal = OptionalDetails()
        op_modal.set_details(req_details=self.req_details)
        await interaction.response.send_modal(op_modal)

    @discord.ui.button(label="Generate Now",
                       style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await adventure_results_publish(generate_adventure(self.req_details), interaction)
        self.stop()


class AdventureModal(discord.ui.Modal, title="Adventure Generation"):
    enc_details = {
        "Num TH": 0,
        "Num Per TH": 0,
        "TH Target": 0,
        "Repel Array": [],
        "Forced Slot": 0,
        "Forced Event": 0,
        "Extra Mons": 0
    }

    encounter_area = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="What is the Encounter Area?",
        required=True,
        placeholder="Type Encounter Area here"
    )

    num_players = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="How many players?",
        required=True,
        placeholder="Type # from 1 to 4"
    )

    max_trainer_level = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Average Trainer Level?",
        required=True,
        placeholder="Type # from 1 to 40"
    )

    max_poke_level = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Average Strongest Pokemon Level?",
        required=True,
        placeholder="Type # from 1 to 100"
    )

    additional_mons = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="How many additional pokemon rolls?",
        required=False,
        default='0',
        placeholder="Leave Empty if None"
    )

    async def on_submit(self, interaction: discord.Interaction):
        self.enc_details["Area"] = self.encounter_area.value
        self.enc_details["Num Players"] = int(self.num_players.value)
        self.enc_details["Avg Poke Lvl"] = int(self.max_poke_level.value)
        self.enc_details["Avg Trainer Lvl"] = int(self.max_trainer_level.value)
        self.enc_details["Extra Mons"] = int(self.additional_mons.value)
        next_view = SimpleView()
        next_view.assign_req(self.enc_details)
        await interaction.response.send_message(
            content="Would you like to add Optional Information? Ex. Forced Slots, Forced Events, Repelled Slots, "
                    "Treasure Hunt, etc.",
            view=next_view)


class PXPCalcView(discord.ui.View):
    num_players = 0
    encounter_type = 0
    doubled = False

    @discord.ui.select(placeholder="Select Encounter Type",
                       options=[discord.SelectOption(label=name[0], value=name[1]) for name in
                                [("Exploration Base", "EB 3"), ("Exploration Training Intent", " ETI 5"),
                                 ("Raid", "R 5"),
                                 ("Adventure Trial Pass", "ATP 4"), ("Adventure Trial Fail", " ATF 2"),
                                 ("Clash Encounter", "CE 3"),
                                 ("Rescue Encounter", "RE 3"), ("Request Encounter", "RQE 5"),
                                 ("Gauntlet Encounter", "GE 5")]], max_values=1, row=0)
    async def select_1(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.encounter_type = int(select.values[0].split(" ")[1])
        await interaction.response.defer()

    @discord.ui.select(placeholder="# Players",
                       options=[discord.SelectOption(label=str(i + 1), value=str(i + 1)) for i in range(4)],
                       max_values=1, row=1)
    async def select_2(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.num_players = int(select.values[0])
        await interaction.response.defer()

    @discord.ui.select(placeholder="Choose if doubled or not",
                       options=[discord.SelectOption(label=i, value=i) for i in ["Yes", "No"]],
                       max_values=1, row=2)
    async def select_3(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.doubled = True if select.values[0] == "Yes" else False
        await interaction.response.defer()

    @discord.ui.button(label="Press to Continue",
                       style=discord.ButtonStyle.success, row=3)
    async def submit(self, interaction: discord.Interaction, button: discord.ui.Button):
        op_modal = PXPCalcModal()
        op_modal.assign_req(np=self.num_players, et=self.encounter_type, d=self.doubled)
        await interaction.response.send_modal(op_modal)


class PXPCalcModal(discord.ui.Modal, title="Pokemon Details"):
    calculation = 0
    num_players = None
    encounter_type = None
    doubled = False

    def assign_req(self, np, et, d):
        self.num_players = np
        self.encounter_type = et
        self.doubled = d

    mon_levels = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Type Num Pokemon, Average Level",
        required=True,
        placeholder="Ex: 4, 35"
    )

    raid_levels = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Type Num Raid Bosses, Average Level",
        required=False,
        default='0, 0',
        placeholder="Ex: 2, 45. Leave blank if not applicable"
    )

    swarm_levels = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Type Num Swarm Bosses, Average Level",
        required=False,
        default='0, 0',
        placeholder="Ex: 1, 40. Leave blank if not applicable"
    )

    minion_levels = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Type Num Minions, Average Level",
        required=False,
        default='0, 0',
        placeholder="Ex: 2, 25. Leave blank if not applicable"
    )

    clash_levels = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Type Num Trainers, Average Tier",
        required=False,
        default='0, 0',
        placeholder="Ex: 2, 2. Leave blank if not applicable"
    )

    async def on_submit(self, interaction: discord.Interaction):
        for i in [self.mon_levels, self.clash_levels, self.minion_levels]:
            muliply_tuple = i.value.split(", ")
            self.calculation += int(muliply_tuple[0]) * int(muliply_tuple[1])
        raid_boss_info = self.raid_levels.value.split(", ")
        self.calculation += int(raid_boss_info[1]) * int(raid_boss_info[0]) * (3 if self.num_players >= 3 else 2)
        swarm_boss_info = self.swarm_levels.value.split(", ")
        self.calculation += int(swarm_boss_info[1]) * int(swarm_boss_info[0]) * (self.num_players + 1)
        self.calculation *= (self.encounter_type * 2 if self.doubled else self.encounter_type)
        await interaction.response.send_message(
            content="The total amount of PXP gained in this encounter is: " + str(self.calculation))


class PXPCalcView2(discord.ui.View):
    num_players = 0
    encounter_type = 0
    doubled = False

    @discord.ui.select(placeholder="Select Encounter Type",
                       options=[discord.SelectOption(label=name[0], value=name[1]) for name in
                                [("Exploration Base", "EB 3"), ("Exploration Training Intent", "ETI 5"),
                                 ("Raid", "R 5"),
                                 ("Adventure Trial Pass", "ATP 4"), ("Adventure Trial Fail", " ATF 2"),
                                 ("Clash Encounter", "CE 3"),
                                 ("Rescue Encounter", "RE 3"), ("Request Encounter", "RQE 5"),
                                 ("Gauntlet Encounter", "GE 5")]], max_values=1, row=0)
    async def select_1(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.encounter_type = int(select.values[0].split(" ")[1])
        await interaction.response.defer()

    @discord.ui.select(placeholder="# Players",
                       options=[discord.SelectOption(label=str(i + 1), value=str(i + 1)) for i in range(4)],
                       max_values=1, row=1)
    async def select_2(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.num_players = int(select.values[0])
        await interaction.response.defer()

    @discord.ui.select(placeholder="Choose if doubled or not",
                       options=[discord.SelectOption(label=i, value=i) for i in ["Yes", "No"]],
                       max_values=1, row=2)
    async def select_3(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.doubled = True if select.values[0] == "Yes" else False
        await interaction.response.defer()

    @discord.ui.button(label="Press to Continue",
                       style=discord.ButtonStyle.success, row=3)
    async def submit(self, interaction: discord.Interaction, button: discord.ui.Button):
        op_modal = PXPCalcModal()
        op_modal.assign_req(np=self.num_players, et=self.encounter_type, d=self.doubled)
        await interaction.response.send_modal(op_modal)
