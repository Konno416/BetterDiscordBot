import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord import member
from discord import *
from discord.ext.commands import has_permissions, MissingPermissions
import requests
import json
import os
from dotenv import load_dotenv
import wavelink

load_dotenv()

SERVERID = os.getenv("SERVERID")

#Have to make your own profane list in an array in the env file.
profane = os.getenv("PROFANE")

class Admin(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Admin.py is ready!")

    @commands.Cog.listener()
    async def on_message(self, message):
        for i in profane:
            words = message.content.split()
        for x in words:
            if x == i:
                await message.delete()
                await user.send("Don't type that again or else!")
                await user.send("https://www.ilcovodelnerd.com/wp-content/uploads/2023/03/88257.png")
        await self.client.process_commands(message)


    @commands.command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'User {member} has been kicked')

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to kick people!")


    @commands.command()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'User {member} has been banned')

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to kick people!")


    # @client.event()
    # async def on_command_error(interaction: discord.Interaction, error):
    #     if isinstance(error, commands.MissingPermissions):
    #         await interaction.response.send_message("You don't ahve permission to run this command")
    
    

async def setup(client):
    await client.add_cog(Admin(client), guilds=[discord.Object(id=SERVERID)])