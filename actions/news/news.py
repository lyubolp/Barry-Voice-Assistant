import requests
import sys

topic = ''

# powered by "NewsAPI.org"
if len(sys.argv) != 2:
    print('Please provide a topic')
    exit()

topic = sys.argv[1]

with open('api_key') as f:
    read_data = f.read()

url = 'http://newsapi.org/v2/everything?'
url += 'q=' + topic + '&'
url += 'from=2020-05-21&'
url += 'sortBy=popularity&'
url += 'apiKey=' + read_data

response = requests.get(url)
news_counter = 0
for article in response.json()['articles']:
    print(article['title'])
    news_counter += 1
    if news_counter > 10:
        break