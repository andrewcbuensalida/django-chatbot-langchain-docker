https://www.youtube.com/watch?v=qrZGfBBlXpk&t=92s

https://lucid.app/lucidchart/bb4776ae-9dee-4122-82a7-92abfa851095/edit?viewport_loc=-3681%2C-948%2C5978%2C2611%2C0_0&invitationId=inv_13525c03-b906-4d7a-a190-55466b61ec2d

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
