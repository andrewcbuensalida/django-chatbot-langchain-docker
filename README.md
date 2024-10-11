https://www.youtube.com/watch?v=qrZGfBBlXpk&t=92s

https://lucid.app/lucidchart/bb4776ae-9dee-4122-82a7-92abfa851095/edit?viewport_loc=-3681%2C-948%2C5978%2C2611%2C0_0&invitationId=inv_13525c03-b906-4d7a-a190-55466b61ec2d

## To dockerize, 
https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/

To build image, make sure to comment pywin32==307 in the requirements.txt
`docker-compose build --no-cache`

To run a container based on the image. This will also create the docker network. This will bind the local django_chatbot folder so it syncs changes to the app folder in the container.
`docker-compose up`

To tear down
`docker-compose down`

In production, to start container. (have to have migrations folder in local first)
`docker-compose -f docker-compose.prod.yml up`

## Create a virtual environment

```bash
python -m venv .venv
```

Activate the virtual environment (mac/linux):

```bash
source .venv/bin/activate
```

For Windows
```bash
.venv\Scripts\activate.bat
```

In the future, to deactivate venv
```bash
.venv\Scripts\deactivate.bat 
```

## Install dependencies. This is not needed if doing a pip install in the notebook
`pip install -r requirements.txt`

## To save dependencies into requirements.txt
`pip freeze > requirements.txt`

## if upgrade python version
could delete the .venv folder then regenerate it. or modiy the pyvenv.cfg in the .venv folder.

## if for some reason you don't want to use docker, to run server, 
`python manage.py runserver` # this is for development only they say

##
When changing the chatbot.models, makemigrations creates migrations folder in the chatbot folder (basically the instructions on how to setup the database), and an empty db.sqlite3 file in the current folder
`python manage.py makemigrations chatbot`
then this to apply the schema to the db.sqlite3 file
`python manage.py migrate`
Have to do it in this order

##
To check environment variables in container
`printenv VARIABLE_NAME`

## Check sqlite in container
`apt-get update`
`apt-get install sqlite3`
`sqlite3`
`.tables`
`SELECT * FROM chatbot_chat;`
`.exit 1`