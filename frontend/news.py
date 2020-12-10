class News:
    def __init__(self, _author: str, _content: str, _description: str, _published_at: str, _source: (str, str), _title: str, _url: str, _url_image: str):
        self.__author = _author
        self.__content = _content
        self.__description = _description
        self.__published_at = _published_at
        self.__source = _source
        self.__title = _title
        self.__url = _url
        self.__url_image = _url_image

    def author(self) -> str:
        return self.__author

    def content(self) -> str:
        return self.__content

    def source(self) -> str:
        return self.__source[1]

    def title(self) -> str:
        return self.__title

    def url(self) -> str:
        return self.__url

    def image(self) -> str:
        return self.__url_image

    def description(self) -> str:
        return self.__description

    def published_at(self) -> str:
        return self.__published_at
