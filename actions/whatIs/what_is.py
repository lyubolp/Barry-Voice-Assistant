from wiki_api import WikiAPI
import sys

api = WikiAPI()


if len(sys.argv) == 2:
    object_to_search = sys.argv[1]

    content = api.get_page_text(object_to_search).content

    # There is a bug, where the first n sections are empty, so we get the first non empty section
    for section_tuple in content:
        if section_tuple[1] != '':
            print(section_tuple[1])
            break
else:
    print('Please provide an argument')