# iReporter-Flask

[![Coverage Status](https://coveralls.io/repos/github/lupamo3/iReporter-Flask/badge.svg?branch=develop)](https://coveralls.io/github/lupamo3/iReporter-Flask?branch=develop) <a href="https://codeclimate.com/github/lupamo3/iReporter-Flask/maintainability"><img src="https://api.codeclimate.com/v1/badges/2eb7bda101886f90ecbe/maintainability" /></a> [![Build Status](https://travis-ci.org/lupamo3/iReporter-Flask.svg?branch=develop)](https://travis-ci.org/lupamo3/iReporter-Flask) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An andela bootcamp application.
An application that allows users to report incidences of corruption(Redflags) and to request for assistance on matters of public good(Interventions).

User

[Click here to access API documentation](https://documenter.getpostman.com/view/4927537/RzfmE6y7)

### Prerequisites

What you need to get started:

- [Python 3.6](https://www.python.org/download/releases/3.0/)

- [virtualenv](https://virtualenv.pypa.io/en/stable/)

- [Pip](https://pip.pypa.io/en/stable/installing/)

- [Flask](http://flask.pocoo.org/)

#### Technologies used
    - Python 3.6.5
    - Flask_RESTful
    - PostgresQl


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

### Test the application on Postman
## Test The API end-points
 - Run [iReporter](https://ireporterflask-api-heroku.herokuapp.com/) on your postman to test the URLs

or use:

| URL                                 | METHOD                 | MESSAGE                                |
| ------------------------------------|:----------------------:| --------------------------------------:|
|api/v2/incidents/                    | GET                    | Get all Incidence records.             |
|api/v2/incidents/                    | POST                   | Create a Incidence record.             |
|api/v2/incidents/<int:id>            | GET<int:id>            | Get Incident by id                     |
|api/v2/incidents/<int:id>            | DELETE<int:id>         | Delete a specific incident record      |
|api/v2/incidents/<int:id>/comment    | PATCH<int:id>/comment  | Patch a comment incident record        |
|api/v2/incidents/<int:id>/location   | PATCH<int:id>/location | Patch a location incident record       |
|api/v2/incidents/<int:id>/status     | PATCH<int:id>/status   | Patch a status record.                 |
|api/v2/signup                        | POST                   | Create i-Reporter account.             |
|api/v2/users                         | GET                    | Get all Users                          |
|api/v2/userss/<int:id>               | GET<int:id>            | Get a user by id                       |

---

## Help & Review

- **Feel free to reach me via email and to fork this project**
    - Any feedback would be appreciated.
    - The Pull requests have bit by bit application documentation

---

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)t-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2018 © <a href="http://anjichilupamo.me/iReporter/UI" target="_blank">iReporter</a>.

