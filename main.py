import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord import member
from discord import *
from discord.ext.commands import has_permissions, MissingPermissions
import requests
import json
import wavelink
import os
from dotenv import load_dotenv

load_dotenv()

#import Bot Token
botToken = str(os.getenv("BOTTOKEN"))


profane = {'shit', 'piss', 'ass', 'cum', 'shit', 'dick'}


client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@client.event
async def on_ready():
    client.loop.create_task(on_node())
    await client.tree.sync()
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('What the dog doing?'))
    print("The bot is now ready for use!")
    print("------------------------------")

async def on_node():

    node: wavelink.Node = wavelink.Node(uri="http://lavalink.clxud.pro:2333", password="youshallnotpass")
    await wavelink.NodePool.connect(client=client, nodes=[node])
    wavelink.Player.autoplay = True

    
@client.tree.command(name="play", description="Plays the song requested")
async def play(interaction: discord.Interaction, search: str):

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


@client.tree.command(name="skip", description="Skips the currently playing song")
async def skip(interaction: discord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client
    await vc.stop()
    await interaction.response.send_message(f'Song was skipped!')


@client.tree.command(name="pause", description="Pauses the current song that is playing")
async def pause(interaction: discord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client

    if vc.is_playing():
        await vc.pause()
        await interaction.response.send_message(f'Song was paused! :smile:')
    else:
        await interaction.response.send_message(f'Song is already paused!')


@client.tree.command(name="resume", description="Resumes the current song")
async def resume(interaction: discord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client

    if not vc.is_paused():

        await interaction.response.send_message(f'Song is already resumed! :smile:')
    else:
        await vc.resume()
        await interaction.response.send_message(f'Song is now resumed!')


@client.tree.command(name="disconnect", description="Disconnects the bot")
async def disconnect(interaction: discord.Interaction):

    vc: wavelink.Player = interaction.guild.voice_client
    await vc.disconnect()
    await interaction.response.send_message(f'The bot was disconnected!')


@client.tree.command(name="queue", description="Shows the current songs in the queue")
async def queue(interaction: discord.Interaction):

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


@client.tree.command(name="current", description="Shows the current song")
async def current(interaction: discord.Interaction):

    vc: wavelink.Player = interaction.guild.voice_client

    if vc.is_playing():
        await interaction.response.send_message(f'The current song is {vc.current.title} by {vc.current.author}')

    else:
        await interaction.response.send_message(f"The player is not currently playing anything!")


# -----------------------------------------------------------------------------









@client.tree.command(name="hello", description="Bot says hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello, I am the tutorial bot. How are you, " + str(interaction.user) + "?")

@client.event
async def on_member_join(member):
    channel = client.get_channel(1087507058070401158)
    await channel.send('Welcome to the server ' + member.name + '!')

@client.event
async def on_member_remove(member):
    channel = client.get_channel(1087507058070401158)
    await channel.send('Have a good day ' + member.name + '!')


@client.command(pass_context = True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


@client.event
async def on_message(message):
    for i in profane:
        words = message.content.split()
        for x in words:
            if x == i:
                await message.delete()
                await user.send("Don't type that again or else!")
                await user.send("https://www.ilcovodelnerd.com/wp-content/uploads/2023/03/88257.png")
    await client.process_commands(message)


@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has been kicked')

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to kick people!")


@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'User {member} has been banned')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to kick people!")


# @client.event()
# async def on_command_error(interaction: discord.Interaction, error):
#     if isinstance(error, commands.MissingPermissions):
#         await interaction.response.send_message("You don't ahve permission to run this command")
    




client.run(botToken)

