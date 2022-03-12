import discord
import json
import random
from replit import db
from helper import button_helper, button_helper_dos
from  discord_components import *
from youtube_api import video_search
from omdb_helper import get_poster
from tmdb_helper import tmdb_search, title_validator, movie_watchlinks, just_watch_api, tmdb_trending
from datetime import date #for adding to watchedlist 

##################################################################
#|                    Movie Finder/ Search function             |#
##################################################################

async def mf_func(message, mov_name):

    mov_title = mov_name
    #tmdb workflow start
    try:
        tmdb_data = tmdb_search(mov_title)
        tmdb_data = tmdb_data["results"][0]
        mov_title = tmdb_data["original_title"]
        poster_path = tmdb_data["poster_path"]
        backup_poster = f"https://image.tmdb.org/t/p/w500{poster_path}"
    except:
        pass


    #omdb workflow start
    movie_data = get_poster(mov_title)



    #embed start: title, description, color
    try:
        embed = discord.Embed(title=mov_title.title(),
                              #movie_data['Plot'] works too tmdb has better descriptions
                              description=tmdb_data['overview'],
                              color=discord.Colour.blue())
    except:
        await message.channel.send("Movie was not found, Please check spelling"
                                   )
        return

    #embed ratings: IMDB
    try:
        embed.add_field(name='IMDB',
                        value=movie_data['Ratings'][0]['Value'],
                        inline=True)
    except:
        embed.add_field(name='IMDB', value="N/A", inline=True)

    #embed ratings: Rotten Tomatoes
    try:
        embed.add_field(name='Rotten Tomatoes',
                        value=movie_data['Ratings'][1]['Value'],
                        inline=True)
    except:
        embed.add_field(name='Rotten Tomatoes', value="N/A", inline=True)

    #embed ratings: Metacritic
    try:
        embed.add_field(name='Metacritic',
                        value=movie_data['Ratings'][2]['Value'],
                        inline=True)
    except:
        embed.add_field(name='Metacritic', value="N/A", inline=True)


    #embed release date
    try:
        embed.add_field(name="Release Date",value=tmdb_data["release_date"],inline=True)
    except:
        embed.add_field(name="Release Date",value="N/A",inline=True)

    #embed Runtime
    try:
        embed.add_field(name="Runtime",value=movie_data["Runtime"],inline=True)
    except:
        embed.add_field(name="Runtime",value="N/A",inline=True)

    #embed Rating
    try:
        if tmdb_data["adult"] == True:
            custom_rating = "R"
        else:
            custom_rating = "PG-13"

        embed.add_field(name="Rated",value=custom_rating,inline=True)
    except:
        embed.add_field(name="Rated",value="N/A",inline=True)

    
    #embed imaging/poster path
    try:
        embed.set_image(url=f"https://image.tmdb.org/t/p/w500{poster_path}")
    except:
        embed.set_image(
                    url=
                    "https://cdn.searchenginejournal.com/wp-content/uploads/2020/08/404-pages-sej-5f3ee7ff4966b-760x400.png"
                )


    # watchlinks
    isNotTMDB = False
    try:
        tmdb_link = movie_watchlinks(tmdb_data["id"])
    except:
        isNotTMDB = True

    isNotNetflix, isNotAmazon, netflix_link, amazon_link = just_watch_api(mov_title)
   
    try:
        await button_helper(message, **{"TMDB":tmdb_link, 
                                        "netflix_link":netflix_link, "amazon_link":amazon_link,
                                        "isNotNetflix":isNotNetflix,
                                        "isNotAmazon":isNotAmazon,
                                        "isNotTMDB":isNotTMDB})
    except:
        await message.channel.send("Movie Link Error", 
                                    components=[[Button(style=ButtonStyle.red,
                                    label = "No Movie links was found!",
                                    disabled=True)]])


    #send embed
    await message.channel.send(embed=embed)
    


    # Youtube api call
    
    #release year for youtube api call
    try:
        release_year = tmdb_data["release_date"].split("-")[0]
    except:
        release_year = ''

    try:
        await message.channel.send("https://youtube.com/watch?v="+video_search(mov_title, release_year))
    except:
        await message.channel.send("Beep Boop! no youtube video was found! your 100 youtube video limit might have been reached...")




##################################################################
#|                      Add Movie to Queue                      |#
##################################################################


async def am_func(message, mov_title, author):
    

    #validates if the movie title exists in the TMDB api
    movie_title, is_val = title_validator(mov_title)
    if (is_val):
        if (add_movie_title(movie_title, message.guild.id)):
            await message.channel.send(f"{movie_title} was added to list by {author.mention} ✅")
        else:
            await message.channel.send(f"{movie_title} is already in the list, {author.mention} ✅")
    else:
        await message.channel.send(
            f"Movie does not exist, Please check spelling!, {author.mention} ❌")


#Adding movie to database queue
def add_movie_title(movie_title, guild_id):
    # checking if server has database entry
    if 'mov_'+str(guild_id) in db.keys():
        movies = db['mov_'+str(guild_id)]

        #checking for movie title in server's queue
        if movie_title not in movies:
            #add movie to the list
            movies.append(movie_title)
        else:
            return False
        db['mov_'+str(guild_id)] = movies
        return True

    # if no db entry for server. then make one
    else:
        db['mov_'+str(guild_id)] = [movie_title]
        return True




##################################################################
#|                 Remove Movie from Queue                      |#
##################################################################


async def rm_func(message,mov_title, author):
    

    movie_title, is_val = title_validator(mov_title)

    if(is_val):
        try:
            db['mov_'+str(message.guild.id)].remove(movie_title)
            await message.channel.send(f"{movie_title} was removed from the list by {author.mention} ✅")
        except:
            await message.channel.send(f"{movie_title} was not found in the list, {author.mention}  ❌")
    else:
        await message.channel.send(f"No movie exists in that name, {author.mention}    ❌")



##################################################################
#|                 Clear movie Queue (delete all)               |#
##################################################################

async def ra_func(message, author):
    db['mov_'+str(message.guild.id)] = []
    await message.channel.send(f"List was reset by {author.mention} ✅")





##################################################################
#|                       Print movie Queue                      |#
##################################################################

#See movie list
def see_movie_list(guild_id):
    return db['mov_'+str(guild_id)]


#Embed for movie watchlist
async def mw_func(message, list_limit = 5):

    movie_list = see_movie_list(message.guild.id)
    if len(movie_list) == 0:
        await message.channel.send("Movie watchlist is empty!")
        return


    # top 5 movies from the top of queue
    limit = list_limit
    x = limit if len(movie_list) > limit else int(len(movie_list))
    

    #printing an embed for each of the 5 movies
    for movie in movie_list[:x]:

        # OMDB workflow begins here
        movie_data = get_poster(movie)

        try:
            tmdb_data = tmdb_search(movie)
            tmdb_data = tmdb_data["results"][0]
            mov_title = tmdb_data["original_title"]
            poster_path = tmdb_data["poster_path"]
            backup_poster = f"https://image.tmdb.org/t/p/w500{poster_path}"
        except:
            pass

        #Title, Description of Embed
        embed = discord.Embed(title=movie,
                              description=tmdb_data['overview'],
                              color=discord.Colour.blue())

        #Embed Rating: IMDB
        try:
            embed.add_field(name='IMDB',
                            value=movie_data['Ratings'][0]['Value'],
                            inline=True)
        except:
            embed.add_field(name='IMDB', value="N/A", inline=True)

        #Embed Rating: Rotten Tomatoes
        try:
            embed.add_field(name='Rotten Tomatoes',
                            value=movie_data['Ratings'][1]['Value'],
                            inline=True)
        except:
            embed.add_field(name='Rotten Tomatoes', value="N/A", inline=True)


        #Embed Rating: Metacritic
        try:
            embed.add_field(name='Metacritic',
                            value=movie_data['Ratings'][2]['Value'],
                            inline=True)
        except:
            embed.add_field(name='Metacritic', value="N/A", inline=True)


        #embed release date
        try:
            embed.add_field(name="Release Date",
                            value=tmdb_data["release_date"],
                            inline=True)
        except:
            embed.add_field(name="Release Date",value="N/A",inline=True)


        #embed Runtime
        try:
            embed.add_field(name="Runtime",
                            value=movie_data["Runtime"],
                            inline=True)
        except:
            embed.add_field(name="Runtime",value="N/A",inline=True)


        #embed Rating
        try:
            if tmdb_data["adult"] == True:
                custom_rating = "R"
            else:
                custom_rating = "PG-13"

            embed.add_field(name="Rated",value=custom_rating,inline=True)
        except:
            embed.add_field(name="Rated",value="N/A",inline=True)

        
        #embed imaging/poster path
        try:
            embed.set_image(url=f"https://image.tmdb.org/t/p/w500{poster_path}")
        except:
            embed.set_image(
                        url=
                        "https://cdn.searchenginejournal.com/wp-content/uploads/2020/08/404-pages-sej-5f3ee7ff4966b-760x400.png"
                    )


        #send the embed then repeat loop till 5 movies are printed
        await message.channel.send(embed=embed, components= 
                                        [Button(style = ButtonStyle.red, 
                                        label="Remove from watchlist", 
                                        custom_id = embed.title)
        ])


async def mw2_func(message):
    # movie_data = tmdb_trending()
    # await message.channel.send("hi!", components = Select(placeholder = "Choose Movie from watchlist", options = [SelectOption(label = "option 1", description= "opt1",)] 
    # ))
    movie_list = see_movie_list(message.guild.id)
    await message.channel.send("hi!",components=
                            [Select(placeholder="Choose what you want to see!",
                            options=[
                                SelectOption(
                                    label=mov,
                                    value=mov
                                ) for mov in movie_list
                            ])], delete_after=300)

    # await message.channel.send("hi!",components=
    #                         [Select(placeholder="Choose what you want to see!",
    #                         options=[
    #                             SelectOption(
    #                                 label="Option 1",
    #                                 value="option 1"
    #                             ),
    #                             SelectOption(
    #                                 label="Option 2",
    #                                 value="option 2"
    #                             ),
    #                             SelectOption(
    #                                 label="Option 3",
    #                                 value="option 3"
    #                             )
    #                         ])], delete_after=10) 

    


##################################################################
#|                           Trending                           |#
##################################################################

async def trending(message):
    movie_data = tmdb_trending()
    
    for movies in movie_data:
        embed = discord.Embed(title=movies['original_title'],
                             	description=movies['overview'],
                             	color=discord.Colour.blue())
        embed.set_thumbnail(url=f"https://image.tmdb.org/t/p/w500{movies['poster_path']}")
        await button_helper_dos(message, embed)
    #print(json.dumps(movie_data, indent=4, sort_keys=True, ensure_ascii=False))




##################################################################
#|                      Add to watched list                     |#
##################################################################
#copied AM code lololol
async def watched(message, wch_title,author):
    
    #Current month/Year Reference because I dont know it
    todays_date = date.today()
    print("Current month:", todays_date.month)
    print("Current day:", todays_date.day)


    #validates if the movie title exists in the TMDB api
    movie_title, is_val = title_validator(wch_title)
    if (is_val):
        if (add_to_watched(movie_title, message.guild.id)):
            await message.channel.send(f"{movie_title} was added to watched list by {author.mention} ✅")
        else:
            await message.channel.send(f"{movie_title} is already in the watched list, {author.mention} ✅")
    else:
        await message.channel.send(
            f"Movie does not exist, Please check spelling!, {author.mention} ❌")


#Adding movie to database queue
def add_to_watched(movie_title, guild_id):
    # checking if server has database entry
    if 'wch_'+str(guild_id) in db.keys():
        movies = db['wch_'+str(guild_id)]

        #checking for movie title in server's queue
        if movie_title not in movies:
            #add movie to the list
            movies.append(movie_title)
        else:
            return False
        db['wch_'+str(guild_id)] = movies
        return True

    # if no db entry for server. then make one
    else:
        db['wch_'+str(guild_id)] = [movie_title]
        return True







##################################################################
#|              Remove Movie from Watched List                  |#
##################################################################

#DOESNT WORK

async def watchedremove(message,wch_title, author):
    

    movie_title, is_val = title_validator(wch_title)

    if(is_val):
        try:
            db['wch_'+str(message.guild.id)].remove(movie_title)
            await message.channel.send(f"{movie_title} was removed from the watched list by {author.mention} ✅")
        except:
            await message.channel.send(f"{movie_title} was not found in the watched list, {author.mention}  ❌")
    else:
        await message.channel.send(f"No movie exists in that name, {author.mention}    ❌")



##################################################################
#|                      Check Watched List                      |#
##################################################################

#
#
#Copied mw for now but need to change how it works since this list can just go on and on
#
#



#See movie list
def see_watched_list(guild_id):
    return db['wch_'+str(guild_id)]


#Embed for movie watchlist
async def watchedlist(message, list_limit = 5):

    movie_list = see_watched_list(message.guild.id)
    if len(movie_list) == 0:
        await message.channel.send("Movie watchlist is empty!")
        return


    # top 5 movies from the top of queue
    limit = list_limit
    x = limit if len(movie_list) > limit else int(len(movie_list))
    

    #printing an embed for each of the 5 movies
    for movie in movie_list[:x]:

        # OMDB workflow begins here
        movie_data = get_poster(movie)

        try:
            tmdb_data = tmdb_search(movie)
            tmdb_data = tmdb_data["results"][0]
            wch_title = tmdb_data["original_title"]
            poster_path = tmdb_data["poster_path"]
            backup_poster = f"https://image.tmdb.org/t/p/w500{poster_path}"
        except:
            pass

        #Title, Description of Embed
        embed = discord.Embed(title=movie,
                              color=discord.Colour.blue())
        
        #embed imaging/poster path
        try:
            embed.set_image(url=f"https://image.tmdb.org/t/p/w500{poster_path}")
        except:
            embed.set_image(
                        url=
                        "https://cdn.searchenginejournal.com/wp-content/uploads/2020/08/404-pages-sej-5f3ee7ff4966b-760x400.png"
                    )


        #send the embed then repeat loop till 5 movies are printed
        await message.channel.send(embed=embed, components= 
                                        [Button(style = ButtonStyle.red, 
                                        label="Remove from watched list", 
                                        custom_id = embed.title)
        ])









##################################################################
#|                      Add a movie review                      |#
##################################################################

async def review(message):
    await message.channel.send("https://davesamaniego2016.files.wordpress.com/2016/10/cat-catstruction-play-on-words-construction-cats-favim-com-4174852.jpeg")









##################################################################
#|                     Display review list                      |#
##################################################################

async def reviews(message):
    await message.channel.send("https://davesamaniego2016.files.wordpress.com/2016/10/cat-catstruction-play-on-words-construction-cats-favim-com-4174852.jpeg")



async def mw3_func(message,mov_title):
    movie_data = get_poster(mov_title)
    try:
        tmdb_data = tmdb_search(mov_title)
        tmdb_data = tmdb_data["results"][0]
        mov_title = tmdb_data["original_title"]
        poster_path = tmdb_data["poster_path"]
        backup_poster = f"https://image.tmdb.org/t/p/w500{poster_path}"
    except:
        pass

    #Title, Description of Embed
    embed = discord.Embed(title=mov_title,
                            description=tmdb_data['overview'],
                            color=discord.Colour.blue())

    #Embed Rating: IMDB
    try:
        embed.add_field(name='IMDB',
                        value=movie_data['Ratings'][0]['Value'],
                        inline=True)
    except:
        embed.add_field(name='IMDB', value="N/A", inline=True)

    #Embed Rating: Rotten Tomatoes
    try:
        embed.add_field(name='Rotten Tomatoes',
                        value=movie_data['Ratings'][1]['Value'],
                        inline=True)
    except:
        embed.add_field(name='Rotten Tomatoes', value="N/A", inline=True)


    #Embed Rating: Metacritic
    try:
        embed.add_field(name='Metacritic',
                        value=movie_data['Ratings'][2]['Value'],
                        inline=True)
    except:
        embed.add_field(name='Metacritic', value="N/A", inline=True)


    #embed release date
    try:
        embed.add_field(name="Release Date",
                        value=tmdb_data["release_date"],
                        inline=True)
    except:
        embed.add_field(name="Release Date",value="N/A",inline=True)


    #embed Runtime
    try:
        embed.add_field(name="Runtime",
                        value=movie_data["Runtime"],
                        inline=True)
    except:
        embed.add_field(name="Runtime",value="N/A",inline=True)


    #embed Rating
    try:
        if tmdb_data["adult"] == True:
            custom_rating = "R"
        else:
            custom_rating = "PG-13"

        embed.add_field(name="Rated",value=custom_rating,inline=True)
    except:
        embed.add_field(name="Rated",value="N/A",inline=True)

    
    #embed imaging/poster path
    try:
        embed.set_image(url=f"https://image.tmdb.org/t/p/w500{poster_path}")
    except:
        embed.set_image(
                    url=
                    "https://cdn.searchenginejournal.com/wp-content/uploads/2020/08/404-pages-sej-5f3ee7ff4966b-760x400.png"
                )


    #send the embed then repeat loop till 5 movies are printed
    # await message.channel.send(embed=embed, components= 
    #                                 [Button(style = ButtonStyle.red, 
    #                                 label="Remove from watchlist", 
    #                                 custom_id = embed.title)
    # ])
    
    return embed