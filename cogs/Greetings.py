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
import mysql.connector
from mysql.connector import Error

load_dotenv()


SERVERID = os.getenv("SERVERID")

class Greetings(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Greetings.py is ready!")
    
    @app_commands.command(name="hello", description="Bot says hello")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello, I am the tutorial bot. How are you, " + str(interaction.user) + "?")

    @commands.Cog.listener()
    async def on_member_join(self, member:discord.Member=None):
        name = member.name
        pic = member.display_avatar.url
        memberId = member.id
        joined = member.joined_at.date()

        print(member)
        print(name)
        print(memberId)
        print(joined)


        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database = 'tutorial_bot',
                                                 user = 'root',
                                                 password = 'root')
            
            mySql_Create_Table_Query = """CREATE TABLE Users (
                                        Id int NOT NULL,
                                        User varchar(250) NOT NULL,
                                        Joinedat datetime,
                                        PRIMARY KEY(Id)) """
            
            cursor = connection.cursor()
            result = cursor.execute(mySql_Create_Table_Query)
            print("User Table created successfully")

        except mysql.connector.Error as error:
            print("Failed to create table in MySQL: {}".format(error))
        
        finally:
            if connection.is_connected():


                mySql_Insert_Row_Query = "INSERT INTO Users (Id, User) VALUES ({memberId}, {member})"

                cursor.execute(mySql_Insert_Row_Query)
                connection.commit()

                cursor.close()
                connection.close()
                print("Mysql connection has been closed")

        
        embed = discord.Embed(
            color=discord.Color.blurple(),
            title="Welcome to the Server!", 
            description=f"I hope you enjoy your stay {name}!"    
        )
        embed.set_image(url="https://i.pinimg.com/originals/ec/9a/42/ec9a42641385d573d3d066bb7d215e88.png")
        embed.set_thumbnail(url=pic)

        await member.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):   
        channel = self.client.get_channel(1087507058070401158)
        await channel.send('Have a good day ' + member.name + '!')

async def setup(client):
    await client.add_cog(Greetings(client), guilds=[discord.Object(id=SERVERID)])
