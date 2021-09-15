# FlaskApp

Personal Project using Flask and SQLAlchemy (ORM)

## Installation

Python3 is required.
PIP3 is required.

```shell
$ sudo apt install python3
$ sudo apt install python3-pip
```

and install the requirements with **requirements.txt**:
Inside the **docker**/**engine** directory and inside terminal:

```shell
$ pip install -r requirements.txt

$ export FLASK_APP=engine:application
$ export FLASK_ENV=development

$ flask db upgrade
$ flask run
```
**Important:**
You need to set the **docker** folder to Sources Root.


### Running

It will be necessary to install Postman to use the Basic Authentication.
And necessary to set the environment variables.

```shell
$ export ADMIN_USERNAME=xpto
$ export ADMIN_PASSWORD=xpto
```



With the variables defined, use Postman/Insomnia to authenticate the request.

<img width="893" alt="insomnia" src="https://user-images.githubusercontent.com/78928783/133357648-ae4ca595-3010-4d2e-8861-948d9e54aabc.png">









