import discord
import requests
import urllib.parse

from discord import NotFound


async def trace_moe(interaction, url):
    try:
        response = requests.get("https://api.trace.moe/search?anilistInfo&url={}".format(urllib.parse.quote_plus(url))).json()

        data = response
        title_jp = data['result'][0]['anilist']['title']['native']
        title = data['result'][0]['anilist']['title']['romaji']
        accuracy = data['result'][0]['similarity']
        image = data['result'][1]['image']
        episode = data['result'][1]['episode']
        percent = round(accuracy * 100, 2)
        print(data)

        embed = discord.Embed(
            colour=discord.Color.blurple(),
            description=f'Accuracy: **{percent}%**'
                        f'\nEpisode: **{episode}**'
        )
        embed.set_author(name=f'{title_jp} | {title}')
        embed.set_image(url=image)
        embed.set_thumbnail(url=url)

        return await interaction.response.send_message(embed=embed)
    except KeyError as error:
        return await interaction.response.send_message("Invalid URL or Website is down", ephemeral=True)
    except NotFound as e:
        return await interaction.response.send_message("Invalid URL or Website is down", ephemeral=True)

