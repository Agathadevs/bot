import discord
from discord.ext import commands
import yt_dlp
from ebs import lib
from ebs import embed
import time
class Main_third(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.stop=True
        self.is_paused = False
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
    
    async def play_next(self,ctx,url,song_len):
            if len(self.music_queue) > 0:
                self.is_playing = True

                #get the first url
                m_url = self.music_queue[0][0]['source']

                
                self.music_queue.pop(0)
                msg=embed.music_embed(ctx,url,song_len)
                emb=msg['Emb']
                await ctx.send(embed=emb)
                try:
                    await self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e:  self.play_next(ctx,url,song_len))
                except Exception as error:
                    print(f"發生錯誤  {error}")
            else:
                self.is_playing = False

    # infinite loop checking 
    async def play_music(self,ctx,url,song_len):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
            
            #try to connect to voice channel if you are not already connected

            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                #in case we fail to connect
                if self.vc == None:
                    await ctx.send("Could not connect to the voice channel")
                    return
            
            print(self.music_queue)
            #remove the first element as you are currently playing it
            self.music_queue.pop(0)
            try:
                self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx,url,song_len))
            except Exception as error:
                print(f" 發生錯誤  {error}")
        else:
            self.is_playing = False
    
    @commands.command(name="play", help="Plays a selected song from youtube")
    async def p(self, ctx, *args):
        query = " ".join(args)
        
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            #you need to be connected so that the bot knows where to go
            await ctx.send("☑️| 成功連結至頻道")
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.")
            else:
                await ctx.send("歌曲已加入撥放清單")
                self.music_queue.append([song, voice_channel])
                song_len=len(self.music_queue)
                if self.is_playing == False:
                    await self.play_music(ctx,song['youtube_url'],song_len)
                    
                    msg=embed.music_embed(ctx,song['youtube_url'],song_len)
                    emb=msg['Emb']
                    await ctx.send(embed=emb)

    @commands.command(name="queue", help="Displays the current songs in queue")
    async def q(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += self.music_queue[i][0]['title'] + "\n"

        print(retval)
        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue")

    @commands.command(name="skip", help="Skips the current song being played")
    async def skip(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            #try to play next in the queue if it exists
            await self.play_music()
                

async def setup(bot):
    await bot.add_cog(Main_third(bot))
   
   
   
   
    
        