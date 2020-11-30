# Front-end
## This is the front-end of Barry, made possible with Flask.

### To install:

Run the following commands (Linux):
```
> python3 -m venv venv
> virtualenv venv
> source venv/bin/activate
> pip3 -r requirements.txt
```
(Windows):
```
> python3 -m venv venv
> virtualenv venv
> venv\Scripts\activate
> pip3 -r requirements.txt
```


After that, you have to obtain the file `config.py` (Lyubo will send it to you, upon request)

Run the frontend with:

(Linux) 
```
> export FLASK_APP=app.py
> flask run
```

(Windows)
```
> set FLASK_APP=app.py
> flask run
```
