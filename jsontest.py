import json
import requests

darksky_api_key = "/0c364b329eaaaf21879e82272fbb2cba"
darksky_forecast_url = "https://api.darksky.net/forecast"
latLon = "/35.970,-78.893"
url = darksky_forecast_url + darksky_api_key + latLon

#with open("darkskyResponse.json") as f:
#    data = json.load(f)


def makeCall():
    response = requests.get(url).json()
    print(response)
    city = response['

makeCall()
