import os
from dotenv import load_dotenv

import discord
from discord.ext import commands, tasks

import itertools

load_dotenv()

TOKEN = os.getenv("TOKEN")
PREFIX = os.getenv("PREFIX")

intents = discord.Intents.all()
intents.message_content = True

class QVIBot(commands.Bot):
    async def setup_hook(self):
        await self.load_extension("cogs.messages")
        await self.tree.sync()

bot = QVIBot(command_prefix=commands.when_mentioned_or(PREFIX), intents=intents)
@bot.event
async def on_ready() -> None:
    print(f'Logged in as {bot.user}')
    
    if not change_status.is_running():
        change_status.start()

statuses = itertools.cycle([
    discord.Activity(
        type=discord.ActivityType.watching,
        name="👁 Watching Q-Verse",
    ),
    discord.Activity(
        type=discord.ActivityType.watching,
        name="👁 Watching for stability failures",
    ),
    discord.Activity(
        type=discord.ActivityType.watching,
        name="👁 Watching CONTROL Layer",
    ),
    discord.Activity(
        type=discord.ActivityType.watching,
        name="👁 Watching QVI logs",
    ),
    discord.Activity(
        type=discord.ActivityType.listening,
        name="🎧 Listening to the void",
    ),
    discord.Activity(
        type=discord.ActivityType.playing,
        name="🎮 Playing with quantum layers",
    ),
])

@tasks.loop(seconds=30)
async def change_status():
    activity = next(statuses)

    await bot.change_presence(
        status=discord.Status.do_not_disturb,
        activity=activity,
    )

    print("Activity changed.")

bot.run(TOKEN)
