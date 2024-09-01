import requests


async def insult_generator_API(interaction):
    """Fetches a random insult from https://evilinsult.com"""

    URL = "https://evilinsult.com/generate_insult.php?lang=en&type=json"
    response = requests.get(URL)

    if response.status_code == 200:
        data = response.json()
        insult = data['insult']
        return await interaction.response.send_message(insult)
    else:
        return await interaction.response.send_message("Unable to fetch the request. Please try again later", ephemeral=True)
