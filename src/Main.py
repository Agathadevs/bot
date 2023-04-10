import discord
from discord.ext import commands
from discord import app_commands


class Main(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game('im online'))
        print('is online')
    @commands.command()
    async def ping(self,ctx):
        await ctx.send(f"{round(self.bot.latency*1000)} (ms)")
    @commands.Cog.listener()
    async def on_message(self,msg):
        if msg.content=="嗨":
            await msg.channel.send("嗨OwO")
    
        if msg.content=="?":
            await msg.channel.send("蝦?")
    
        if msg.content=="沒事":
            await msg.channel.send("好窩owo")
async def setup(bot):
    await bot.add_cog(Main(bot))