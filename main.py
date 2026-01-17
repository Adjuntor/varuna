#Allows to import cogs
import os
import config.config as config

#Async lib
import asyncio

#Discord lib
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix=config.PREFIX, owner_id = config.OWNER_ID, intents=intents, help_command=None)

@bot.event
async def on_ready():
      print('Bot is online')

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message[0] == config.PREFIX:
        return
    if message.author == bot.user:
        return

#load cogs inside /cogs/<dir>
async def load():
    for x in config.ACTIVECOGS:
        for dir in os.listdir('./cogs'):
            for file in os.listdir('./cogs/'+dir):
                if file == x:
                    if file.endswith('.py'):
                        await bot.load_extension(f'cogs.{dir}.{file[:-3]}')
                        print(f'{file} Loaded')

async def main():
    await load()
    await bot.start(config.TOKEN)


asyncio.run(main())

