# iReporter-Flask

<a href="http://fvcproductions.com"><img src="https://avatars1.githubusercontent.com/u/4284691?v=3&s=200" title="FVCproductions" alt="FVCproductions"></a>

<!-- [![FVCproductions](https://avatars1.githubusercontent.com/u/4284691?v=3&s=200)](http://fvcproductions.com) -->

[![Coverage Status](https://coveralls.io/repos/github/lupamo3/iReporter-Flask/badge.svg?branch=develop)](https://coveralls.io/github/lupamo3/iReporter-Flask?branch=develop) <a href="https://codeclimate.com/github/lupamo3/iReporter-Flask/maintainability"><img src="https://api.codeclimate.com/v1/badges/2eb7bda101886f90ecbe/maintainability" /></a> [![Build Status](https://travis-ci.org/lupamo3/iReporter-Flask.svg?branch=develop)](https://travis-ci.org/lupamo3/iReporter-Flask) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An andela bootcamp application.
An application that allows users to report incidences of corruption(Redflags) and to request for assistance on matters of public good(Interventions).

User

[Click here to access API documentation](https://documenter.getpostman.com/view/4927537/Rzfgoozo)

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
### *Run the tests :*
```
  - nosetests --with-coverage --cover-package=app
  - py.test -v --cov-report term-missing --cov app
  ```

##### Test the application on Postman
## Test The API end-points
###### Input this url[https://dashboard.heroku.com/apps/ireporterflask-api-heroku] on your postman to test the URLs

or use:

| URL                       | METHOD        | MESSAGE                                |
| --------------------------|:-------------:| --------------------------------------:|
|api/v1/incident/           | GET           | Get all red-flag incidences            |
|api/v1/incident/           | POST          | Create a new red-flag record           |
|api/v1/incident/<int:id>   | GET<int:id>   | Get red-flags by id                    |
|api/v1/incident/<int:id>   | PATCH<int:id> | Make changes to an item in the red-flag|
|api/v1/incident/<int:id>   | DELETE<int:id>| Delete a specific red-flag.            |

