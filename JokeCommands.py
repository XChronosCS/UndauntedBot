import random

import discord


def piglatinify(key, sentence):
    def strip_consonants(word):
        word_lower = word.lower()
        stripped = ""
        for i, c in enumerate(word_lower):
            if c in 'aeiou':
                stripped = word[i:]
                break
        return stripped

    addition = strip_consonants(key)

    def piglatin(word):
        stripped = strip_consonants(word)
        if len(stripped) > 0:
            return stripped + word[:len(word) - len(stripped)] + addition
        else:
            return word + "w" + addition

    words = sentence.split()
    piglatin_words = []
    for i, word in enumerate(words):
        if word[-1] in '.!?':
            piglatin_words.append(piglatin(word[:-1]) + word[-1])
        else:
            piglatin_words.append(piglatin(word))
    return " ".join(piglatin_words).capitalize()

class MuffinButton(discord.ui.View):
    @discord.ui.button(label="Push for Muffin",
                       style=discord.ButtonStyle.success, row=3)
    async def submit(self, interaction: discord.Interaction, button: discord.ui.Button):
        muf_var = random.randint(1, 4)
        await interaction.response.send_message(file=discord.File('Images/muffin_{0}.png'.format(muf_var)),
                                                ephemeral=True)


class BunnyButton(discord.ui.View):
    @discord.ui.button(label="Push for Bunny",
                       style=discord.ButtonStyle.success, row=3)
    async def submit(self, interaction: discord.Interaction, button: discord.ui.Button):
        bun_var = random.randint(1, 40)
        await interaction.response.send_message(
            file=discord.File('Images/Bunny Pictures/bunny_{0}.png'.format(bun_var)), ephemeral=True)