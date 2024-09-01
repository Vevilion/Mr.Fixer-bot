import re
import discord
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


async def nhentai_code(interaction, numbers):
    options = Options()
    options.add_argument('--headless=new')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://nhentai.to/g/" + numbers)

    # img = driver.find_element("xpath", '//*[@id="cover"]/a/img') # website doesn't load img
    header = driver.find_element("xpath", '//*[@id="info"]/h1')
    tags = driver.find_element("xpath", '//*[@id="tags"]/div[1]/span')
    # artists = driver.find_element("xpath", '//*[@id="tags"]/div[1]/span')
    # pages = driver.find_element("xpath", '//*[@id="tags"]/div[1]/span')
    # content = driver.find_elements("id", "tags")

    test = tags.text
    # a = img.get_attribute("src")

    pattern = re.compile(r'\b\d+\b')
    result_string = re.sub(pattern, '', test)
    result_list = [item.strip() for item in result_string.split(' ') if item.strip()]
    result_str = ', '.join(result_list)

    """ for i, div in enumerate(content):
        embed = discord.Embed(
            colour=discord.Color.dark_red(),
            description=f'{div.text}'
            )
                #embed.add_field(name="Known errors, cuz website is shit", value="Images are currently broken\nTags might also break", inline=False)
        embed.set_author(name=header.text, url="https://nhentai.to/g/" + code)
        embed.set_footer(text="https://nhentai.to/g/" + code, icon_url="https://cdn.discordapp.com/attachments/636390466073526284/987148482328526938/logo.090da3be7b51.png") """
    # test = driver.find_elements("id", "tags")
    # for i, div in enumerate(test):
    embed = discord.Embed(
        colour=discord.Color.dark_red(),
        description=f'**Tags:** {result_str}'
        # description=f'{div.text}'
    )
    embed.add_field(name="[WIP]", value="⚬ Tags might break", inline=False)
    embed.set_author(name=header.text, url="https://nhentai.to/g/" + numbers)
    embed.set_footer(text="https://nhentai.to/g/" + numbers,
                     icon_url="https://cdn.discordapp.com/attachments/636390466073526284/987148482328526938/logo.090da3be7b51.png")
    # embed.set_image(url=a)

    # embed.set_image(url="https://cdn.dogehls.xyz/galleries/2362822/cover.jpg")
    file = discord.File("pic.png")
    embed.set_image(url="attachment://pic.png")

    # print(f'#{i}\n{div.text}')

    # embed.set_thumbnail(url=a)
    # embed.set_image(url=a)
    # time.sleep(0.5)
    S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
    driver.set_window_size(S('Width'),
                           S('Height'))  # May need manual adjustment
    driver.find_element("xpath", "//*[@id='cover']/a/img").screenshot('pic.png')

    driver.quit()

    # return await msg.channel.send(file=file, embed=embed, reference=msg)
    return await interaction.followup.send(file=file, embed=embed)

# TODO
# Put all divs in a list
# If there are parodies, then embed one with parodies and tags
# If not, then just tags.

# Try to fix tag spaces
