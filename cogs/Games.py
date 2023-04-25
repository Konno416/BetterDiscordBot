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

load_dotenv()


SERVERID = os.getenv("SERVERID")

class Games(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Games.py is ready!")


async def setup(client):
    await client.add_cog(Games(client), guilds=[discord.Object(id=SERVERID)])
