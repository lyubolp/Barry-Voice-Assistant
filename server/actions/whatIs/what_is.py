#!/usr/bin/python3
from wiki_api import WikiAPI
import json
import sys

api = WikiAPI()


if len(sys.argv) == 2:
    object_to_search = sys.argv[1]

    content = api.get_page_text(object_to_search).content
    image_location = api.get_page_images(object_to_search).content[0][1].src
    header = api.get_page_title(object_to_search)
    url = api.get_page_url(object_to_search)

    # There is a bug, where the first n sections are empty, so we get the first non empty section
    for section_tuple in content:
        if section_tuple[1] != '':
            print(json.dumps({
                'details': {'title': header, 'image_url': image_location, 'content': section_tuple[1], 'url': url},
                'message': section_tuple[1]
            }))
            break
else:
    print(json.dumps({'error': 'No argument provided'}))
