import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord import member
from discord import *
from discord.ext.commands import has_permissions, MissingPermissions
import json
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import datetime
from discord.utils import get


load_dotenv()
list1 = ["name1", "name2", "name3"]

embedId = 0
embedCopy = 0

SERVERID = os.getenv("SERVERID")

# class SimpleView(discord.ui.View):
#     foo : bool = None

#     async def disable_all_items(self):
#         for item in self.children:
#             item.disabled = True
#         await self.message.edit(view=self)


#     async def on_timeout(self) -> None:
#         await self.message.channel.send("Timed Out")
#         await self.disable_all_items()

#     @discord.ui.button(label="Hello",
#                        style=discord.ButtonStyle.success)
#     async def hello(self, interaction: discord.Interaction, button: discord.ui.Button):
#             await interaction.response.send_message("World")
#             self.foo = True
#             self.stop()
    
#     @discord.ui.button(label="Cancel",
#                        style=discord.ButtonStyle.red)
#     async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
#             await interaction.response.send_message("Cancelling")
#             self.foo = False
#             self.stop()


# class PollView(discord.ui.View):
#     def __init__(self):
#         super().__init__(timeout=None)
     
#     @discord.ui.button(label="1", style=discord.ButtonStyle.primary)
#     async def addOne(self, interaction: discord.Interaction, button: discord.ui.Button):
#         user = interaction.user

        
        

        
    

class Poll(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Poll.py is ready!")
        print("-------------------")

    # @commands.command()
    # @has_permissions(manage_guild=True)
    # async def create_poll()

    # @app_commands.command(name="poll", description="Testing poll")
    # @has_permissions(manage_guild=True)
    # async def poll(self, interaction: discord.Interaction, question: str, choiceone: str, choicetwo: str):

    #     creatorpic = interaction.user.avatar.url
    #     creatorname = interaction.user.name
        
    #     embed = discord.Embed(  
    #         color=discord.Color.dark_teal(),
    #         title="Poll",
    #         description=question,
    #         timestamp=datetime.datetime.now(datetime.timezone.utc)
    #     )
    #     embed.add_field(name=choiceone, value=":one:") 
    #     embed.add_field(name=choicetwo, value=":two:")
    #     embed.set_footer(text=creatorname)
    #     await interaction.response.send_message(embed=embed)

    #     message: discord.Message
    #     async for message in interaction.channel.history():
    #         if not message.embeds:
    #             continue
    #         if message.embeds[0].title == embed.title and message.embeds[0].colour == embed.colour:
    #             vote = message
    #             break
    #     else:
    #         # something broke
    #         return

    #     await vote.add_reaction("<:yes:914969003645091900>")
    #     await vote.add_reaction("<:no:914969105482809355>")



    # @commands.command()
    # async def button(self, ctx):
    #     view = SimpleView(timeout=50)
    #     # button = discord.ui.Button(label="Click me")
    #     # view.add_item(button)
        
    #     message = await ctx.send(view=view)
    #     view.message = message

    #     await view.wait()
    #     await view.disable_all_items()

    #     if view.foo is None:
    #          print("timeout")
    #     elif view.foo is True:
    #          print("Ok")
    #     else:
    #          print("Cancel")


async def setup(client):
    await client.add_cog(Poll(client), guilds=[discord.Object(id=SERVERID)])