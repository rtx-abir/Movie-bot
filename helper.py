import discord
import requests
import json
import datetime
from  discord_components import *

#API call for UwU adage
def get_fortune():
    response = requests.get("https://helloacm.com/api/fortune")
    data = json.loads(response.content)
    return data



#API call for UwU quote
def get_quote():
    response = requests.get("http://zenquotes.io/api/random")
    data = json.loads(response.content)
    rand_quote = data[0]['q'] + ' -' + data[0]['a']
    return rand_quote



#Returns embeded quote
async def quote_embed(message):
    embed = discord.Embed(title='Inspiring quote',
                          description=get_quote(),
                          color=discord.Colour.blue())
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text='\u200b')
    embed.set_image(
        url=
        "https://www.kindpng.com/picc/m/106-1065472_harold-thumbs-up-png-download-thumbs-up-meme.png"
    )
    await message.channel.send(embed=embed)


async def button_helper(message,**kwargs):
    links = list(kwargs.keys())
    await message.channel.send("Movie links",components=[[Button(style=ButtonStyle.URL,
                                        label = "Netflix", 
                                        url=kwargs["netflix_link"],
                                        disabled = kwargs["isNotNetflix"],
                                        emoji=discord.PartialEmoji(name="Netflix",id=887778799536721921)),

                                        Button(style=ButtonStyle.URL,
                                        label = "Prime Video", 
                                        url=kwargs["amazon_link"],
                                        disabled = kwargs["isNotAmazon"],
                                        emoji=discord.PartialEmoji(name="APV",id=887781807624421427)),
                                        
                                        Button(style=ButtonStyle.URL,
                                        label = "TMDB", 
                                        url=kwargs["TMDB"],
                                        emoji=discord.PartialEmoji(name="TMDB",id=887911819002404904))
                                        ]])



#help command
async def helper(message):
    embed = discord.Embed(title='Help',
                          description='All bot commands start with uwu',
                          color=discord.Colour.blue())

    embed.add_field(name='hi', value='Hi', inline=True)
    embed.add_field(name='adage', value='fuc kyou', inline=True)
    embed.add_field(name='quote', value='Quote', inline=True)
    embed.add_field(name='inspiring quote', value='inspiration', inline=True)
    embed.add_field(name='am', value='Add movie', inline=True)
    embed.add_field(name='rm', value='Remove movie', inline=True)
    embed.add_field(name='mw', value='Movie watchlist', inline=True)
    embed.add_field(name='mf', value='Movie finder', inline=True)
    embed.add_field(name='ra', value='remove all from list', inline=True)

    embed.set_thumbnail(
        url=
        'https://static.onecms.io/wp-content/uploads/sites/20/2016/08/the-rock-pancakes.jpg'
    )

    #Grabs current time for footers
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text='\u200b')

    await message.channel.send(embed=embed)
