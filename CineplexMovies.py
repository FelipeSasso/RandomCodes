"""
I wrote this code because I don't like Cineplex website. 
I use this code only when I need to check what movies they have on a specific date.
"""

from bs4 import BeautifulSoup
import requests
import json
from datetime import date

banner_names_dict = {
    "vip19plus": "movie-cat-wrap banner-vip19plus",
    "regular": "movie-cat-wrap banner-regular",
    "regular_3d": "movie-cat-wrap banner-regular_3d",
    "dbox_3d_avx_atmos": "movie-cat-wrap banner-ultraavx_3d_atmos_dbox",
    "ultra_avx_3d_atmos": "movie-cat-wrap banner-ultraavx_3d_atmos",
    "dbox_avx_atmos": "movie-cat-wrap banner-ultraavx_atmos_dbox",
    "ultra_avx_atmos": "movie-cat-wrap banner-ultraavx_atmos"
}


class MoviesList(BeautifulSoup):

    def __init__(self, html_text, parser):
        super().__init__(html_text, parser)

    def get_all_movies(self):
        return self.findAll("div", {"class": "showtime-single"})

class Movie():
    def __init__(self, resultset):
        self.resultset = resultset

    def get_movie_title(self):
        return self.resultset.findAll("a", {"class" : "movie-details-link-click"})[0].get_text().strip()

    def get_movie_duration(self):
        return self.resultset.findAll("span")[1].get_text()

    def get_times_list(self):
        return self.resultset.findAll("div", {"class" : "grid__item one-whole"})

def get_page():

    base_url = "https://www.cineplex.com/Showtimes/any-movie/cineplex-cinemas-lansdowne-and-vip?Date={}"

    try:
        return requests.get(base_url.format(date.today().strftime("%d/%m/%Y")))
    except ConnectionError:
        print("Sem internet")

def get_movies_info(movie_result):

    dict_movie_details = {}
    movie = Movie(movie_result)

    dict_movie_details['title'] = movie.get_movie_title()
    dict_movie_details['duration'] = movie.get_movie_duration()

    for movie_times in movie.get_times_list():
        for key in banner_names_dict.keys():
            if(len(movie_times.findAll("div", {"class": banner_names_dict[key]}))):
                dict_movie_details[key] = []
                for time in movie_times.findAll("li"):
                    dict_movie_details[key].append(time.get_text().strip())

    return dict_movie_details

r = get_page()

bs = MoviesList(r.text, 'html.parser')

# import pdb; pdb.set_trace()

id = 0
dict = {}
for movie_result in bs.get_all_movies():
    dict[id] = get_movies_info(movie_result)
    id += 1

print(dict)
