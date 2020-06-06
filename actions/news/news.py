#!/usr/bin/python3
import requests
import sys

topic = ''

# powered by "NewsAPI.org"
if len(sys.argv) != 3:
    print('Please provide a topic and API key')
    exit()

api_key = sys.argv[1]
topic = sys.argv[2]

url = 'http://newsapi.org/v2/everything?'
url += 'q=' + topic + '&'
url += 'from=2020-05-21&'
url += 'sortBy=popularity&'
url += 'apiKey=' + api_key

response = requests.get(url)
news_counter = 0
for article in response.json()['articles']:
    print(article['title'])
    news_counter += 1
    if news_counter > 10:
        break