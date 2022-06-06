import discord
from discord.ext import commands
import os
from keys import *
# BOT_TOKEN
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.event
async def on_ready():
    """
    Bot has started
    :return:
    """
    print("Ready")
    print("-"*27)


initial_extensions = []

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        initial_extensions.append("cogs." + filename[:-3])

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)


bot.run(BOT_TOKEN)