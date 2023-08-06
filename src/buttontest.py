import discord
from discord.ext import commands
from discord import app_commands


class ButtonHandler(discord.ui.View):
    @discord.ui.button(label="",
                       style=discord.ButtonStyle.primary)
    async def buttonA(self,
                      interaction:discord.Interaction,
                      button:discord.ui.Button):
        await interaction.response.edit_message(content="")
    @discord.ui.button(label="",
                       style=discord.ButtonStyle.primary)
    async def buttonB(self,
                      interaction:discord.Interaction,
                      button:discord.ui.Button):
        await interaction.response.edit_message(content="")
class quiz(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot=bot
    @app_commands.command(name="quiz",description="")
    async def quiz(self , interaction:discord.Interaction):
        view=ButtonHandler()
        await interaction.response.send_message(f"",view=view)
async def setup(bot:commands.Bot):
    await bot.add_cog(quiz(bot))
