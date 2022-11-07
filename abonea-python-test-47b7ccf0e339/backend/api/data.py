import requests

import random
import string
import logging


API_KEY = '4f5ac72c'
IMDB_URL = 'https://www.omdbapi.com/?'

# Class to retrive the OMDB API data
class Data:
    def __init__(self):
        self.api_key = API_KEY
        self.imdb_url = IMDB_URL
        #print(self.api_key)
        self.movie_dict_list = []
        
    def print_log(self,msg):
        print("======================================================================")
        print("{}".format(msg))
        print("======================================================================")

    def search_movies(self,search,movies=[]):
        url = self.imdb_url+'apikey='+self.api_key+"&"+'s={}'.format(search)
        response = requests.get(url)
        data = response.json()
        ##print(data)

        if 'Error' not in data:
            results = data['Search']
        else:
            results = []    

        for result in results:
            if len(movies) >= 100:
                return(movies)
            else:
                movies.append(result['Title'])
                self.movie_dict_list.append(result)

        movies = list(set(movies))

        if len(movies) < 100:
            letters = string.ascii_lowercase
            search = ''.join(random.choice(letters) for i in range(3))
            ##print('----')
            ##print("Len movies:",len(movies))
            ##print('------')
            movies += self.search_movies(search,movies)
            movies = list(set(movies))

        return(movies)
        
    def final_data(self):
        self.print_log("Fetching Data from OMDB API")
        movies = self.search_movies('abc')
        final_data = [i for n, i in enumerate(self.movie_dict_list) if i not in self.movie_dict_list[n + 1:]]
        self.print_log("Completed........")
        return final_data

    def get_movie_by_title(self,title):
        self.print_log("Fetching Data for specific title:{}".format(title))
        form_url = self.imdb_url+'apikey='+self.api_key+"&"+'t={}'.format(title)
        response = requests.get(form_url)
        data = response.json()
        movies = {}
       
        if 'Error' in data:
            return {"Error":"NO Movies name with title:{}".format(title)}
        else:
            return data

      
