import discord
from discord.ext import commands
from discord import app_commands
from discord import member
from discord import *
import asyncio
import json
import os
from dotenv import load_dotenv
import wavelink

load_dotenv()

#import Bot Token
botToken = str(os.getenv("BOTTOKEN"))


client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@client.event
async def on_ready():
    client.loop.create_task(on_node())
    print("The bot is now ready for use!")
    print("------------------------------")

async def on_node():
    node: wavelink.Node = wavelink.Node(uri="http://localhost:2333", password="youshallnotpass")
    await wavelink.NodePool.connect(client=client, nodes=[node])
    print(node)
    wavelink.Player.autoplay = True

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")
            print(f"{filename[:-3]} is loaded!")

async def main():
    async with client:
        await load()
        await client.start(botToken)


asyncio.run(main())

