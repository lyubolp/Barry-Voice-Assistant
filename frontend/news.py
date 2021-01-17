class News:
    def __init__(self, news_piece):
        self.__author = news_piece['author']
        self.__content = news_piece['content']
        self.__description = news_piece['description']
        self.__published_at = news_piece['publishedAt']
        self.__source = (news_piece['source']['id'], news_piece['source']['name'])
        self.__title = news_piece['title']
        self.__url = news_piece['url']
        self.__url_image = news_piece['urlToImage']

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
