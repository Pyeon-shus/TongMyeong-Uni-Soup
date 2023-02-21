import discord
import asyncio
import os
from discord.ext import commands
from discord.ext.commands import Bot

TOKEN = os.environ['TOKEN']
client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_message(message):
    content = message.content
    guild = message.guild
    author = message.author
    channel = message.channel
    if content.startswith("!test"):
        await message.channel.send("test" + message.content)
    if content == "!ping":
        await message.channel.send("Pong!")
try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
