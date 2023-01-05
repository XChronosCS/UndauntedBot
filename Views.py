import discord

from CollectData import worlddex


class SimpleView(discord.ui.View):
    enc_details = {}

    @discord.ui.Select(custom_id="Encounter Slots", placeholder="Select Encounter Area",
                       options=[discord.SelectOption(label=name, value=name) for name in
                                worlddex["Encounter Slots"].keys()], max_values=1, row=0)
    async def select(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.enc_details["Area"] = select.values[0]
        self.stop()

    @discord.ui.Select(custom_id="Number Players", placeholder="# Players",
                       options=[discord.SelectOption(i + 1) for i in range(4)], max_values=1, row=0)
    async def select(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.enc_details["Num Players"] = select.values[0]
        self.stop()

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
