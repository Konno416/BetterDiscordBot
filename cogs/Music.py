import discord
from discord import app_commands
from discord.ext import commands
from discord import *
from discord.ext.commands import has_permissions, MissingPermissions
import os
from dotenv import load_dotenv
import wavelink

load_dotenv()

SERVERID = os.getenv("SERVERID")

class Music(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Music.py is ready")

    @commands.command()
    async def sync(self, ctx) -> None:
        fmt = await self.client.tree.sync(guild=ctx.guild)

        await ctx.send(f"Synced {len(fmt)} commands.")


    #Plays the music
    @app_commands.command(name="play", description="Plays the song requested")
    async def play(self, interaction: discord.Interaction, search: str):

        query = await wavelink.YouTubeTrack.search(search, return_first=True)
        destination = interaction.user.voice.channel

        if not interaction.guild.voice_client:

            vc: wavelink.Player = await destination.connect(cls=wavelink.Player)
        else:

            vc: wavelink.Player = interaction.guild.voice_client

        if vc.queue.is_empty and not vc.is_playing():

            await vc.play(query)
            await interaction.response.send_message(f'Now Playing {vc.current.title}')
        else:
            await vc.queue.put_wait(query)
            await interaction.response.send_message(f'Song was added to the queue')


    #Skips the current song
    @app_commands.command(name="skip", description="Skips the currently playing song")
    async def skip(self, interaction: discord.Interaction):
        vc: wavelink.Player = interaction.guild.voice_client
        await vc.stop()
        await interaction.response.send_message(f'Song was skipped!')


    #Pauses the current song
    @app_commands.command(name="pause", description="Pauses the current song that is playing")
    async def pause(self, interaction: discord.Interaction):
        vc: wavelink.Player = interaction.guild.voice_client

        if vc.is_playing():
            await vc.pause()
            await interaction.response.send_message(f'Song was paused! :smile:')
        else:
            await interaction.response.send_message(f'Song is already paused!')


    #Resumes the song
    @app_commands.command(name="resume", description="Resumes the current song")
    async def resume(self, interaction: discord.Interaction):
        vc: wavelink.Player = interaction.guild.voice_client

        if not vc.is_paused():

            await interaction.response.send_message(f'Song is already resumed! :smile:')
        else:
            await vc.resume()
            await interaction.response.send_message(f'Song is now resumed!')


    #Disconnects the bot from the Voice Channel
    @app_commands.command(name="disconnect", description="Disconnects the bot")
    async def disconnect(self, interaction: discord.Interaction):

        vc: wavelink.Player = interaction.guild.voice_client
        await vc.disconnect()
        await interaction.response.send_message(f'The bot was disconnected!')


    #Shows the list of of songs currently in the queue
    @app_commands.command(name="queue", description="Shows the current songs in the queue")
    async def queue(self, interaction: discord.Interaction):

        vc: wavelink.Player = interaction.guild.voice_client

        if not vc.queue.is_empty:

            song_counter = 0
            songs = []
            queue = vc.queue.copy()
            embed = discord.Embed(title="Queue")

            for song in queue:
                song_counter += 1
                songs.append(song)
                embed.add_field(name=f"[{song_counter}] Duration {song.duration}", value=f"{song.title}", inline=False)

            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("The queue is empty!")


    #This shows the current song playing
    @app_commands.command(name="current", description="Shows the current song")
    async def current(self, interaction: discord.Interaction):

        vc: wavelink.Player = interaction.guild.voice_client

        if vc.is_playing():
            await interaction.response.send_message(f'The current song is {vc.current.title} by {vc.current.author}')

        else:
            await interaction.response.send_message(f"The player is not currently playing anything!")



async def setup(client):
    await client.add_cog(Music(client), guilds=[discord.Object(id=SERVERID)])
    