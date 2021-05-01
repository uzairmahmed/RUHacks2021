'''
    May 1, 2021
    Uzair Ahmed

    Discord Bot
'''

from discord import Game
from discord.ext import commands

# Functions
import sys
sys.path.append('functions')
from text import translate_text
from search import *
from vision import ocr, identify

# BOT VARIABLES
token="ODM3OTU1NjYzMDQ5MTMwMDM0.YI0FBg.2kGS2lPvj9BZC2lJL4CLJLs7ckg"
bot = commands.Bot(command_prefix='-c ')

# Client Methods
@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=Game(name='with Google Cloud Console'))

@bot.event
async def on_command_error(context, error):
    if isinstance(error, commands.CommandNotFound):
        await context.send("huh") 

@bot.command(name='translate', help='Translate from one language to the other [-c translate fr hello]')
async def translate(context):
    try:
        args = str(context.message.content).split(' ')
        await context.send("Translate: " + translate_text(args[2], (' ').join(args[3:])))
    except Exception as e:
        print(e)

@bot.command(name='search', help='Search Google for anything and get links back [-c search cookie recipes 3')
async def search(context):
    try:
        args = str(context.message.content).split(' ')
        results = search_google((' ').join(args[2:len(args)-1]), int(args[-1]))
        for link in results:
            await context.send(link)
    except Exception as e:
        print(e)

@bot.command(name='img', help='Get first result from Google Images [-c img dog]')
async def image(context):
    try:
        args = str(context.message.content).split(' ')
        await context.send(image_search((' ').join(args[2:]))[0])
    except Exception as e:
        print(e)

@bot.command(name='ocr', help='Get text from image [-c ocr <image url>]')
async def image(context, message):
    try:
        await context.send(ocr(message))
    except Exception as e:
        print(e)

@bot.command(name='id', help='Identify object in image [-c id <image url>]')
async def image(context, message):
    try:
        await context.send('Objects found: ' + (', ').join(set(identify(message))))
    except Exception as e:
        print(e)

if __name__ == "__main__":
    # for extension in startup_extensions:
    #     try:
    #         bot.load_extension(extension)
    #     except Exception as e:
    #         exc = '{}: {}'.format(type(e).__name__, e)
    #         print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(token)
