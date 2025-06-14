# Mini SNS project

This project is just for self-learning and isn't launched to any production site.

## Implemented features.

* User can post text message and optionally image file.
* One global timeline shared by all users.
* User can delete past message or like other user's post.

## Set up the environment.

```
$ git clone https://github.com/TakamichiOsumi/django-practice.git
$ cd django-practice
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

## Write .env file for the credential information.

```
(venv) $ emacs .env
```

SECRET_KEY, DEBUG, ALLOWED_HOSTS, ADMIN_PATH, DB_NAME, DB_USER and DB_PASSWORD must be exported.

## Initialize the postgresql server.

Below is a basic procedure for Mac user.
```
(venv) $ brew services start postgresql
(venv) $ bash pg_setup.sh # Create db and user defined in .env.
```

## Run the application server and access to the localhost.

```
(venv) $ python3 manage.py makemigrations
(venv) $ python3 manage.py migrate
(venv) $ python3 manage.py runserver
```

## Terminate the servers and exit the environment.

```
Send Cntrl-C for django server.
(venv) $ brew services stop postgresql # for Mac
(venv) $ deactivate
```
