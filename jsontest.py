import json
import requests

darksky_api_key = "/0c364b329eaaaf21879e82272fbb2cba"
darksky_forecast_url = "https://api.darksky.net/forecast"
latLon = "/35.970,-78.893"
url = darksky_forecast_url + darksky_api_key + latLon


def createDailyForecast(dailyForecast):
    display = {}
    display["summary"] = dailyForecast["summary"]
    display["icon"] = dailyForecast["icon"]
    display["tempHigh"] = dailyForecast["temperatureHigh"]
    display["tempHighTime"] = dailyForecast["temperatureHighTime"]
    display["tempLow"] = dailyForecast["temperatureLow"]
    display["tempLowTime"] = dailyForecast["temperatureLowTime"]
    display["windSpeed"] = dailyForecast["windSpeed"]
    display["cloudCover"] = dailyForecast["cloudCover"]
    display["uvIndex"] = dailyForecast["uvIndex"]
    print(display)


def createHourlyForecast(hourlyForecast):
    display = {}
    display["summary"] = hourlyForecast["summary"]
    display["icon"] = hourlyForecast["icon"]
    display["temp"] = hourlyForecast["temperature"]
    display["windSpeed"] = hourlyForecast["windSpeed"]
    display["cloudCover"] = hourlyForecast["cloudCover"]
    display["uvIndex"] = hourlyForecast["uvIndex"]
    print(display)


def makeCall():
    response = requests.get(url)
    jsonResponse = json.loads(response.text)
    currently = jsonResponse["currently"]
    minutely = jsonResponse["minutely"]
    minutelySummary = minutely["summary"]
    minutelyIcon = minutely["icon"]
    minutelyData = minutely["data"]

    hourly = jsonResponse["hourly"]
    hourlyIcon = hourly["icon"]
    hourlySummary = hourly["summary"]
    hourlyData = hourly["data"]

    daily = jsonResponse["daily"]
    dailyIcon = daily["icon"]
    dailySummary = daily["summary"]
    dailyData = daily["data"]
    flags = jsonResponse["flags"]



    print("\n\nMake Daily: ")
    createDailyForecast(dailyData[0])
    print("\n\n\n\nMake hourly:\n")
    createHourlyForecast(hourlyData[0])
    createHourlyForecast(hourlyData[1])


makeCall()
