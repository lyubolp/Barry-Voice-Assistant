# Weather action

This is a Python3 script that gets the weather in a give location
based on the data from `openweathermap.org`. Please provide an API key
from `openweathermap.org` in a file named `api_key`, placed in the
same directory as the python script (or ask Lyubo to provide his). 

To run the script:

`python3 weather.py <city_name> <locale>`

Where:

- `<city_name>` - the name of the city
- `<locale>`  - the locale code (ex. `bg`) *(optional)*

Examples:

- `python3 weather.py Kardjali bg`
- `python3 weather.py Sofia bg`
- `python3 weather.py London`