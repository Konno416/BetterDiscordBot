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
import mysql.connector
from mysql.connector import Error

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

    
    @app_commands.command(name="clear", description="Should clear the amount of messages inputed or just typing all should delete everything")
    @has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount:str):
        await interaction.channel.purge(limit=(int(amount) + 1))
        print('ran')
        

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

    @app_commands.command(name="store_info", description="Test for storing data")
    async def store_info(self, interaction: discord.Interaction, message: str):
        
        guild = interaction.guild.id

        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database = 'tutorial_bot',
                                                 user = 'root',
                                                 password = 'root')
            
            mySql_Create_Table_Query = """CREATE TABLE DB_""" + str(guild) + """ (
                                        Id int(11) NOT NULL AUTO_INCREMENT,
                                        User varchar(250) NOT NULL,
                                        Message varchar(5000) NOT NULL,
                                        PRIMARY KEY(Id)) """    
            
            cursor = connection.cursor()
            result = cursor.execute(mySql_Create_Table_Query)
            print("Guild (" + str(guild) + ") Table created successfully")

        except mysql.connector.Error as error:
            print("Failed to create table in MySQL: {}".format(error))
        
        finally:
            if connection.is_connected():

                table = "DB_" + str(guild)

                mySql_Insert_Row_Query = "INSERT INTO " + table + " (User, Message) VALUES (%s, %s)"
                mySql_Insert_Row_Values = (str(interaction.user), message)

                cursor.execute(mySql_Insert_Row_Query, mySql_Insert_Row_Values)
                connection.commit()

                await interaction.response.send_message("I have stored your message for you!")

                cursor.close()
                connection.close()
                print("Mysql connection has been closed")


    @app_commands.command(name="retrieve_info", description="Retrieve some data that a user has stored")
    async def retrieve_info(self, interaction: discord.Interaction):

        guild = interaction.guild.id
        table = "DB_" + str(guild)

        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database = 'tutorial_bot',
                                                 user = 'root',
                                                 password = 'root')
            
            cursor = connection.cursor()

            sql_select_query = "Select * from " + table + " where user like '" + str(interaction.user) + "'"

            cursor.execute(sql_select_query)

            record = cursor.fetchall()

            Recieved_Data = []

            for row in record:
                Recieved_Data.append({"Id": str(row[0]), "Message": str(row[2])})

            await interaction.response.send_message("All Stored Data: \n \n " + json.dumps(Recieved_Data, indent=1))

        except mysql.connector.Error as error:
            print("Failed to get record from MySQL table: {}".format(error))

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("Mysql connection is closed")
    
    

async def setup(client):
    await client.add_cog(Admin(client), guilds=[discord.Object(id=SERVERID)])