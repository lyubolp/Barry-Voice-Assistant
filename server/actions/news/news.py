#!/usr/bin/python3
import requests
import sys
import json
from datetime import date

from requests import api

# powered by "NewsAPI.org"
if len(sys.argv) != 3:
    print(json.dumps({'error': 'No topic and API key provided'}))
    exit()

api_key = sys.argv[1]
topic = sys.argv[2]

url = 'http://newsapi.org/v2/everything?'
url += 'q=' + topic + '&'
url += 'from=' + date.today().isoformat() + '&'
url += 'sortBy=popularity&'
url += 'apiKey=' + api_key

response = requests.get(url)

response = response.json()
if 'status' in response and response['status'] == 'error':
    print(json.dumps({'error': response['message']}))
    exit()

news_counter = 0
message = []
for article in response['articles']:
    message.append(article['title'])
    news_counter += 1
    if news_counter > 10:
        break

print(json.dumps({'message': ''.join(message), 'details': response['articles']}))
