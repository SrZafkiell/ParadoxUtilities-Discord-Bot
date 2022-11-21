# Author: Daniel Alejandro Ceron Rayo
# Software development student at Universidad del valle Cali-Colombia / 1st semester
# Mail: daniel.rayo@correounivalle.edu.co

# Importing required discord dependencies
import discord
from discord.ext import commands

# Importing extra functions dependencies
import os
import traceback
import asyncio
import platform

# Importing BOT packages
import colors
from keys import *


# STARTING BOT FUNCTIONS
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents, description="https://github.com/SrZafkiell",
                   owner_id=285699404713820170, application_id=1041239518487007304)

prefix = "[ParadoxU]:"


async def loadExtensions():
    try:
        # This for statement will loop on all the cogs dir searching for all the .py files
        # If it finds a .py file, it gets added to the initialExtensions list.
        for filename in os.listdir("./cogs"):
            # Conditional searching for all the files that ends with .py
            if filename.endswith(".py"):
                # Once it finds a .py file, it gets added to the inicialExtensions list without the .py
                # termination "[:-3]" removes the last 3 chars -> ".py"
                await bot.load_extension(f"cogs.{filename[:-3]}")
        print("Loaded: Extensions ->", bot.extensions.items())
    except:
        print("Something wrong happen when loading the extensions")
        traceback.print_exc()


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name="Paradox", url="https://www.twitch.tv/srzafkiell"))
    print("Loaded: Bot presence")
    synced = await bot.tree.sync()
    print(prefix+f" Commands has been synced / Synced {len(synced)} commands")


@bot.tree.command(name="credits", description="Bot credits")
async def paradox(interaction: discord.Interaction):
    await interaction.response.send_message(content=f"Developed by: SrZafkiell")


async def main():
    if not os.path.isdir("./ErrorLogs"):
        os.makedirs("./ErrorLogs")
        print("ErrorLogs directory has been created")

    if not os.path.isdir("./Storage"):
        os.makedirs("./Storage")
        print("Storage directory has been created")

    async with bot:
        await loadExtensions()
        await bot.start(botToken)

try:
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
except KeyboardInterrupt:
    print("INFO: El bot ha sido terminado KeyboardInterrupt")
    # print("STARTS KeyboardInterrupt stacktrace", traceback.print_exc(), "ENDS KeyboardInterrupt stacktrace")
except RuntimeError:
    print("INFO: El bot ha sido terminado RuntimeError")
    # print("STARTS KeyboardInterrupt stacktrace", traceback.print_exc(), "ENDS KeyboardInterrupt stacktrace")
except asyncio.TimeoutError:
    print("INFO: El bot ha sido terminado asyncio RuntimeError")
    # print("STARTS asyncio.TimeoutError stacktrace", traceback.print_exc(), "ENDS asyncio.TimeoutError stacktrace")

