import discord
from datetime import datetime
import playmusic
import lib

def music_embed(ctx,youtube_url,song_len) :
    user = ctx.message.author
    avatar = user.display_avatar
    name = ctx.author.name
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    data=lib.music_info(youtube_url)
    embed=discord.Embed(title=f'{data["title"]}',url=f'{data["url"]}',color=discord.Color.red())
    embed.add_field(name="時間:",value=f"> {data['Time']}")
    embed.add_field(name="歌單:",value=f'> {song_len} 首歌')
    embed.set_footer(text=f'Requested By · {name} · {now}',icon_url=F"{avatar}")
    embed.set_thumbnail(url= data["thumbnail"])
    embed.set_author(name="💿播放音樂中!")
    return{"Emb":embed,"URL":data['source'],"duration":data["duration"]}