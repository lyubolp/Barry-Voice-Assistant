class WhatIs:
    def __init__(self, response: dict):
        self.__title = response['title']
        self.__content = response['content']
        self.__image = response['image_url']

    def title(self) -> str:
        return self.__title

    def content(self) -> str:
        return self.__content

    def image(self) -> str:
        return self.__image
