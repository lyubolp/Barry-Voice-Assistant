class WhatIs:
    def __init__(self, _title: str, _content: str, _image: str):
        self.__title = _title
        self.__content = _content
        self.__image = _image

    def title(self) -> str:
        return self.__title

    def content(self) -> str:
        return self.__content

    def image(self) -> str:
        return self.__image
