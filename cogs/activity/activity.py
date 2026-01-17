#Allows to import config.py from the directory above
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.config as config

#Discord lib
import discord
from discord.ext import commands, tasks

#Random Numbers lib
import random

class Activity(commands.Cog, name="Activity"):
    """Activity cog"""
    @commands.Cog.listener()
    async def on_ready(self):
        print('Activity Cog initialized')
        self.change_activity.start()

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @tasks.loop(hours = 1)
    async def change_activity(self):
        rand = random.randint(0,2)

        if rand == 0:
            statuses = config.PLAY_STAT
            status = random.choice(statuses)
            await self.bot.change_presence(activity=discord.Game(name=status))
        
        if rand == 1:
            statuses = config.WATCH_STAT
            status = random.choice(statuses)
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))

        if rand == 2:
            statuses = config.LISTEN_STAT
            status = random.choice(statuses)
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status))

async def setup(bot: commands.Bot):

  await bot.add_cog(Activity(bot))
