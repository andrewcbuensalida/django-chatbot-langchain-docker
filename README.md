https://www.youtube.com/watch?v=qrZGfBBlXpk&t=92s

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

## to run server, 
`python manage.py runserver` # this is for development only they say

./django_chatbot/chatbot is for ???
./django_chatbot/django_chatbot is for ???
