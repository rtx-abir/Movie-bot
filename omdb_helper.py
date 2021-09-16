import json
import os
import requests

omdb_base_url = "http://www.omdbapi.com/?i=tt3896198"
omdb_key = os.environ["OMDB_key"]


#OMDB movie search
def get_poster(movie_title):
    url = f"{omdb_base_url}&apikey={omdb_key}&t={movie_title}&r=json"
    response = requests.get(url)
    data = response.json()
    #print(json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False))
    return data





