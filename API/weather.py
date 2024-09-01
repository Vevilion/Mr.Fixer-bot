import requests
import discord

from API.utils.iso_country_codes import ISO3166


async def weather_call(location, interaction):
    """Fetches a weather data from https://openweathermap.org. Takes in an arg for a city/country"""

    API_KEY = ['API TOKEN HERE']
    WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather'

    request_url = f"{WEATHER_URL}?appid={API_KEY}&q={location}"
    response = requests.get(request_url)

    if response.status_code == 200:
        data = response.json()
        weather_main = data['weather'][0]['main']
        # weather = data['weather'][0]['description']
        country = data['sys']['country']
        place = data['name']
        tempC = round(data['main']['temp'] - 273.15, 2)
        tempF = (int(tempC) * 9 / 5) + 32
        humidity = data['main']['humidity']
        # print(data)
        # print(ISO3166[country])
        embed = discord.Embed(
            colour=discord.Color.blue()
        )
        embed.set_author(name=f'Weather for {ISO3166[country]}, {place}')
        embed.add_field(name=f'**{tempC}°C / {tempF}°F**', value='', inline=False)
        embed.add_field(name=f'Weather condition: {weather_main}', value='', inline=False)
        embed.add_field(name=f'Humidity: {humidity}%', value='', inline=False)

        return await interaction.response.send_message(embed=embed)
    else:
        return await interaction.response.send_message("Invalid Location! Or website perhaps might be down", ephemeral=True)
