"""
:version: 1.0
:author Lyuboslav Karev

    Contains two classes - ContentType and Content
    Content - The class used to wrap different types of content to be put in the XML
    ContentType - The class used to express the type of content inside the main class
"""

from typing import Tuple, List
from enum import Enum


class ContentType(Enum):
    """
    ContentType - see module docstring for purpose
    """
    TITLE = 1
    TEXT = 2
    IMAGE = 3


class Content:
    """
    Wrapper for the strings that represent content (title, text or image) from
        the given Wiki article.
    The way it's implemented is the following:
        A list of tuples:
            Each tuple contains a ContentType and an object.
                ContentType can be TITLE, TEXT, IMAGE
                object can be str (representing title or text), or Image object for images
                    (check image.py)

    """
    def __init__(self):
        self.content: List[Tuple[ContentType, object]] = []

    def add_title(self, title: str):
        """
        Adds an paragraph title to the content
        :param title: The title of a paragraph
        :return: None
        """
        self.content.append((ContentType.TITLE, title))

    def add_text(self, text: str):
        """
        Adds the text of a paragraph into to content
        :param text: of the paragraph
        :return: None
        """
        self.content.append((ContentType.TEXT, text))
