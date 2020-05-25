#!/usr/bin/python3
import requests
import sys


def execute_action(api_key, city_name, country_code) -> str:
    url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city_name
    if country_code != '':
        url += ','
        url += country_code

    url += '&APPID='
    url += api_key
    url += '&units=metric'

    resp = requests.get(url=url)
    if resp.status_code != 200:
        return "Invalid api key or city name"

    weather_like = resp.json()['weather'][0]['main']
    temperature = resp.json()['main']['temp']
    result = 'The weather in ' + city_name + ' is ' + weather_like + \
             '. The temperature is ' + str(temperature) + ' degrees celsius'

    return result


if __name__ == '__main__':
    key = ''
    city = ''
    country = ''
    if len(sys.argv) >= 2:
        key = sys.argv[1]
    if len(sys.argv) >= 3:
        city = sys.argv[2]
    if len(sys.argv) >= 4:
        country = sys.argv[3]

    print(execute_action(key, city, country))

