import discord
from replit import db
from helper import button_helper
from  discord_components import *
from youtube_api import video_search
from omdb_helper import get_poster
from tmdb_helper import tmdb_search, title_validator, movie_watchlinks, just_watch_api


##################################################################
#|                    Movie Finder/ Search function             |#
##################################################################

async def mf_func(message):

    #msg splitting/preprocessing
    msg = message.content
    mov_title = msg.split('mf ', 1)[1].lower()

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
        embed.add_field(name="Rated",value=movie_data["Rated"],inline=True)
    except:
        embed.add_field(name="Rated",value="N/A",inline=True)

    
    #embed imaging/poster path
    if movie_data['Poster'] == 'N/A':
        if poster_path == "":
            embed.set_image(
                url=
                "https://cdn.searchenginejournal.com/wp-content/uploads/2020/08/404-pages-sej-5f3ee7ff4966b-760x400.png"
            )
        else:
            embed.set_image(url=backup_poster)
    else:
        embed.set_image(url=movie_data['Poster'])


    # watchlinks
    tmdb_link = movie_watchlinks(tmdb_data["id"])
    isNotNetflix, isNotAmazon, netflix_link, amazon_link = just_watch_api(mov_title)
   
    try:
        await button_helper(message, **{"TMDB":tmdb_link, 
                                        "netflix_link":netflix_link, "amazon_link":amazon_link,
                                        "isNotNetflix":isNotNetflix,
                                        "isNotAmazon":isNotAmazon})
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
        release_year = movie_data['Year']
    except:
        release_year = ''

    try:
        await message.channel.send("https://youtube.com/watch?v="+video_search(mov_title, release_year))
    except:
        await message.channel.send("Beep Boop! no youtube video was found! your 100 youtube video limit might have been reached...")




##################################################################
#|                      Add Movie to Queue                      |#
##################################################################


async def am_func(message):
    msg = message.content
    movie_title = msg.split('am ', 1)[1].lower()

    #validates if the movie title exists in the TMDB api
    movie_title, is_val = title_validator(movie_title)
    if (is_val):
        if (add_movie_title(movie_title, message.guild.id)):
            await message.channel.send(f"{movie_title} was added to list")
        else:
            await message.channel.send(f"{movie_title} is already in the list")
    else:
        await message.channel.send(
            "Movie does not exist, Please check spelling!")


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


async def rm_func(message):
    msg = message.content
    movie_title = msg.split('rm ', 1)[1].lower()

    movie_title, is_val = title_validator(movie_title)

    if(is_val):
        try:
            db['mov_'+str(message.guild.id)].remove(movie_title)
            await message.channel.send(f"{movie_title} was removed from the list")
        except:
            await message.channel.send(f"{movie_title} was not found in the list")
    else:
        await message.channel.send("No movie exists in that name")



##################################################################
#|                 Clear movie Queue (delete all)               |#
##################################################################

async def ra_func(message):
    db['mov_'+str(message.guild.id)] = []
    await message.channel.send("List was reset")





##################################################################
#|                       Print movie Queue                      |#
##################################################################

#See movie list
def see_movie_list(guild_id):
    return db['mov_'+str(guild_id)]


#Embed for movie watchlist
async def mw_func(message):

    movie_list = see_movie_list(message.guild.id)
    if len(movie_list) == 0:
        await message.channel.send("Movie watchlist is empty!")
        return


    # top 5 movies from the top of queue
    x = 5 if len(movie_list) > 5 else int(len(movie_list))
    

    #printing an embed for each of the 5 movies
    for movie in movie_list[:x]:

        # OMDB workflow begins here
        movie_data = get_poster(movie)

        #Title, Description of Embed
        embed = discord.Embed(title=movie,
                              description=movie_data['Plot'],
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
                            value=movie_data["release_date"],
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
            embed.add_field(name="Rated",
                            value=movie_data["Rated"],
                            inline=True)
        except:
            embed.add_field(name="Rated",value="N/A",inline=True)


        # poster/image of movie
        if movie_data['Poster'] == 'N/A':
            embed.set_image(
                url=
                "https://cdn.searchenginejournal.com/wp-content/uploads/2020/08/404-pages-sej-5f3ee7ff4966b-760x400.png"
            )
        else:
            embed.set_image(url=movie_data['Poster'])


        #send the embed then repeat loop till 5 movies are printed
        await message.channel.send(embed=embed)




        

