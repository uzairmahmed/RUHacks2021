'''
    May 1, 2021
    Uzair Ahmed

    Discord Bot
'''

from discord import Game
from discord.ext import commands

# BOT VARIABLES
token="ODM3OTU1NjYzMDQ5MTMwMDM0.YI0FBg.2kGS2lPvj9BZC2lJL4CLJLs7ckg"
bot = commands.Bot(command_prefix='-cloud ')
# startup_extensions = ["adminbot", "imagebot", "searchbot", "soundbot", "chatbot", "gamblebot"]

# Client Methods
@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=Game(name='with Google Cloud Console'))

@bot.event
async def on_command_error(context, error):
    if isinstance(error, commands.CommandNotFound):
        await context.send("huh") 

if __name__ == "__main__":
    # for extension in startup_extensions:
    #     try:
    #         bot.load_extension(extension)
    #     except Exception as e:
    #         exc = '{}: {}'.format(type(e).__name__, e)
    #         print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(token)
