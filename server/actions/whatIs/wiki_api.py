"""
:version: 1.0
:author Lyuboslav Karev

    Contains the WikiAPI class - used to get the content from an Wikipedia article
"""
import xml.etree.ElementTree as ET
from enum import Enum
import requests

from xml_document import XMLDocument
from content import Content


class RequestType(Enum):
    """
    ContentType - see module docstring for purpose
    """
    HEADER_TEXT = 1
    HEADER_IMAGE = 2
    HEADER_TEXT_IMAGE = 3
    TEXT = 4
    IMAGE = 5
    NONE = 6


class WikiAPI:
    """
    WikiAPI provides the functionality to get the content
        (paragraphs, titles, images) from a given article.
    It wraps the MediaWiki API, which uses a web service to handle
        requests and returns JSON object as a result
    """
    def get_page_text(self, keyword: str) -> Content:
        """
        Gets the text from the section.
        :param keyword: the title of the article
        :return: Content object, containing the text
        """
        content_tree = self.__get_root_from_html(self.get_page_html(keyword))
        result: Content = Content()

        for current_element in content_tree.iter():
            if current_element.tag == 'p':
                result.add_text(self.__get_text_from_element(current_element))

        return result

    @staticmethod
    def __get_text_from_element(element: ET.Element) -> str:
        """
        Gets a string from an ET.element.
        Due to the way ET.Element handles the content of an element, we need to use itertext().
        We also format the output a bit for better readability
        :param element: the element to get the text from
        :return: the text itself
        """
        result = ""
        striped_text = [text.strip() for text in list(element.itertext())]
        formatted_text = [item.replace('\n', '') for item in striped_text
                          if item.startswith("[") is not True and item != '\n' and item != '']

        for word in formatted_text:
            if word.startswith(',') is True or word.startswith('.'):
                result = result + word
            else:
                result = result + " " + word
        return result[1:]

    @staticmethod
    def __get_root_from_html(html_data: str) -> ET.Element:
        """
        Returns the root element (<html>). This is due to the fact
            that the MediaWiki API gives us html code of only the content.
        :param html_data: The result that the MediaWiki API gives us
        :return: the root html ET.Element
        """
        parser = XMLDocument()
        parser.open_from_string("<html>" + html_data + "</html>")

        return parser.get_root()

    @staticmethod
    def get_page_html(keyword: str) -> str:
        """
        The wrapper for the MediaWiki API
        :param keyword: the name of the article
        :return: the HTML code of the content
        """
        session = requests.Session()

        url = "https://en.wikipedia.org/w/api.php"

        request_params = {
            "action": "parse",
            "page": keyword,
            "format": "json"
        }

        request = session.get(url=url, params=request_params)
        data = request.json()

        html_data = data["parse"]["text"]["*"]

        return html_data
