import json
import discord
from discord.ext import commands
from Cogs.Main import Main
from Cogs.meme import Main_second
from Cogs.playmusic import Main_third
from Cogs.slash import slash


bot=commands.Bot(command_prefix='>',intents=discord.Intents.all(),help_command=None)
@bot.command(name='help')
async def help(ctx):
    
    embed=discord.Embed(
        title='指令:',
        color=discord.Color.blue()
    )
    embed.add_field(name='`>ping`',value='**查看延遲**',inline=False)
    embed.add_field(name='`>meme`',value='**梗圖**',inline=False)
    embed.add_field(name='`>music`',value='**查看音樂系統的各項指令**')
    embed.set_author(name='ChickenBot的指令列表',icon_url='https://i.pinimg.com/originals/54/73/1e/54731e74a0752206c1df5e6ccf21531d.jpg')    
    await ctx.send(embed=embed)


@bot.command(name="set_welcome")
async def set_welcome(ctx,channel:discord.TextChannel):
    with open("welcome.json",mode="r") as file:
        data=json.load(file)
    data[str(ctx.guild.id)]=channel.id
    new_data=json.dumps(data)
    with open("welcome.json","w") as file:
        file.write(new_data)
    await ctx.send("資料更新成功")

@bot.command(name="set_leave")
async def set_leave(ctx,channel:discord.TextChannel):
    with open("leave.json",mode="r") as file:
        data=json.load(file)
    data[str(ctx.guild.id)]=channel.id
    new_data=json.dumps(data)
    with open("leave.json","w") as file:
        file.write(new_data)
    await ctx.send("資料更新成功")

@bot.event
async def on_member_join(member):
    with open("leave.json","r") as file:
        data=json.load(file)
    if str(member.guild.id) in data:
        channel=bot.get_channel(data[str(member.guild.id)])
        embed=discord.Embed(description=f"{member.mention} 已加入",color=discord.Colour.blue())
        await channel.send(embed=embed)
        
@bot.event
async def on_member_remove(member):
    with open("leave.json","r") as file:
        data=json.load(file)
    if str(member.guild.id) in data:
        channel=bot.get_channel(data[str(member.guild.id)])
        embed=discord.Embed(description=f"{member.mention} 離開",color=discord.Colour.blue())
        await channel.send(embed=embed)



@bot.event
async def on_ready():
    print("Bot is online")
    await bot.add_cog(Main_second(bot))
    await bot.add_cog(Main_third(bot))
    await bot.add_cog(Main(bot))
    await bot.add_cog(slash(bot))
    try:
        synced=await bot.tree.sync()
        print(f"synced {len(synced)}command(s)")
    except Exception as e:
        print(e)
    
    

    
    
bot.run('MTA4NjYzNDQ0ODA5MjY2Mzg5OA.GfTddu._bNxlTVK6aB08sN5qUhTiQbXG0DfrqHeLCc94g')





