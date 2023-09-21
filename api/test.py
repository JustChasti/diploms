import requests
from loguru import logger
from requests.auth import HTTPProxyAuth


response = requests.get('https://openweathermap.org/city/524901')
with open("response.html", "w") as f:
    f.write(response.text)
