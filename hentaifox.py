import re
import discord
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


async def hentai_fox(interaction, numbers):
    options = Options()
    options.add_argument('--headless=new')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(f'https://hentaifox.com/gallery/{numbers}')  # numbers.content

    header = driver.find_element("xpath", '//*[@class="info"]/h1')
    tags = driver.find_element("xpath", '//*[@class="tags"]')
    artists = driver.find_element("xpath", '//*[@class="artists"]/li/a')
    languages = driver.find_element("xpath", '//*[@class="languages"]')
    category = driver.find_element("xpath", '//*[@class="categories"]')
    pages = driver.find_element("xpath", '//*[@class="i_text pages"]')
    img = driver.find_element("xpath", '//*[@class="cover"]/img')

    """print(tags.text)
    print(artists.text)
    print(languages.text)
    print(category.text)"""

    embed = discord.Embed(
        colour=discord.Color.yellow(),
        description=f'**{tags.text[:4]}:** {await regex(tags.text[5:])}'
                    f'\n**Artists:** {await regex(artists.text)}'
                    f'\n**{languages.text[:9]}:** {await regex(languages.text[10:])}'
                    f'\n**{category.text[:8]}:** {await regex(category.text[9:])}'
                    f'\n**{pages.text[:5]}:** {pages.text[6:]}'
    )
    embed.set_author(name=header.text, url=f'https://hentaifox.com/gallery/{numbers}')
    embed.set_footer(text=f'https://hentaifox.com/gallery/{numbers}',
                     icon_url="https://hentaifox.com/images/logo.png")
    embed.set_image(url=img.get_attribute("src"))

    driver.quit()
    # return await numbers.channel.send(embed=embed, reference=numbers)
    return await interaction.followup.send(embed=embed)


async def regex(test):
    pattern = re.compile(r'\d')
    result_string = re.sub(pattern, '', test)
    result_list = [item.strip() for item in result_string.split(' ') if item.strip()]
    result_str = ', '.join(result_list)
    return result_str
