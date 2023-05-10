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
import random

load_dotenv()


SERVERID = os.getenv("SERVERID")   

class Games(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.questions = {}

        with open('trivia_questions.json') as f:
            self.trivia_questions = json.load(f)

    def get_random_question(self):
        random_question = random.choice(self.trivia_questions)
        return random_question['question'], random_question['answer']

    @commands.Cog.listener()
    async def on_ready(self):
        print("Games.py is ready!")

    @app_commands.command(name="trivia", description="A command to allow users to quiz themselves on anything random! Use /answer to answer!")
    async def trivia(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        if user_id in self.questions:
            await interaction.response.send_message("You already have a question! Answer that one first.")
        else:
            question, answer = self.get_random_question()
            await interaction.response.send_message(question)
            self.questions[user_id] = answer

    @app_commands.command(name="answer", description="Use this to answer the question you were given by the bot!")
    async def answer(self, interaction: discord.Interaction, user_answer: str):
        user_id = interaction.user.id
        if user_id not in self.questions:
            await interaction.response.send_message("You don't have a question to answer! Use the trivia command to get a questions.")
        else:
            answer = self.questions[user_id]
            if user_answer.lower() == answer.lower():
                await interaction.response.send_message("Correct!")
            else:
                await interaction.response.send_message(user_answer + " is incorrect. The correct answer is: " + answer)
            del self.questions[user_id]
    


async def setup(client):
    await client.add_cog(Games(client), guilds=[discord.Object(id=SERVERID)])
