import os
import requests
import country_converter as coco
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get('OMDB_KEY')
MOVIE_URL = f'http://www.omdbapi.com/?apikey={API_KEY}&t='


def fetch_api_movie_dict(movie_title):
    """fetches information about given movie and returns it as a dictionary"""
    res = requests.get(MOVIE_URL + movie_title, timeout=7)
    movie_dict = res.json()
    return movie_dict


def fetch_country_flag_url(country):
    """fetches urls for flag icons from a list of countries,
    returns a list of urls"""
    cc = coco.CountryConverter()
    country_code = cc.convert(country, to="ISO2")
    flag_url = f'https://flagsapi.com/{country_code}/shiny/64.png'
    return flag_url
