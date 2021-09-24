import os
import discord
from replit import db
from helper import *
from youtube_api import video_search
from tmdb_helper import *
from movie_helper import *
from server import keep_alive
from discord_components import interaction


client = discord.Client()
command_pref = "uwu"

@client.event
async def on_ready():
    DiscordComponents(client)
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_guild_join(guild):
    db["mov_"+str(guild.id)] = []
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send('Beep Boop! I have risen! TREMBLE in fear mortals of my mere presence. If you need help please use the "uwu help" command.')
        break




@client.event
async def on_guild_remove(guild):
    if "mov_"+str(guild.id) in db.prefix("mov_"):
        del db["mov_"+str(guild.id)]

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(f'{command_pref} hi'):
        await message.channel.send('Hello!')

    if message.content.startswith(f'{command_pref} adage'):
        fortune = get_fortune()
        await message.channel.send(fortune)

    if message.content.startswith(f'{command_pref} quote'):
        await quote_embed(message)

    if message.content.startswith(f'{command_pref} inspiring quote'):
        embed = discord.Embed(title='"In three words I can sum up everything I have learned about life: it goes on. -Robert Frost"')
        await message.channel.send(embed=embed)

    if message.content.startswith(f'{command_pref} tmdb'):
        trending_daily()
        #genre_list()

        
#Movie Stuff
    if message.content.startswith(f'{command_pref} am'):
        msg = message.content
        movie_title = msg.split('am ', 1)[1].lower()
        await am_func(message, movie_title, message.author)

    if message.content.startswith(f'{command_pref} rm'):
        msg = message.content
        movie_title = msg.split('rm ', 1)[1].lower()
        await rm_func(message, movie_title, message.author)

    if message.content.startswith(f'{command_pref} mw'):
        await mw_func(message)

        while True:
            res = await client.wait_for(event="button_click")

            if res.channel == message.channel and res.message.components[0].components[0].label.startswith("Remove"):
                    res.message.components[0].components[0].disabled = True
                    await res.respond(
                        type=7,
                        content = f"{res.component.custom_id} was requested to be removed",components=res.message.components
                    )
                    author_name=res.author
                    await rm_func(message, res.component.custom_id,author_name)

            
#moviefind
    if message.content.startswith(f'{command_pref} mf'):       
        #msg splitting/preprocessing
        msg = message.content
        mov_title = msg.split('mf ', 1)[1].lower()
        await mf_func(message,mov_title)

    if message.content.startswith(f'{command_pref} cl'):
        await ra_func(message, message.author)

    if message.content.startswith(f'{command_pref} trending'):
        await trending(message)

        while True:
            res = await client.wait_for(event="button_click")
            if res.channel == message.channel and res.component._label.startswith("Add"):
                res.message.components[0].components[1].disabled = True
                await res.respond(
                    type=7,
                    content = f"{res.component.custom_id} was requested to be added",components=res.message.components
                )
                author_name=res.author
                await am_func(message, res.component.custom_id,author_name)

            elif res.channel == message.channel and res.component._label.startswith("More"):
                movie_name = res.component.custom_id.split("1")[0]
                await res.respond(
                    type=7,
                    content = f"More Information was requested for {movie_name}",
                    components=res.message.components
                )
                author_name=res.author
                await mf_func(message, movie_name)

#Reviews		
    if message.content.startswith(f'{command_pref} rw'):  
        await review(message)
    if message.content.startswith(f'{command_pref} rl'):  
        await reviews(message)
        

#Help
    if message.content.startswith(f'{command_pref} help'):
        await helper(message)

keep_alive()
client.run(os.environ['Token'])

#to do
#post movie reviewss
#movie review list
#grab movie from fmovies
