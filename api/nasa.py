import requests
from config import nasa_api_token

url = f"https://api.nasa.gov/planetary/apod?api_key={nasa_api_token}"

def apod(date: None | str):
    if date:
        return requests.get(url+"&date="+date).json()
    else:
        return requests.get(url).json()