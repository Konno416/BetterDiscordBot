import discord
from discord.ext import commands
from discord import member
from discord import *
from discord.ext.commands import has_permissions, MissingPermissions
import json
import os
from dotenv import load_dotenv
import random
import aiohttp

load_dotenv()


SERVERID = os.getenv("SERVERID")   

class Games(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.questions = {}
        self.api_url = "https://opentdb.com/api.php?amount=1&difficulty=easy&type=multiple"


    async def get_random_question(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.api_url) as response:
                data = await response.json()
                question = data['results'][0]['question']
                correct_answer = data['results'][0]['correct_answer']
                print(data)
                return question, correct_answer

    @commands.Cog.listener()
    async def on_ready(self):
        print("Games.py is ready!")

    @app_commands.command(name="trivia", description="A command to allow users to quiz themselves on anything random! Use /answer to answer!")
    async def trivia(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        if user_id in self.questions:
            await interaction.response.send_message("You already have a question! Answer that one first.")
        else:
            question, answer = await self.get_random_question()
            await interaction.response.send_message(question)
            self.questions[user_id] = answer

    @app_commands.command(name="answer", description="Use this to answer the question you were given by the bot!")
    async def answer(self, interaction: discord.Interaction, user_answer: str):
        user_id = interaction.user.id
        if user_id not in self.questions:
            await interaction.response.send_message("You don't have a question to answer! Use the trivia command to get a question.")
        else:
            answer = self.questions[user_id]
            if user_answer.lower() == answer.lower():
                await interaction.response.send_message("Correct!")
            else:
                await interaction.response.send_message(f"{user_answer} is incorrect. The correct answer is: {answer}")
            del self.questions[user_id]
    


async def setup(client):
    await client.add_cog(Games(client), guilds=[discord.Object(id=SERVERID)])
