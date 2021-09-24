import discord
import requests
import json
# import datetime
from discord_components import *

#tmdb workflow start
try:
    tmdb_data = tmdb_search(mov_title)
    tmdb_data = tmdb_data["results"][0]
    mov_title = tmdb_data["original_title"]
    poster_path = tmdb_data["poster_path"]
    backup_poster = f"https://image.tmdb.org/t/p/w500{poster_path}"
except:
    pass

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


async def button_helper(message, **kwargs):
	await message.channel.send(
	    "Movie links",
	    components=[[
	        Button(style=ButtonStyle.URL,
	               label="Netflix",
	               url=kwargs["netflix_link"],
	               disabled=kwargs["isNotNetflix"],
	               emoji=discord.PartialEmoji(name="Netflix",
	                                          id=887778799536721921)),
	        Button(style=ButtonStyle.URL,
	               label="Prime Video",
	               url=kwargs["amazon_link"],
	               disabled=kwargs["isNotAmazon"],
	               emoji=discord.PartialEmoji(name="APV",
	                                          id=887781807624421427)),
	        Button(style=ButtonStyle.URL,
	               label="TMDB",
	               url=kwargs["TMDB"],
                   disabled=kwargs["isNotTMDB"],
	               emoji=discord.PartialEmoji(name="TMDB",
	                                          id=887911819002404904))
	]])

async def button_helper_dos(message, embed ):
        await message.channel.send(embed=embed, 
            components= [[
                Button(style = ButtonStyle.blue, 
                    label="More Info",
                    custom_id = embed.title + "1"),
                Button(style = ButtonStyle.green, 
                    label="Add to watchlist", 
                    custom_id = embed.title)
        ]])


#help command
async def helper(message):
	embed = discord.Embed(title='Help',
	                      description='All bot commands start with uwu',
	                      color=discord.Colour.blue())

	# embed.add_field(name='hi', value='Hi', inline=False)
	# embed.add_field(name='adage', value='A fact', inline=False)
	# embed.add_field(name='quote', value='Quote', inline=False)
	# embed.add_field(name='inspiring quote', value='Inspiration', inline=False)
	embed.add_field(name='```am [movie name]```', value='l\tAdd a movie to the watchlist', inline=False)
	embed.add_field(name='```rm [movie name]```', value='l\tRemove a movie from the watchlist', inline=False)
	embed.add_field(name='```mw [movie name]```', value='l\tYour movie watchlist', inline=False)
	embed.add_field(name='```mf [movie name]```', value='l\tInfo about a movie', inline=False)
	embed.add_field(name='```cl```', value='l\tClears all movies from the watchlist', inline=False)
	embed.add_field(name='```trending```', value='l\tDisplays 5 random movies from a list of the top 200 trending movies', inline=False)
	embed.add_field(name='```rw [movie name] (1-5)```', value='l\tSubmit a rating of 1-5 for a movie', inline=False)
	embed.add_field(name='''rl''', value='Displays server reviewed movies', inline=False)
	embed.set_thumbnail( 
	    url=
	    'https://pbs.twimg.com/media/EBiczvXW4AA8MZr.jpg'
	)

	#Grabs current time for footers
	# embed.timestamp = datetime.datetime.utcnow()
	# embed.set_footer(text='\u200b')

	await message.channel.send(embed=embed)
