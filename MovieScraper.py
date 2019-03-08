"""
This code scraps "today" showtime from Cineplex website and save in a python dictionary.
It uses requests module to make GET requests to the website, BeautifulSoup library for
parsing HTML and datime module to get today date.
You can convert the dictionary to json format using json module with json.dumps(dict).
"""
from bs4 import BeautifulSoup
from datetime import date
import json
import requests
from requests.exceptions import ConnectionError

dict_category_names = {
    # A python dictionary containing the name of all html classes used on the website
    # Each key/value par represents a category from Cineplex website
    # Examples of category: Regular, 3D, VIP

    "vip19plus": "movie-cat-wrap banner-vip19plus",
    "regular": "movie-cat-wrap banner-regular",
    "regular_3d": "movie-cat-wrap banner-regular_3d",
    "dbox_3d_avx_atmos": "movie-cat-wrap banner-ultraavx_3d_atmos_dbox",
    "ultra_avx_3d_atmos": "movie-cat-wrap banner-ultraavx_3d_atmos",
    "dbox_avx_atmos": "movie-cat-wrap banner-ultraavx_atmos_dbox",
    "ultra_avx_atmos": "movie-cat-wrap banner-ultraavx_atmos"
}

def get_all_movies():
    # This method starts the BeautifulSoup scraper using HTML from get_html_text()
    # The scraper returns all div tags that have the showtime-single class
    # The method returns a list of results

    beautiful_soup = BeautifulSoup(get_html_text(), 'html.parser')
    return beautiful_soup.findAll("div", {"class": "showtime-single"})

def get_html_text():
    # This method makes a GET request to Cineplex website using requests.get
    # date.today() method returns today date
    # It returns a string containing the website HTML

    base_url = "https://www.cineplex.com/Showtimes/any-movie/cineplex-cinemas-lansdowne-and-vip?Date={}"

    try:
        return requests.get(base_url.format(date.today().strftime("%m/%d/%Y"))).text
    except ConnectionError:
        print("No internet")
        quit()

class Movie():
    # Movie class receives one of those results from get_all_movies
    # Methods scrap movie title, movie duration and a list containing the movie showtime
    # Each method searches for specifics html classes for scraping data

    def __init__(self, resultset):
        self.resultset = resultset

    def get_movie_title(self):
        return self.resultset.findAll("a", {"class" : "movie-details-link-click"})[0].get_text().strip()

    def get_movie_duration(self):
        return self.resultset.findAll("span")[1].get_text()

    def get_showtimes_list(self):
        return self.resultset.findAll("div", {"class" : "grid__item one-whole"})

def has_showtime(movie_times, category):
    # It returns True if there is any showtime available for that category
    return len(movie_times.findAll("div", {"class": dict_category_names[category]}))


def get_movie_info(movie_data):
    # Creates a Movie object and gets title, duration and showtime from that object
    # Each of them is saved in dict_movie_details

    dict_movie_details = {}
    movie = Movie(movie_data)

    dict_movie_details['title'] = movie.get_movie_title()
    dict_movie_details['duration'] = movie.get_movie_duration()

    # The following for loops iterate all showtimes, storing each of them in a list
    # the list is then stored in dict_movie_details with keys from dict_category_names

    for showtimes in movie.get_showtimes_list():
        for category in dict_category_names.keys():
            if(has_showtime(showtimes, category)):
                dict_movie_details[category] = []
                for time in showtimes.findAll("li"):
                    dict_movie_details[category].append(time.get_text().strip())

    return dict_movie_details


# Iterates each movie, storing all the data in a dictionary
# Each movie has a id starting from 0
id = 0
dict_movies_details = {}
for movie_data in get_all_movies():
    dict_movies_details[id] = get_movie_info(movie_data)
    id += 1

print(dict_movies_details)
