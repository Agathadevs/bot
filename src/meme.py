import discord
from discord.ext import commands
import urllib.request as req
import json
from datetime import datetime
import random
import urllib.request as req

url='https://memes.tw/wtf/api'
request=req.Request(url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})

with req.urlopen(request) as re:
    data=json.load(re)
    
class Main_second(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        
    @commands.command()
    async def meme(self,ctx):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        memeData=data
        meme=random.choice(memeData)
        memeurl=meme["src"]
        memename=meme["title"]
        memeposter=meme['author']["name"]
        memesrc=meme["url"]
        memelike=meme["total_like_count"]
        view=meme['pageview']
        embed=discord.Embed(title=memename,colour=discord.Color.blue(),url=f"{memesrc}")
        embed.set_image(url=memeurl)
        embed.set_footer(text=f"作者: {memeposter} | 👍:{memelike} | 👀:{view} • 時間:{now}  ")
        await ctx.send(embed=embed)
async def setup(bot):
    await bot.add_cog(Main_second(bot))