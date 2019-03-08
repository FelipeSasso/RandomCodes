from bs4 import BeautifulSoup
from datetime import date
import json
import requests
from requests.exceptions import ConnectionError

dict_banner_names = {
    "vip19plus": "movie-cat-wrap banner-vip19plus",
    "regular": "movie-cat-wrap banner-regular",
    "regular_3d": "movie-cat-wrap banner-regular_3d",
    "dbox_3d_avx_atmos": "movie-cat-wrap banner-ultraavx_3d_atmos_dbox",
    "ultra_avx_3d_atmos": "movie-cat-wrap banner-ultraavx_3d_atmos",
    "dbox_avx_atmos": "movie-cat-wrap banner-ultraavx_atmos_dbox",
    "ultra_avx_atmos": "movie-cat-wrap banner-ultraavx_atmos"
}

def get_all_movies():
    beautiful_soup = BeautifulSoup(get_html_text(), 'html.parser')
    return beautiful_soup.findAll("div", {"class": "showtime-single"})

def get_html_text():

    base_url = "https://www.cineplex.com/Showtimes/any-movie/cineplex-cinemas-lansdowne-and-vip?Date={}"

    try:
        return requests.get(base_url.format(date.today().strftime("%m/%d/%Y"))).text
    except ConnectionError:
        print("No internet")
        quit()

class Movie():
    def __init__(self, resultset):
        self.resultset = resultset

    def get_movie_title(self):
        return self.resultset.findAll("a", {"class" : "movie-details-link-click"})[0].get_text().strip()

    def get_movie_duration(self):
        return self.resultset.findAll("span")[1].get_text()

    def get_showtimes_list(self):
        return self.resultset.findAll("div", {"class" : "grid__item one-whole"})

def has_showtime(movie_times, key):
    return len(movie_times.findAll("div", {"class": dict_banner_names[key]}))


def get_movie_info(movie_data):

    dict_movie_details = {}
    movie = Movie(movie_data)

    dict_movie_details['title'] = movie.get_movie_title()
    dict_movie_details['duration'] = movie.get_movie_duration()

    for showtimes in movie.get_showtimes_list():
        for key in dict_banner_names.keys():
            if(has_showtime(showtimes, key)):
                dict_movie_details[key] = []
                for time in showtimes.findAll("li"):
                    dict_movie_details[key].append(time.get_text().strip())

    return dict_movie_details

id = 0
dict_movies_details = {}
for movie_data in get_all_movies():
    dict_movies_details[id] = get_movie_info(movie_data)
    id += 1

print(json.dumps(dict_movies_details))
