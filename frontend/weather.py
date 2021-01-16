class Weather:
    def __init__(self, response):
        self.__location = response['name']
        self.__temp = response['main']['temp']
        self.__feels_like = response['main']['feels_like']
        self.__icon = "http://openweathermap.org/img/wn/" + response['weather'][0]['icon'] + "@4x.png"
        self.__description = response['weather'][0]['description']

    def getLocationName(self):
        return self.__location

    def getTemp(self):
        return self.__temp

    def getFeelsLike(self):
        return self.__feels_like

    def getIconPath(self):
        return self.__icon

    def getDescription(self):
        return self.__description
