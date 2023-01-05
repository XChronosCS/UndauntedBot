import discord


class OptionalDetails(discord.ui.Modal, title="Optional Details"):
    enc_details = {}

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

    max_level = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Average Strongest Pokemon Level?",
        required=True,
        placeholder="Type # from 1 to 80"
    )

    async def on_submit(self, interaction: discord.Interaction):
        self.enc_details["Area"] = self.encounter_area.value
        self.enc_details["Num Players "] = int(self.num_players.value)
        await interaction.response.send_message(content="Thank you.", ephemeral=True)


class SimpleView(discord.ui.View):

    @discord.ui.button(label="Add Optional Details",
                       style=discord.ButtonStyle.success)
    async def hello(self, interaction: discord.Interaction, button: discord.ui.Button):
        op_modal = OptionalDetails()
        await interaction.response.send_modal(op_modal)

    @discord.ui.button(label="Generate Now",
                       style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Cancelling")


class AdventureModal(discord.ui.Modal, title="Adventure Generation"):
    enc_details = {}

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

    max_level = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Average Strongest Pokemon Level?",
        required=True,
        placeholder="Type # from 1 to 100"
    )

    async def on_submit(self, interaction: discord.Interaction):
        self.enc_details["Area"] = self.encounter_area.value
        self.enc_details["Num Players "] = int(self.num_players.value)
        next_view = SimpleView()
        await interaction.response.send_message(
            content="Would you like to add Optional Information? Ex. Forced Slots, Forced Events, Repelled Slots, "
                    "Extra Mons, etc.",
            view=next_view)

# async def select_area(self, interaction: discord.Interaction, select_item: discord.ui.Select):
#     self.enc_details["Area"] = select_item.values
#     self.children[0].disabled = True
#     player_num = Number_Players()
#     self.add_item(player_num)
#     await interaction.message.edit(view=self)
#     await interaction.response.defer()
#
#
# async def respond_to_answer2(self, interaction: discord.Interaction, choices):
#     self.enc_details["Num Players"] = choices
#     self.children[1].disabled = True
#     await interaction.message.edit(view=self)
#     await interaction.response.defer()
#     self.stop()

# class SimpleView(discord.ui.View):
#     enc_details = {}
#
#     @discord.ui.select(custom_id="Encounter Slots", placeholder="Select Encounter Area",
#                        options=[discord.SelectOption(label=name, value=name) for name in
#                                 worlddex["Encounter Slots"].keys()], max_values=1)
#     async def select(self, interaction: discord.Interaction, select: discord.ui.Select):
#         self.enc_details["Area"] = select.values[0]
#         self.stop()
#
#     @discord.ui.select(custom_id="Number Players", placeholder="# Players",
#                        options=[discord.SelectOption(label=str(i+1), value=str(i+1)) for i in range(4)], max_values=1)
#     async def select(self, interaction: discord.Interaction, select: discord.ui.Select):
#         self.enc_details["Num Players"] = select.values[0]
#         self.stop()


# foo: bool = None

# async def disable_all_items(self):
#     for item in self.children:
#         item.disabled = True
#     await self.message.edit(view=self)
#
# async def on_timeout(self) -> None:
#     await self.message.channel.send("Timedout")
#     await self.disable_all_items()
#
# @discord.ui.button(label="Hello",
#                    style=discord.ButtonStyle.success)
# async def hello(self, interaction: discord.Interaction, button: discord.ui.Button):
#     await interaction.response.send_message("World")
#     self.foo = True
#     self.stop()
#
# @discord.ui.button(label="Cancel",
#                    style=discord.ButtonStyle.red)
# async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
#     await interaction.response.send_message("Cancelling")
#     self.foo = False
#     self.stop()
