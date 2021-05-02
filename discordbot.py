'''
    May 1, 2021
    Uzair Ahmed, Arjun Dureja, Niranjan Krishnaswamy, Jason Sayroo

    Discord Bot
'''

from discord import Game, File
from discord.ext import commands

# Functions
import sys, json
sys.path.append('functions')
from text import translate_text
from search import search_google, image_search
from vision import ocr, identify
from maps import streetAndMapsView, placeInfo, placeDescription
from tts import text_to_speech
from sentimentAnalysis import analyze_sentiment


with open('more_keys.json', 'r') as f:
    keys = json.load(f)
    f.close()

dckey = keys["discord_token"]

# BOT VARIABLES
token=dckey
bot = commands.Bot(command_prefix='-c ')

yesmoji = '\N{THUMBS UP SIGN}'
noemoji = '\N{THUMBS DOWN SIGN}'
prevemoji = u"\u25C0"
nextemoji = u"\u25B6"

image_cache = []
IMAGE_CACHE_SIZE=10

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

@bot.command(name='map', help='Map and street view of location [-c map ryerson university]')
async def map(context):
    try:
        await context.send((' ').join(streetAndMapsView(context.message.content[7:])))
    except Exception as e:
        print(e)

@bot.command(name='place', help='Get details about a place [-c place walmart]')
async def map(context):
    try:
        place = placeInfo(context.message.content[9:])
        placeDesc = placeDescription(place['candidates'][0]['place_id'])
        formatted_place = '''**Name:** '''+place['candidates'][0]['name']+'''
**Address:** '''+place['candidates'][0]['formatted_address']+'''
**Phone Number:** '''+str(placeDesc['result']['formatted_phone_number'])+'''
**Google Rating:** '''+str(place['candidates'][0]['rating'])+'''/5
**Longitude:** '''+str(place['candidates'][0]['geometry']['location']['lat'])+'''
**Latitude:** '''+str(place['candidates'][0]['geometry']['location']['lng'])

        await context.send(formatted_place)
    except Exception as e:
        print(e)

@bot.command(name='tts', help='Text to speech [-c tts hello]')
async def tts(context):
    try:
        text = context.message.content[7:]
        text_to_speech(text)
        with open('ttsFile.mp3', 'rb') as f:
            await context.send(file=File(f, 'TTS.mp3'))
    except Exception as e:
        print(e)

@bot.command(name='img', help='Get first result from Google Images [-c img dog]')
async def image(context):
    try:
        query = context.message.content[7:]
        if len(query) == 0:
            await context.send("you forgot to add a query dumbass")
            return

        temp_msg = await context.send("https://i.imgur.com/crzmhsy.gif")
        image_urls = image_search(query)
        if image_urls:
            temp_cache_payload = {
                "msg_id": temp_msg.id,
                "urls" : image_urls,
                "index" : 0
            }

            image_cache.append(temp_cache_payload)
            if IMAGE_CACHE_SIZE < len(image_cache):
                image_cache.pop(0)

            await temp_msg.edit(content=image_urls[0])
            await temp_msg.add_reaction(prevemoji)
            await temp_msg.add_reaction(nextemoji)
        else:
            print("NOT FOUND")
            await temp_msg.edit(content="https://media3.giphy.com/media/3zhxq2ttgN6rEw8SDx/giphy.gif")
            await context.message.add_reaction(noemoji)
    except Exception as e:
        print(e)

@bot.event
async def on_reaction_add(reaction,user):
    if user.name != 'CloudBot':
        for i in image_cache:
            if i['msg_id'] == reaction.message.id:
                if reaction.emoji == nextemoji:
                    i['index'] += 1
                    if i['index'] == len(i['urls']):
                        i['index'] = 0
                    temp_url = i['urls'][i['index']]
                    await reset_img_msg(reaction, temp_url)
                elif reaction.emoji == prevemoji:
                    i['index'] -= 1
                    if i['index'] == -1:
                        i['index'] = len(i['urls'])-1
                    
                    temp_url = i['urls'][i['index']]
                    await reset_img_msg(reaction, temp_url)

@bot.command(name='sentiment', help='Analyse the sentiment of a sentence [-c sentiment how are you]')
async def sentiment(context):
    try:
        result = analyze_sentiment(context.message.content[13:])
        await context.send('Score: ' + str(round(result[0], 3)) + '\nMagnitude: ' + str(round(result[1], 3)))
    except Exception as e:
        print(e)
    
async def reset_img_msg(reaction, temp_url):
    await reaction.message.edit(content=temp_url)
    await reaction.message.clear_reactions()
    await reaction.message.add_reaction(prevemoji)
    await reaction.message.add_reaction(nextemoji)

if __name__ == "__main__":
    # for extension in startup_extensions:
    #     try:
    #         bot.load_extension(extension)
    #     except Exception as e:
    #         exc = '{}: {}'.format(type(e).__name__, e)
    #         print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(token)
