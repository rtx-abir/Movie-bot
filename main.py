import os
import discord
from replit import db
from helper import *
from youtube_api import video_search
from tmdb_helper import *
from movie_helper import *

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
            await channel.send('Beep Boop! I have risen! TREMBLE in fear mortals of my mere presence. If you need help please use the "UwU help" command.')
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
        await am_func(message)

    if message.content.startswith(f'{command_pref} rm'):
        await rm_func(message)

    if message.content.startswith(f'{command_pref} mw'):
        await mw_func(message)
#moviefind
    if message.content.startswith(f'{command_pref} mf'):
        await mf_func(message)

    if message.content.startswith(f'{command_pref} ra'):
        await ra_func(message)

    if message.content.startswith(f'{command_pref} button'):
        await message.channel.send(fortune)

#Help
    if message.content.startswith(f'{command_pref} help'):
        await helper(message)

client.run(os.environ['Token'])

#to do
#post movie reviewss
#movie review list
#grab movie from fmovies
