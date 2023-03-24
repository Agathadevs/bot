import discord
from discord.ext import commands
import yt_dlp
import Cogs.music
import Cogs.lib


class Main_third(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        #all the music related stuff
        self.is_playing = False
        self.stop=True

        # 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None

    def search_yt(self,item):
        with yt_dlp.YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
                    
            except Exception: 
                return False
    
            return {'source': info['url'],
                    'title': info['title'],
                    "youtube_url":info['webpage_url'],
                    "duration":info["duration"]
                   }
    
    async def play_music(self, ctx,song_len,song_source):
        if len(self.music_queue) > 0:
            self.is_playing = True

            #try to connect to voice channel if you are not already connected
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()
                
                #in case we fail to connect
                if self.vc == None:
                    await ctx.send("Could not connect to the voice channel")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            #remove the first element as you are currently playing it
            msg=Cogs.music.music_embed(ctx,self.music_queue[0][0]['youtube_url'],song_len)
            embed=msg['Emb']
                
            await ctx.send(embed=embed)
            m_url=song_source
            player=discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS)
            self.vc.play(player,after=lambda e:self.play_music(ctx,song_len,song_source) )
            self.music_queue.pop(0)
            
        else:
            self.is_playing = False
        
    @commands.command(name='play')
    async def play(self,ctx,*args):
        
        query = " ".join(args)
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            #you need to be connected so that the bot knows where to go
            await ctx.send("❎ | 請連接至語音頻道")
        else:
            song =self.search_yt(query)
            
            if type(song) == type(True):
                await ctx.send("無法下載歌曲。 格式不正確請嘗試其他關鍵字。")
            else:
                self.music_queue.append([song,voice_channel])
                songlen=len(self.music_queue)
                if self.is_playing == False:
                    await ctx.send("✅ | 歌已加入清單!")
                    
                    await self.play_music(ctx,songlen,song["source"])
    @commands.command(name="music")  
    async def music(self,ctx):
        embed=discord.Embed(title="以下為音樂下統指令列表:",
                            color=discord.Color.blue()
                            ).set_author(name='ChickenBot的指令列表',icon_url='https://i.pinimg.com/originals/54/73/1e/54731e74a0752206c1df5e6ccf21531d.jpg'
                            ).add_field(name="`>play`",value="**撥放音樂**",inline=False
                            ).add_field(name="`>queue`",value="**歌曲清單**",inline=False)
        await ctx.send(embed=embed)
        