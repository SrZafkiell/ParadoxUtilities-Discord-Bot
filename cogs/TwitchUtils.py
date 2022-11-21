# Author: Daniel Alejandro Ceron Rayo
# Software development student at Universidad del Valle Cali-Colombia / 1st semester
# Mail: daniel.rayo@correounivalle.edu.co

# Importing required discord dependencies
import ast
import os
import datetime

import discord
from discord.ext import commands, tasks
from discord import app_commands

# Importing extra function dependencies
# requests -> We using this library to ask the twitch API for info
import requests
import pytz

# Importing BOT packages
import keys

# The following list will store other lists of streamers
# [streamer_name, streamer_message, streamer_status]
# streamer_name
#   -> This will store the name of the streamer that was given by the adder
#   -> IMPORTANT: This name will be stored in lower case
# streamer_message
#   -> This will store the message that will invite the people to the stream
# streamer_status
#   -> This will store if the streamer is live or not
#   [Live -> True / Offline -> False]
# streamer_profile_pic
#   -> This will store the url for the profile picture

streamersStorage = []
currently_streaming = []
announcements_channel = 804522055956561930


async def get_stream_data(streamer):
    searchScope = "streams?user_login="
    response = requests.request("GET", keys.twitchApiUrl + searchScope + streamer.lower(), headers=keys.twitchHeaders)
    data_from_request = response.json().get('data')
    return data_from_request


async def get_user_data(streamer):
    # We have the api url as 'https://api.twitch.tv/helix/', then we need to
    # select where are we going to ask for the information. It is 'users?login='
    searchScope = "users?login="
    # The response is going to be
    # 200 OK	Successfully retrieved the specified users’ information.
    # 400 Bad Request
    # The id or login query parameter is required unless the request uses a user access token.
    # The request exceeded the maximum allowed number of id and/or login query parameters.
    # 401 Unauthorized
    # The Authorization header is required and must contain an app access token or user access token.
    # The access token is not valid.
    # The ID specified in the Client-Id header does not match the client ID specified in the access token.
    response = requests.request("GET", keys.twitchApiUrl + searchScope + streamer.lower(),
                                headers=keys.twitchHeaders)
    # We need to extract the data from the response, it is given in the following
    # syntax: {'data': [], 'pagination': {}}. Then store only the 'data' part from
    # the response in dataFromRequest
    data_from_request = response.json().get('data')
    return data_from_request


# The 'streamerExists(streamer)' functions will determine if the streamer is
# a valid name on twitch.
# Returns:
# If the account exists -> True
# If the account doesn't exist -> False
async def streamerExists(streamer):
    dataFromRequest = await get_user_data(streamer)
    if not dataFromRequest:
        return False
    else:
        return True


# the 'streamerExists(streamer)' functions will determine if the streamer is
# already a part of the 'streamersList' List.
# Returns:
# If the streamer is already in the list -> True
# If the streamer is not in the list -> False
async def streamerAlreadyOnList(streamer):
    # If the 'streamersStorage' is empty, this returns False
    if not streamersStorage:
        return False
    else:
        # This loop will look for the streamer's name given
        # and will return 'True' if it gets found
        for s in range(0, len(streamersStorage), 1):
            if streamersStorage[s][0] == streamer.lower():
                return True
        # If the 'streamer' is no on the 'streamersStorage' returns False
        return False


async def isLive(streamer):
    data_from_request = await get_stream_data(streamer)
    if not data_from_request:
        return False
    else:
        return True


# Para futuras versiones:
# * Añadir soporte para UTF-8
# * Añadir manejo de error en caso de que los datos del archivo no sean los esperados
async def streamersStorageManager():
    if os.path.exists('./storage/TwitchUtils/currently-streaming.txt'):
        if not currently_streaming:
            if os.stat("./storage/TwitchUtils/currently-streaming.txt").st_size == 0:
                print("[TwitchUtils - Vault]: There are not live streamers to sync with bot")
            else:
                with open("./storage/TwitchUtils/currently-streaming.txt", "r") as file:
                    temp = file.read()
                    temp = list(ast.literal_eval(temp))
                    for streamer in range(0, len(temp), 1):
                        currently_streaming.append(temp[streamer])
                    if currently_streaming == temp:
                        print("[TwitchUtils - Vault]: Data from file has been synced with bot")
                    else:
                        print("[TwitchUtils - Vault]: Something went wrong while syncing the data to bot")
                    file.close()
        else:
            if os.stat("./storage/TwitchUtils/currently-streaming.txt").st_size == 0:
                file = open("./storage/TwitchUtils/currently-streaming.txt", "w")
                file.write(str(currently_streaming))
                print("[TwitchUtils - Vault]: Data from bot has been synced to file")
                file.close()
            else:
                file = open("./storage/TwitchUtils/currently-streaming.txt", "r")
                temp = file.read()
                temp = list(ast.literal_eval(temp))
                if temp != currently_streaming:
                    file.close()
                    with open("./storage/TwitchUtils/streamers.txt", "w") as file:
                        file.write(str(currently_streaming))
                        print("[TwitchUtils - Vault]: Data from bot has been synced to file")
                else:
                    print("[TwitchUtils - Vault]: Data is up to date")
                    file.close()
    else:
        with open("./storage/TwitchUtils/currently-streaming.txt", "w") as file:
            if not currently_streaming:
                print("[TwitchUtils - Vault]: currently-streaming.txt has been created. There was no data to store.")
            else:
                file.write(str(currently_streaming))
                print("[TwitchUtils - Vault]: currently-streaming.txt has been created and synced")

    if os.path.exists('./storage/TwitchUtils/streamers.txt'):
        if not streamersStorage:
            if os.stat("./storage/TwitchUtils/streamers.txt").st_size == 0:
                print("[TwitchUtils - Vault]: There are no data to be synced with the bot")
            else:
                with open("./storage/TwitchUtils/streamers.txt", "r") as file:
                    # Reads the contents of the file "str" and stores them in "temp"
                    temp = file.read()
                    # Removes the first and last chars on the streamers.txt.
                    # This chars should be "[" and "]". First and Last respectively
                    # temp = temp[1:-1]
                    # For now, we have and string in the form of
                    # [streamer_name, streamer_message, streamer_status, streamer_profile_pic],
                    # [streamer_name, streamer_message, streamer_status, streamer_profile_pic]
                    # Then we convert "temp" to a list.
                    temp = list(ast.literal_eval(temp))
                    # Now we have to give values to the streamersStorage but, as it is out
                    # of the scope, we have to append each item from temp into streamersStorage
                    # streamer -> index for temp
                    # "0" in range -> We need to start at the first index for temp
                    # len(temp) -> This will give us the amount of items we have to append
                    for streamer in range(0, len(temp), 1):
                        # We append one of the items on temp[streamer], each item is in the form of
                        # [streamer_name, streamer_message, streamer_status, streamer_profile_pic]
                        streamersStorage.append(temp[streamer])
                    if streamersStorage == temp:
                        print("[TwitchUtils - Vault]: Data from file has been synced with bot")
                    else:
                        print("[TwitchUtils - Vault]: Something went wrong while syncing the data to bot")
                    file.close()
        else:
            fileSize = os.stat("./storage/TwitchUtils/streamers.txt").st_size
            if fileSize == 0:
                file = open("./storage/TwitchUtils/streamers.txt", "w")
                file.write(str(streamersStorage))
                print("[TwitchUtils - Vault]: Data from bot has been synced to file")
                file.close()
            else:
                file = open("./storage/TwitchUtils/streamers.txt", "r")
                # Reads the contents of the file "str" and stores them in "temp"
                temp = file.read()
                # Removes the first and last chars on the streamers.txt.
                # This chars should be "[" and "]". First and Last respectively
                # temp = temp[1:-1]
                # For now, we have and string in the form of
                # [streamer_name, streamer_message, streamer_status, streamer_profile_pic],
                # [streamer_name, streamer_message, streamer_status, streamer_profile_pic]
                # Then we convert "temp" to a list.
                temp = list(ast.literal_eval(temp))
                if temp != streamersStorage:
                    file.close()
                    with open("./storage/TwitchUtils/streamers.txt", "w") as file:
                        file.write(str(streamersStorage))
                        print("[TwitchUtils - Vault]: Data from bot has been synced to file")
                        file.close()
                else:
                    print("[TwitchUtils - Vault]: Data is up to date")
                    file.close()
    else:
        with open("./storage/TwitchUtils/streamers.txt", "w") as file:
            if not streamersStorage:
                print("[TwitchUtils - Vault]: streamers.txt has been created. There was no data to store.")
            # This else should not happen but it is there in case
            else:
                file.write(str(streamersStorage))
                print("[TwitchUtils - Vault]: streamers.txt has been created and synced")


# currently_streaming = []
# [streamer, announced]
async def live_manager():
    to_be_announced = []
    coincidences = 0
    for streamer in range(0, len(streamersStorage), 1):
        if await isLive(streamersStorage[streamer][0]):
            if not currently_streaming:
                currently_streaming.append([streamersStorage[streamer][0], True])
                to_be_announced.append(streamersStorage[streamer][0])
            else:
                for streamer_pos in range(0, len(currently_streaming), 1):
                    if currently_streaming[streamer_pos][0] == streamersStorage[streamer][0]:
                        coincidences = coincidences + 1
                if coincidences == 0:
                    currently_streaming.append([streamersStorage[streamer][0], True])
                    to_be_announced.append(streamersStorage[streamer][0])

    for streamer_live in range(0, len(currently_streaming), 1):
        if not await isLive(currently_streaming[streamer_live][0]):
            print(f"Removing: {currently_streaming[streamer_live]}")
            currently_streaming[streamer_live].remove()

    return to_be_announced


class TwitchUtils(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    async def live_announce(streamer_name, channel):
        stream_data = await get_stream_data(streamer_name)
        user_data = await get_user_data(streamer_name)
        print(f"Generate embed: Stream - {stream_data} User- {user_data}")
        print(f"List test: {type(stream_data)} {type(user_data)}")
        print(f"Dict test: {type(stream_data[0])} {type(user_data[0])}")
        print(f"Test get: {user_data[0].get('display_name')} {stream_data[0].get('title')}")
        embed = discord.Embed(title=f":red_circle: {user_data[0].get('display_name')} ha iniciado un stream!",
                              url=f"https://www.twitch.tv/+{user_data[0].get('display_name')}",
                              description="Únete y muéstrale tu apoyo",
                              color=0x70119c)
        embed.set_author(name="Paradox - Stream Checker",
                         icon_url="https://cdn-icons-png.flaticon.com/512/5968/5968819.png",
                         url=f"https://www.twitch.tv/+{user_data[0].get('display_name')}")
        embed.set_thumbnail(url=f"{user_data[0].get('profile_image_url')}")
        embed.add_field(name=":small_orange_diamond: Streamer Name",
                        value=f"{user_data[0].get('display_name')}",
                        inline=True)
        embed.add_field(name=":small_orange_diamond: Stream Game:",
                        value=f"{stream_data[0].get('game_name')}",
                        inline=True)
        embed.add_field(name=":small_orange_diamond: Stream Title:",
                        value=f"{stream_data[0].get('title')}",
                        inline=False)
        embed.add_field(name=":small_orange_diamond: Viewers",
                        value=f"{stream_data[0].get('viewer_count')}",
                        inline=True)
        embed.set_image(
            url=f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{stream_data[0].get('user_login')}-1920x1080.jpg")
        embed.set_footer(
            text=f"\n» {datetime.datetime.now(pytz.timezone('America/Bogota')).strftime('%B %d %Y - %H:%M:%S')} (GMT-5) «"
                 "\nParadox Utilities Discord Bot × Twitch Announcer"
                 "\n"
                 "\nDeveloped by: @SrZafkiell")
        await channel.send(embed=embed)
        await channel.send(f">>> :rotating_light: **Announce tags:** <@&804524421867896902>")

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(self, ctx) -> None:
        fmt = await ctx.bot.tree.sync(guild=ctx.guilg)
        await ctx.send(f"TwitchUtils: Synced {len(fmt)} commands")

    # Twitch checker loop
    @tasks.loop(seconds=10)
    async def streamChecker(self):
        try:
            print(f"[{datetime.datetime.now()}]: Task loop streamersStorageManager()")
            await streamersStorageManager()
            to_be_announced = await live_manager()
            announce_in = self.bot.get_channel(announcements_channel)
            for streamer in range(0, len(to_be_announced), 1):
                await self.live_announce(to_be_announced[streamer], announce_in)
        except Exception as e:
            print("Something went wrong in the streamChecker Task Loop")
            if os.path.exists('./ErrorLogs/StorageManager.txt'):
                errorLog = open("./ErrorLogs/StorageManager.txt", "r+")
                temp = errorLog.read()
                errorLog.write(f"{temp}[{datetime.datetime.now()}]: {str(repr(e))}\n")
                errorLog.close()
                print("Error has been logged on ./ErrorLogs/StorageManager.txt")
            else:
                errorLog = open("./ErrorLogs/StorageManager.txt", "x")
                errorLog.close()

    # Declaring event listener for:
    @commands.Cog.listener()
    async def on_ready(self):
        print("Loaded: Cog 'TwitchUtils'")
        if not os.path.isdir("./storage/TwitchUtils"):
            os.makedirs("./storage/TwitchUtils")
            print("TwitchUtils directory has been created in Storage")
        try:
            await self.streamChecker.start()
            print("Loaded: Stream Checker routine")
        except Exception as e:
            print("ERROR: streamChecker function couldn't start")
            print("STARTS streamChecker stacktrace", e, "ENDS streamChecker stacktrace")

    # Revisar profile pic, si se permite cualquier dominio pueden haber alertas con imagenes NSFW
    @app_commands.command(name="addstreamer", description="Add an streamer to Twitch module")
    @app_commands.describe(streamer_name="Name of the streamer to add. It has to be a valid twitch account",
                           streamer_message="Invitation message for the streamer live notification",
                           streamer_status="Current status of the streamer / True = (Live) / False = (Offline) /",
                           streamer_profile_pic="Profile picture URL for the streamer notification.")
    @app_commands.choices(streamer_message=[
        app_commands.Choice(name="Te invito a unirte al stream", value="Te invito a unirte al stream"),
        app_commands.Choice(name="No hay otro stream mejor, te espero!", value="No hay otro stream mejor, te espero!")
    ])
    @app_commands.checks.has_permissions(administrator=True)
    async def add_streamer(self, interaction: discord.Interaction,
                           streamer_name: str,
                           streamer_message: app_commands.Choice[str] = "Spanish",
                           streamer_status: bool = False,
                           streamer_profile_pic: str = "https://cdn-icons-png.flaticon.com/512/5968/5968819.png"):
        if await streamerExists(streamer_name):
            # The streamer exists
            if not await streamerAlreadyOnList(streamer_name):
                try:
                    streamerInfo = [streamer_name.lower(), streamer_message, streamer_status, streamer_profile_pic]
                    streamersStorage.append(streamerInfo)
                    await interaction.response.send_message(streamer_name.lower() + " has been added to the list")
                    print("Streamers stored:", streamersStorage)
                except:
                    await interaction.response.send_message(
                        "ERROR: Something went wrong while adding the streamer to the list")
            else:
                await interaction.response.send_message("Streamer is already on the list")
        else:
            # The streamer doesn't exists
            await interaction.response.send_message(f"The streamer {streamer_name} doesn't exists")


# Exporting the class
async def setup(bot):
    await bot.add_cog(TwitchUtils(bot))
