import requests
from movies_task.settings import OMDB_API_KEY

def get_movie(title):
    return requests.get('http://www.omdbapi.com/?t=' +str(title)+ '&type=movie&apikey=' + str(OMDB_API_KEY)).json()