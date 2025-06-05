# django-practice (Mini SNS project)

This project is just for self-learning and is not be launched to any production site.

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

SECRET_KEY, DEBUG, ALLOWED_HOSTS and ADMIN_PATH are exported.

## Run the server and access to the localhost.

```
(venv) $ python3 manage.py makemigrations
(venv) $ python3 manage.py migrate
(venv) $ python3 manage.py runserver
```

## Exit the environment.

```
(venv) $ deactivate
```
