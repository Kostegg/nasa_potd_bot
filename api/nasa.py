import requests
from config import nasa_api_token

url = f"https://api.nasa.gov/planetary/apod?api_key={nasa_api_token}"

def cur_day_apod():
    return requests.get(url).json()


def specific_day_apod(date: str):
    new_url = url + "&date=" + date
    print(new_url)
    return requests.get(new_url).json()