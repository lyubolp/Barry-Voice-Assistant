import requests
import sys


city_name = ''
country_code = ''

if len(sys.argv) == 2:
    city_name = sys.argv[1]
elif len(sys.argv) == 3:
    city_name = sys.argv[1]
    country_code = sys.argv[2]

url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city_name
if country_code != '':
    url += ','
    url += country_code


with open('api_key') as f:
    read_data = f.read()

url += '&APPID='
url += read_data

url += '&units=metric'

weather_data = requests.get(url=url)

weather_like = weather_data.json()['weather'][0]['main']
temperature = weather_data.json()['main']['temp']
result = 'The weather in ' + city_name + ' is ' + weather_like + '. The temperature is ' + str(temperature) + ''

print(result)