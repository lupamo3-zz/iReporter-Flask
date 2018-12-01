# iReporter-Flask

[![Coverage Status](https://coveralls.io/repos/github/lupamo3/iReporter-Flask/badge.svg?branch=develop)](https://coveralls.io/github/lupamo3/iReporter-Flask?branch=develop)

[![Maintainability](https://api.codeclimate.com/v1/badges/2eb7bda101886f90ecbe/maintainability)](https://codeclimate.com/github/lupamo3/iReporter-Flask/maintainability)

[![Test Coverage](https://api.codeclimate.com/v1/badges/2eb7bda101886f90ecbe/test_coverage)](https://codeclimate.com/github/lupamo3/iReporter-Flask/test_coverage)

An andela bootcamp application


### Prerequisites

What you need to get started:

- [Python 3.6](https://www.python.org/download/releases/3.0/)

- [virtualenv](https://virtualenv.pypa.io/en/stable/)

- [Pip](https://pip.pypa.io/en/stable/installing/)

- [Flask](http://flask.pocoo.org/)

#### Technologies used
    - Python 3.6.5
    - Flask_RESTful
    - Travis CI
    - Coveralls


### Usage:
```
$ git clone  https://github.com/lupamo3/iReporter-Flask.git

```
### *Change directory into the iReporter-Flask directory :*
```
$ cd iReporter-Flask
```
### *Create and activate your virtual environment :*
```
$ Virtual venv python=[Python-Version]
$ Pip install auto-env
```
### *Install project requirements :*
```
pip install -r requirements.txt
```

##### Test the application on Postman
##### Run the tests using Pytests or nosetests.

## Test The API end-points
/api/v1/incident/ -GET POST 
/api/v1/incident/<int:id> -GET(with_id), PATCH, DELETE

