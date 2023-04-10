import discord
from discord.ext import commands
import yt_dlp
import lib
import embed
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
    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            #get the first url
            m_url = self.music_queue[0][0]['source']

            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    # infinite loop checking 
    async def play_music(self,ctx,song_len,song_source):
        if len(self.music_queue) > 0:
            self.is_playing=True
            m_url = self.music_queue[0][0]['source']
            
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
            msg=embed.music_embed(ctx,self.music_queue[0][0]['youtube_url'],song_len)
            embed=msg['Emb']
                
            await ctx.send(embed=embed)
            m_url=song_source
            self.music_queue.pop(0)    
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx,song_len,song_source))
            self.is_playing==True
        else:
            self.is_playing = False

    @commands.command(name="play", aliases=["p","playing"], help="Plays a selected song from youtube")
    async def play(self, ctx, *args):
        query = " ".join(args)
        
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            #you need to be connected so that the bot knows where to go
            await ctx.send("Connect to a voice channel!")
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.")
            else:
                await ctx.send("Song added to the queue")
                self.music_queue.append([song, voice_channel])
                songlen=len(self.music_queue)
                if self.is_playing == False:
                    await self.play_music(ctx,songlen,song["source"])
                    msg=embed.music_embed(ctx,self.music_queue[0][0]['youtube_url'],songlen)
                    embed=msg['Emb']
                    await ctx.send(embed=embed)
                

async def setup(bot):
    await bot.add_cog(Main_third(bot))
   
   
   
    
        