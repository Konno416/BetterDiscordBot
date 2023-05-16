import traceback
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord import member
from discord import *
from discord import File
from typing import Optional
from discord.ext.commands import has_permissions, MissingPermissions
import json
import os
from dotenv import load_dotenv
import wavelink
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from datetime import date
from easy_pil import Editor, load_image_async, Font

level = ['Level-5+', "Level-10+", "Level-15+"]

level_num = [5, 10, 15]


load_dotenv()

SERVERID = os.getenv("SERVERID")

#Have to make your own profane list in an array in the env file.
# profane = os.getenv("PROFANE")

class Admin(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Admin.py is ready!")

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        profane = os.getenv("PROFANE_WORDS").split(",")
        if message.author.bot:
            return  # ignore messages from bots
        for word in profane:
            if word in message.content.lower():
                await message.delete()
                user = message.author
                await user.send("Don't use profanity in this server or else!")
                break  # stop checking for profanity once one is found
        # print(message)
        if not message.content.startswith("!"):
            # print(message)
            if not message.author.bot:
                # print(message)
                try:
                    with open("levels.json", "r") as f:
                        data = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError):
                    data = {}
                    
                if str(message.author.id) in data:
                    xp = data[str(message.author.id)]['xp']
                    lvl = data[str(message.author.id)]['level']
                        
                    #increases the xp
                    increased_xp = xp+25
                    new_level = int(increased_xp/100)

                    data[str(message.author.id)]['xp']=increased_xp

                    with open("levels.json", 'w') as f:
                        json.dump(data, f)
                        
                    if new_level > lvl:
                        await message.channel.send(f"{message.author.mention} Just Leveled Up to Level {new_level}!!!")
                            
                        data[str(message.author.id)]['level']=new_level
                        data[str(message.author.id)]['xp']=0

                        with open("levels.json", "w") as f:
                            json.dump(data, f)

                        for i in range(len(level)):
                            if new_level == level_num[i]:
                                await message.author.add_roles(discord.utils.get(message.author.guild.roles, name=level[i]))

                                embed = discord.Embed(title=f"{message.author} You Have Gotten role **{level[i]}**", color=message.author.colour)

                                embed.set_thumbnail(url=message.author.avatar.url)
                                await message.channel.send(embed=embed)

                else:
                    data[str(message.author.id)] = {}
                    data[str(message.author.id)]['xp'] = 0
                    data[str(message.author.id)]['level'] = 1
                    print(data)

                    with open("levels.json", "w") as f:
                        json.dump(data, f)

        await self.client.process_commands(message)

    @commands.command(name="rank")
    async def rank(self, ctx: commands.Context, user: Optional[discord.Member]):
        userr = user or ctx.author

        with open("levels.json", "r") as f:
            data = json.load(f)
        
        xp = data[str(userr.id)]["xp"]
        lvl = data[str(userr.id)]["level"]

        next_levelup_xp = (lvl+1)*100
        xp_need = next_levelup_xp
        xp_have = data[str(userr.id)]["xp"]

        percentage = int(((xp_have*100)/xp_need))

        background = Editor("zImage.png")
        profile = await load_image_async(str(userr.avatar.url))

        profile = Editor(profile).resize((150, 150)).circle_image()

        poppins = Font.poppins(size=40)
        poppins_small = Font.poppins(size=30)

        ima = Editor("zBlack.png")
        background.blend(image=ima, alpha=.5, on_top=False)

        background.rectangle((30, 220), width=650, height=40, fill="#fff", radius=20)
        background.bar(
            (30, 220),
            max_width=650,
            height=40,
            percentage=percentage,
            fill="#ff9933",
            radius=20,
        )
        background.text((200, 40), str(userr.name), font=poppins, color="#ff9933")

        background.rectangle((200, 40), width=350, height=2, fill="#ff9933")
        background.text(
            (200, 130),
            f"Level : {lvl}"
            + f"xp : {xp} / {(lvl+1)*100}",
            font=poppins_small,
            color="#ff9933"
        )

        card = File(fp=background.image_bytes, filename="zCard.png")
        await ctx.send(file=card)
    
    @commands.command(name="leaderboard")
    async def leaderboard(self, ctx, range_num=5):
        with open("levels.json", "r") as f:
            data = json.load(f)
        
        l = {}
        total_xp = []

        for userid in data:
            xp = int(data[str(userid)]["xp"])+(int(data[str(userid)]['level']*100))

            l[xp] = f"{userid};{data[str(userid)]['xp']};{data[str(userid)]['level']}"
            total_xp.append(xp)

        total_xp = sorted(total_xp, reverse=True)
        index=1

        mbed = discord.Embed(
            title="Leaderboard"
        )

        for amt in total_xp:
            id_ = int(str(l[amt]).split(";")[0])
            level = int(str(l[amt]).split(";")[1])
            xp = int(str(l[amt]).split(";")[2])

            member = await self.client.fetch_user(id_)

            if member is not None:
                name = member.name
                mbed.add_field(name=f"{index}. {name}",
                value=f"**Level: {level} | XP: {xp}**",
                inline=False)

                if index == range_num:
                    break
                else:
                    index += 1

        await ctx.send(embed=mbed)
    
    

    @commands.command()
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        """Clears the specified number of messages."""
        # Add a check to ensure the user has the necessary permissions if required.

        # Delete the command message
        await ctx.message.delete()

        # Delete the desired number of messages
        deleted = await ctx.channel.purge(limit=amount)

        # Send a response about the number of deleted messages
        response = f"Cleared {len(deleted)} messages."
        await ctx.send(response, delete_after=5)  # Delete the response after 5 seconds


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


    @app_commands.command(name="statistics", description="Shows the statistics for a selected user")
    async def statistics(self, interaction: discord.Interaction, user: discord.Member):

        pic = user.avatar.url

        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database = 'tutorial_bot',
                                                 user = 'root',
                                                 password = '')
            
            cursor = connection.cursor()

            sql_select_query = "Select * from Users where user like '" + str(user) + "'"

            cursor.execute(sql_select_query)

            record = cursor.fetchone()

            print(record)

            if(record == None):
                await interaction.response.send_message("There is no data on this individual!", ephemeral=True)
            
            embed = discord.Embed(
            color=discord.Color.dark_blue(),
            title="Stats", 
            description=f"Statistics of {user}!"    
            )
            embed.add_field(name="ID: ", value=record[0])
            embed.add_field(name="Name: ", value=record[1])
            embed.add_field(name="Joined: ", value=record[2])
            embed.set_thumbnail(url=pic)

            
            await interaction.response.send_message(embed=embed, ephemeral=True)

        except mysql.connector.Error as error:
            print("Failed to get record from MySQL table: {}".format(error))

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("Mysql connection is closed")


    @app_commands.command(name="add_user", description="Adds a user to the stats Database if they are not in it already!")
    async def add_user_DB(self, interaction: discord.Interaction, user: discord.Member):

        pic = user.avatar.url
        name = user.name
        pic = user.display_avatar.url
        memberId = user.id
        joined = user.joined_at.date()

        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database = 'tutorial_bot',
                                                 user = 'root',
                                                 password = '')
            
            cursor = connection.cursor()

            sql_select_query = "Select * from Users where user like '" + str(user) + "'"

            cursor.execute(sql_select_query)

            record = cursor.fetchone()

            print(record)

            if(record == None):
                mySql_Insert_Row_Query = "INSERT INTO `users` (`Id`, `User`, `Joinedat`) VALUES (%s, %s, %s);"
                mySql_Insert_Row_Value = (str(memberId), str(user), str(joined))

                cursor.execute(mySql_Insert_Row_Query, mySql_Insert_Row_Value)
                connection.commit()

                await interaction.response.send_message("Added user to the database!", ephemeral=True)

            else:
                await interaction.response.send_message("User is already in the database!", ephemeral=True)

        except mysql.connector.Error as error:
            print("Failed to get record from MySQL table: {}".format(error))

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("Mysql connection is closed")


    @app_commands.command(name="server_stats", description="Shows server stats!")
    async def server_stats(self, interaction: discord.Interaction):

        serverdate = interaction.guild.created_at.date()
        memberamount = interaction.guild.member_count
        serverid = interaction.guild.id
        pic = interaction.guild.icon.url

        # print(serverdate)
        # print(memberamount)
        # print(serverid)
        # print(f"picture = {pic}")
        

        embed = discord.Embed(
            color=discord.Color.blue(), 
            title="Server Statistics", 
            description="Here are some server Statistics"
            )
        embed.add_field(name="Server ID: ", value=serverid)
        embed.add_field(name="Member Amount: ", value=memberamount)
        embed.add_field(name="Server Created", value=serverdate)
        embed.set_thumbnail(url=pic)

        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    

async def setup(client):
    await client.add_cog(Admin(client), guilds=[discord.Object(id=SERVERID)])