import random
import re

import discord
from discord import app_commands
from discord.ext import commands

from hentaiScrapper import nhentai_code
from hentaifox import hentai_fox
from API.weather import weather_call
from API.Igenerator import insult_generator_API
from API.trace_moe import trace_moe

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


def start():
    TOKEN = ['TOKEN HERE']

    @bot.event
    async def on_ready():
        await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="Provides general support"))
        print(f'{bot.user} is now online!')
        """try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)"""

    @bot.event
    async def on_message(msg):
        if msg.author == bot.user:
            return
        # await on_twitter(msg) | Down for future notice
        # await on_six_digits(msg)
        await temptConverter(msg)

    # SLASH COMMANDS
    @bot.tree.command(name="sync", description="Owner only")
    async def guild_sync(interaction: discord.interactions.Interaction):
        if interaction.user.name == 'vevy':
            # synced = await bot.tree.sync(guild=discord.Object(id=567355696786440202))
            synced = await bot.tree.sync()
            await interaction.response.send_message(f'Synced {len(synced)} command(s) to the current guild', ephemeral=True)
        else:
            await interaction.response.send_message("You must be the Owner to use this command", ephemeral=True)

    @bot.tree.command(name="weather", description="Provide a country or a city")
    @app_commands.describe(location='Country or City')
    async def weather(interaction: discord.interactions.Interaction, location: str):
        await weather_call(location, interaction)

    @bot.tree.command(name="insult", description="Generate a random insult")
    async def insult_generator(interaction: discord.interactions.Interaction):
        await insult_generator_API(interaction)

    """@bot.tree.command(name="server_restart", description="Restart Palword Server")
    async def server_restart(interaction: discord.interactions.Interaction):
        try:
            os.system("TASKKILL /F /IM cmd.exe")
        except Exception as e:
            print(e)

        time.sleep(2)

        try:
            os.startfile("C:/Users/0Ende\Desktop\SteamCMD/palworld_server.bat")
        except Exception as e:
            print(e)
        await interaction.response.send_message("Server restarted")"""

    """@bot.tree.command(name="eval", description="Evaluates given parameters")
    @app_commands.describe(argument='Provide an argument to evaluate')
    async def evaluation(interaction: discord.interactions.Interaction, argument: str):
        try:
            await interaction.response.send_message(f'```py'
                                                    f'\n# Argument given:\n{argument}\n\n'
                                                    f'# Output:\nSUCCESS: {(eval(argument))}'
                                                    f'```')
        except Exception as e:
            await interaction.response.send_message(f'```py'
                                                    f'\n# Argument given:\n{argument}\n\n'
                                                    f'# Output:\nERROR: {e}```')"""

    @bot.tree.command(name="flipcoin", description="Flips the coin")
    async def insult_generator(interaction: discord.interactions.Interaction):
        coin = ['heads', 'tails']
        rand = random.choice(coin)
        await interaction.response.send_message(f'Coin lands on **{rand}**')

    @bot.tree.command(name="tracemoe", description="Provides the data for anime character by looking at the image")
    @app_commands.describe(url='Provide a url to a picture of anime')
    async def trace_moe_API(interaction: discord.interactions.Interaction, url: str):
        await trace_moe(interaction, url)

    # NORMAL COMMANDS
    """
    # TWITTER FIXED ITS EMBED
    # IM PAUSING THE USE OF THIS FUNCTION FOR THE TIME BEING
    async def on_twitter(msg):
        try:
            twitter = msg.content.split('https://twitter.com/')
            x = msg.content.split('https://x.com/')

            _site = msg.content.split('/', 3)[-2]

            if _site == "twitter.com":
                await msg.channel.send('https://fxtwitter.com/' + twitter[1], reference=msg)
            elif _site == "x.com":
                await msg.channel.send('https://fxtwitter.com/' + x[1], reference=msg)
        except IndexError as e:
            return"""

    @bot.tree.command(name="hentai", description="Fetches hentai from hentai.to")
    async def nhentai(interaction: discord.interactions.Interaction, numbers: str):
        await interaction.response.defer()
        try:
            _digits = numbers
            if is_integer(_digits):
                await nhentai_code(interaction, numbers)
            else:
                await interaction.followup.send("Please use numbers only | Or numbers could be out of scope")
        except Exception as e:
            return

    @bot.tree.command(name="hentaifox", description="Fetches hentai from hentaifox")
    async def nhentai(interaction: discord.interactions.Interaction, numbers: str):
        await interaction.response.defer()
        try:
            _digits = numbers
            if is_integer(_digits):
                await hentai_fox(interaction, numbers)
            else:
                await interaction.followup.send("Please use numbers only | Or numbers could be out of scope")
        except Exception as e:
            return

    """async def on_six_digits(msg):
        try:
            six_digits = msg.content
            if len(six_digits) == 6 and is_integer(six_digits):
                await hentai_fox(msg)
        except Exception as e:
            print("a")
            return"""

    async def temptConverter(msg):
        # TODO: Check and return whole integer or float
        if msg.author == bot.user:
            return
        try:
            temp = tempValue(msg.content)
            for value, unit, space, extraValue in temp:
                if (unit == 'c' or unit == 'C') and (space or not extraValue):
                    result = (int(value) * 9 / 5) + 32
                    await msg.channel.send(f'{value}{unit} = {result:.1f}F', reference=msg)
                    # Printing out value + unit for testing
                if (unit == 'f' or unit == 'F') and (space or not extraValue):
                    result = (int(value) - 32) * 5 / 9
                    await msg.channel.send(f'{value}{unit} = {result:.1f}C', reference=msg)
                    # Printing out value + unit for testing
        except Exception as e:
            return

    def tempValue(msg):
        pattern = re.compile(r'(\d+)([CFcf])(\s*)([A-Za-z0-9]?)')
        matches = pattern.findall(msg)
        return matches

    def is_integer(n):
        try:
            float(n)
        except ValueError:
            return False
        else:
            return float(n).is_integer()

    bot.run(TOKEN)


if __name__ == '__main__':
    start()
