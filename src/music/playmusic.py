import discord
from discord.ext import commands
from ebs import lib
from ebs import embed
import yt_dlp
import asyncio
class Main_third(commands.Cog):
    '''
    init setting
    '''
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

    async def play_next(self,ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            song_len=len(self.music_queue)
            url=self.music_queue[0][0]["youtube_url"]
            msg=embed.music_embed(ctx,url,song_len)
            emb=msg['Emb']
            await ctx.send(embed=emb)
            m_url = self.music_queue[0][0]['source']
            self.music_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e:  asyncio.ensure_future(self.play_next(ctx)))
                
        else:
            self.is_playing = False
        
   
    async def play_music(self,ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
         
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                if self.vc == None:
                    await ctx.send("Could not connect to the voice channel")
                    return
            
            song_len=len(self.music_queue)
            url=self.music_queue[0][0]["youtube_url"]
            msg=embed.music_embed(ctx,url,song_len)
            emb=msg['Emb']
            await ctx.send(embed=emb)

            async with ctx.typing():
                await asyncio.sleep(1)

            if self.vc.is_playing():
                 self.vc.stop()

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop).result())
            self.music_queue.pop(0)
        else:

            self.is_playing = False

    @commands.command(name="play", help="Plays a selected song from youtube")
    async def p(self, ctx, *args):
        query = " ".join(args)
        
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
    
            await ctx.send("Connect to a voice channel!")
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.")
            else:
                await ctx.send("Song added to the queue")
                self.music_queue.append([song, voice_channel])
                
                if self.is_playing == False:
                    await self.play_music(ctx)

    @commands.command(name="queue", help="Displays the current songs in queue")
    async def q(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += self.music_queue[i][0]['title'] + "\n"
       
        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue")

    @commands.command(name="skip", help="Skips the current song being played")
    async def skip(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            await self.play_music()
            
    @commands.command(name="disconnect", help="Disconnecting bot from VC")
    async def dc(self, ctx):
        await self.vc.disconnect()
async def setup(bot):
    await bot.add_cog(Main_third(bot))  
