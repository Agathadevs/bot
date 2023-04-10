import json
import discord
from discord.ext import commands
import os


bot=commands.Bot(command_prefix='>',intents=discord.Intents.all(),help_command=None)



@bot.command(name="set_welcome")
async def set_welcome(ctx,channel:discord.TextChannel):
    with open("./Discord.py-Bot/database/channel.json",mode="r") as file:
        data=json.load(file)
    data["welcome"][str(ctx.guild.id)]=channel.id
    new_data=json.dumps(data)
    with open("./Discord.py-Bot/database/channel.json","w") as file:
        file.write(new_data)
    await ctx.send("資料更新成功")

@bot.command(name="set_leave")
async def set_leave(ctx,channel:discord.TextChannel):
    with open("./Discord.py-Bot/database/channel.json",mode="r") as file:
        data=json.load(file)
    data["leave"][str(ctx.guild.id)]=channel.id
    new_data=json.dumps(data)
    with open("./Discord.py-Bot/database/channel.json","w") as file:
        file.write(new_data)
    await ctx.send("資料更新成功")

@bot.event
async def on_member_join(member):
    with open("./Discord.py-Bot/database/channel.json","r") as file:
        data=json.load(file)
    if str(member.guild.id) in data:
        channel=bot.get_channel(data["welcome"][str(member.guild.id)])
        embed=discord.Embed(description=f"{member.mention} 已加入",color=discord.Colour.blue())
        await channel.send(embed=embed)
        
@bot.event
async def on_member_remove(member):
    with open("./Discord.py-Bot/database/channel.json","r") as file:
        data=json.load(file)
    if str(member.guild.id) in data:
        channel=bot.get_channel(data["leave"][str(member.guild.id)])
        embed=discord.Embed(description=f"{member.mention} 離開",color=discord.Colour.blue())
        await channel.send(embed=embed)
async def load_extensions():
    for filename in os.listdir("./Discord.py-Bot/src"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"src.{filename[:-3]}")
                print(f"✅   已加載 {filename}")
            except Exception as error:
                print(f"❎   {filename} 發生錯誤  {error}")
    for filename in os.listdir("./Discord.py-Bot/src/music"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"src.music.{filename[:-3]}")
                print(f"✅   已加載 {filename}")
            except Exception as error:
                print(f"❎   {filename} 發生錯誤  {error}")


@bot.event
async def on_ready():
    await load_extensions()
    print("Bot is online")
    try:
        synced=await bot.tree.sync()
        print(f"synced {len(synced)}command(s)")
    except Exception as e:
        print(e)
with open("./Discord.py-Bot/database/token.json","r")  as file:
    data=json.load(file)
bot.run(data["TOKEN"])
    







