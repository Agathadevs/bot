import discord
from discord.ext import commands
from discord import app_commands


class ButtonHandler(discord.ui.View):
    @discord.ui.button(label="A",
                       style=discord.ButtonStyle.primary)
    async def buttonA(self,
                      interaction:discord.Interaction,
                      button:discord.ui.Button):
        await interaction.response.edit_message(content="你選擇了A")
    @discord.ui.button(label="B",
                       style=discord.ButtonStyle.primary)
    async def buttonB(self,
                      interaction:discord.Interaction,
                      button:discord.ui.Button):
        await interaction.response.edit_message(content="你選擇了B")
class quiz(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot=bot
    @app_commands.command(name="quiz",description="start a quiz")
    async def quiz(self , interaction:discord.Interaction):
        view=ButtonHandler()
        await interaction.response.send_message(f"開始考試",view=view)
async def setup(bot:commands.Bot):
    await bot.add_cog(quiz(bot))