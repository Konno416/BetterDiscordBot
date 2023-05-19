import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord import member
from discord import *
from discord.ext.commands import has_permissions, MissingPermissions
import json
import os
import random
import giphy_client
from giphy_client.rest import ApiException
from dotenv import load_dotenv

load_dotenv()

apitoken = str(os.getenv("GIFAPIKEY"))

punch_gifs = ["https://media.tenor.com/BoYBoopIkBcAAAAC/anime-smash.gif", "https://gifdb.com/images/high/anime-fight-funny-punch-s4n15b8fw49plyhd.gif"
              , "https://media.tenor.com/44IcPjhMv5oAAAAd/punch-anime.gif", "https://i.pinimg.com/originals/e1/63/ff/e163ff743644a8250d4f07112b8ddb08.gif"
              , "https://media.tenor.com/6a42QlkVsCEAAAAd/anime-punch.gif", "https://img.wattpad.com/43358585b815432050002a5458087fa19e6c86ef/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f776174747061642d6d656469612d736572766963652f53746f7279496d6167652f4856594c434d57516b6a504d65413d3d2d3938383431343736312e313634626631343038306561313765613131333530353931313336362e676966"
              , "https://64.media.tumblr.com/2b908ad159837f7b49037849831f82f5/tumblr_pxw6vjfvXE1vg0r9to1_540.gif"]

kick_gifs = ["https://i.pinimg.com/originals/4f/90/40/4f9040a91c1a888a9e0ff2f02f2a64fc.gif", "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/efad94cd-d200-4d9f-a4d3-c558b53f884c/d9osa0j-372bb442-c31f-495c-9b33-59dce7685903.gif?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcL2VmYWQ5NGNkLWQyMDAtNGQ5Zi1hNGQzLWM1NThiNTNmODg0Y1wvZDlvc2Ewai0zNzJiYjQ0Mi1jMzFmLTQ5NWMtOWIzMy01OWRjZTc2ODU5MDMuZ2lmIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.NvEj3ixv5wHizYZ-3f_W0AVW3ay-v9dEvAuv6YmRJ8w"
             , "https://i.pinimg.com/originals/44/6f/49/446f49e675e38e1bb10d226f12519092.gif", "https://64.media.tumblr.com/1ae35cc7d78b5e579d5baabe3f0c03db/93cab037caf29e98-82/s540x810/00a2d481867ccd79d1302aced86271584594dae9.gif"
             , "https://media.tenor.com/Lyqfq7_vJnsAAAAC/kick-funny.gif", "https://media.tenor.com/4zwRLrLMGm8AAAAC/chifuyu-chifuyu-kick.gif", "https://media.tenor.com/IlaJyD0XEMwAAAAC/index-anime.gif"
             , "https://media.tenor.com/4F6aGlGwyrwAAAAd/sdf-avatar.gif"]


SERVERID = os.getenv("SERVERID")

class Media(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Media.py is ready!")
    
    @app_commands.command(name="punch", description="Punches the person you mention")
    async def punch_user(self, interaction: discord.Interaction, user: discord.Member):
        pic = self.client.user.display_avatar.url
        
        embed = discord.Embed(
            color=discord.Color.blurple(),
            title=f"Anime Gifs",
            description=f"{interaction.user.mention} punches {user.mention}!"    
        )
        embed.set_image(url=random.choice(punch_gifs))
        embed.set_thumbnail(url=pic)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="kick", description="Kicks the person you mention")
    async def kick_user(self, interaction: discord.Interaction, user: discord.Member):
        pic = self.client.user.display_avatar.url
        
        embed = discord.Embed(
            color=discord.Color.blurple(),
            title=f"Anime Gifs",
            description=f"{interaction.user.mention} kicks {user.mention}!"    
        )
        embed.set_image(url=random.choice(kick_gifs))
        embed.set_thumbnail(url=pic)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="gif", description="Gives a gif of your choosing or random")
    async def gif(self, interaction: discord.Interaction, search: str):

        api_key = apitoken
        api_instance = giphy_client.DefaultApi()

        try:

            api_response = api_instance.gifs_search_get(api_key, search, limit=5, rating='pg-13')
            lst = list(api_response.data)
            giff = random.choice(lst)
            
            await interaction.response.send_message(giff.embed_url)
        
        except ApiException as e:
            print("Exception when calling Api")


async def setup(client):
    await client.add_cog(Media(client), guilds=[discord.Object(id=SERVERID)])
