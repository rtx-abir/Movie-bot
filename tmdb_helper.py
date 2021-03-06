import json
import os
import requests
from random import sample
from justwatch import JustWatch

tmdb_base_url = "https://api.themoviedb.org/3/"
tmdb_key = os.environ["TMDB_key"]

api_requests = {
        "fetchTrending": f'trending/movie/week?api_key={tmdb_key}&language=en-US',
        "fetchNetflixOriginals": f'discover/tv?api_key={tmdb_key}&with_networks=213',
        "fetchTopRated": f'movie/top_rated?api_key={tmdb_key}&language=en-US',
        "fetchActionMovies": f'discover/movie?api_key={tmdb_key}&with_genres=28',
        "fetchComedyMovies": f'discover/movie?api_key={tmdb_key}&with_genres=35',
        "fetchHorrorMovies": f'discover/movie?api_key={tmdb_key}&with_genres=27',
        "fetchRomanceMovies": f'discover/movie?api_key={tmdb_key}&with_genres=10749',
        "fetchDocumentaries": f'discover/movie?api_key={tmdb_key}&with_genres=99',
}

# define trending
def tmdb_trending():

	random_list = sample(range(0, 199), 5)
	random_list.sort()
	movie_trend_list =[]

	for num in random_list:
		q, mod = divmod(num,20)

		if q == 0:
			q = 1

		url = tmdb_base_url + f'trending/movie/week?api_key={tmdb_key}&language=en-US&page={q}'
		response = requests.get(url)
		movie_trend_list.append(response.json()["results"][mod])

	return movie_trend_list
	
		#print(response.json()["results"][mod]) 
		#print(json.dumps(response.json()["results"][mod], indent=4, sort_keys=True, ensure_ascii=False))

	# page_dict = {0:[],
	# 			    1:[],
	# 				2:[],
	# 				3:[],
	# 				4:[]}
	# print(random_list)
	# for num in random_list:
	# 	q, mod = divmod(num,20)
	# 	page_dict[q].append(mod)
	# print(page_dict)
	# for keys in page_dict.keys():
	# 	if len(page_dict[keys]) == 0:
	# 		continue
	# 	else:
	# 		url = tmdb_base_url + f'trending/movie/week?api_key={tmdb_key}&language=en-US&page={keys+1}'
	# 		response = requests.get(url)
	# 		for x in page_dict[keys]:
	# 			print(json.dumps(response.json()["results"][x], indent=4, sort_keys=True, ensure_ascii=False))

# search for a movie using keyword
def tmdb_search(mov_title):
    url = tmdb_base_url+"search/movie?api_key="+tmdb_key+"&query="+mov_title
    response = requests.get(url)

    #print(json.dumps(response.json(), indent=4, sort_keys=True, ensure_ascii=False))
    return response.json()


#TMDB title search to validate api
# def title_validator(mov_title):
#     url = tmdb_base_url+"search/movie?api_key="+tmdb_key+"&query="+mov_title
#     response = requests.get(url)
#     data = response.json()

    # returns complete title from api if validation success or empty title if validation failure
    # if data["total_results"] != 0:
    #     return data["results"][0]["original_title"], True
    # else:
    #     return '', False

#TMDB title search to validate api but for watched movies because I don't know how it works
def title_validator(wch_title):
    url = tmdb_base_url+"search/movie?api_key="+tmdb_key+"&query="+wch_title
    response = requests.get(url)
    data = response.json()

    # returns complete title from api if validation success or empty title if validation failure
    if data["total_results"] != 0:
        return data["results"][0]["original_title"], True
    else:
        return '', False

def trending_daily():
    url = f"{tmdb_base_url}trending/movie/day?api_key={tmdb_key}"
    response = requests.get(url)
    #return response
    print(json.dumps(response.json(), indent=4, sort_keys=True, ensure_ascii=False))


def genre_list():
    url = f"{tmdb_base_url}genre/movie/list?api_key={tmdb_key}"
    response = requests.get(url)
    #print(json.dumps(response.json(), indent=4, sort_keys=True, ensure_ascii=False))


def movie_watchlinks(movie_id):
    url = f"{tmdb_base_url}movie/{movie_id}/watch/providers?api_key={tmdb_key}"
    response = requests.get(url)
    #print(json.dumps(response.json()["results"]["US"], indent=4, sort_keys=True, ensure_ascii=False))
    #print()
    return response.json()["results"]["US"]["link"]



# Helps get weblinks for amazon and netflix
def just_watch_api(movie_name):
    just_watch = JustWatch(country='US')


    # boolean values
    netflix = False
    amazon = False

    #default links so the component library doesnt crash
    netflix_link = 'https://www.netflix.com/'
    amazon_link = 'https://www.amazon.com/Amazon-Video/b?ie=UTF8&node=2858778011'

    results = just_watch.search_for_item(query=movie_name)
    #print(json.dumps(results["items"][0]['offers'][0], indent=4, sort_keys=True, ensure_ascii=False))

    #parsing through the data and finding amazon and netflix links
    try:
        for item in results["items"][0]['offers']:
            if item["provider_id"] == 8 and netflix == False:
                netflix_link = item['urls']['standard_web']
                if netflix_link != 'https://www.netflix.com/':
                    netflix = True
            if item["provider_id"] == 582 or item["provider_id"] == 10 and amazon == False:
                amazon_link = item['urls']['standard_web']
                if amazon_link != 'https://www.amazon.com/Amazon-Video/b?ie=UTF8&node=2858778011':
                    amazon = True
            if netflix and amazon:
                break
    except:
        pass
            
    return not netflix, not amazon, netflix_link, amazon_link


