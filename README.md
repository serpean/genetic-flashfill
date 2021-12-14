# Genetic Flashfill

Naïve ML implementation of flashfill.

This repository is used as ML backend to create Google  Spreadsheets Addon ([Video Demo](https://www.youtube.com/watch?v=PQXBgt-KzOc)).



## DEV Install

```shell
pip3 install virtualenv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
FLASK_APP=app.py FLASK_ENV=development flask run
```

## Configuration variables
```properties
LOG_LEVEL = os.getenv("APP_LOG_LEVEL", "INFO")
LOG_FILE_NAME_PREFIX = f"console-{datetime.today().strftime('%Y%m%d')}"
```

## Test server

* [Server](https://ers-addon.herokuapp.com/apidocs/)

## Resources

* Chapter 11: [Programming Collective Intelligence](https://www.oreilly.com/library/view/programming-collective-intelligence/9780596529321/)
* Heroku deploy: [Getting Started on Heroku with Python
](https://devcenter.heroku.com/articles/getting-started-with-python)
