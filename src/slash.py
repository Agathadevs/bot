import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
class slash(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    @app_commands.command(name="say",description="讓機器人說話")
    async def test_command(self,interaction:discord.Interaction,description:str):
        await interaction.response.send_message(f"{description}")

    @app_commands.command(name="avatar",description="查看頭像")
    async def avatar(self,interaction:discord.Interaction,member:Optional[discord.Member]=None):
        avatar = member.display_avatar
        embed = discord.Embed(title="頭貼",
                              description=f"{member.mention}的頭貼",
                              color=discord.colour.Color.blue()).set_image(url=avatar)
        await interaction.response.send_message(embed=embed)
    @app_commands.command(name="help",description="指令列表")
    async def help(self,interaction:discord.Interaction,member:Optional[discord.Member]=None):
        HELP_LIST={}
        

async def setup(bot):
    await bot.add_cog(slash(bot))   
    
    

