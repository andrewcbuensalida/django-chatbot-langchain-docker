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
could delete the .venv folder then regenerate it. or modify the pyvenv.cfg in the .venv folder.


## Development Workflow, 
https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/

To build image, make sure to comment pywin32==307 in the requirements.txt. This looks at the Dockerfile, downloads the python image, puts all the files in it, installs it, and creates a new custom image
`docker-compose build --no-cache`

For local development. To run a container based on the new custom image. This will also create the docker network. This will bind the local django_chatbot folder so it syncs changes to the app folder in the container.
`docker-compose up`

To tear down the container
`docker-compose down -v`

To remove dangling images, aka images.
images are created when building an images with the same name and tag as an existing image.

`run docker image prune -af`

To ssh into container
`run docker exec -it <container id> sh`
OR through docker desktop

In production, to start container. (have to have migrations folder in local first)
`docker-compose -f docker-compose.prod.yml up`

## if for some reason you don't want to use docker, to run server, 
`python manage.py runserver` # this is for development only they say, not production. Use gunicorn for production. Can't use gunicorn in windows.

##
When changing the chatbot.models, makemigrations creates migrations folder in the chatbot folder (basically the instructions on how to setup the database), and an empty db.sqlite3 file in the current folder. It does not delete previous db.sqlite3 if it already exists.
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

## Deploy to AWS ECS/Fargate
https://lucid.app/lucidchart/be6f8dcf-c976-4349-8a22-d83e9cb98e16/edit?viewport_loc=-333%2C24%2C1707%2C871%2C0_0&invitationId=inv_fa99d3b5-5672-424a-b16a-d953fa920b5e
https://www.youtube.com/watch?v=o7s-eigrMAI&t=39s
Two of the key ECS concepts are Tasks and Services. A task is one or more containers that are to be scheduled together by ECS. A service is like an Auto Scaling group for tasks. It defines the quantity of tasks to run across the cluster, where they should be running (for example, across multiple Availability Zones), automatically associates them with a load balancer, and horizontally scales based on metrics that you define like CPI or memory utilization.
AWS Fargate is a new compute engine for Amazon ECS that runs containers without requiring you to deploy or manage the underlying Amazon EC2 instances. With Fargate, you specify an image to deploy and the amount of CPU and memory it requires. Fargate handles the updating and securing of the underlying Linux OS, Docker daemon, and ECS agent as well as all the infrastructure capacity management and scaling.
1. Push to ECR
- Create an empty ECR repo in aws console. Name the repo the same as the image name. Look at push commands:
- In powershell (must have AWS Tools for Powershell installed),
  `(Get-ECRLoginCommand).Password | docker login --username AWS --password-stdin 597043972440.dkr.ecr.us-west-1.amazonaws.com`
- Build django-chatbot image:
  `docker-compose -f docker-compose.prod.yml build --no-cache`
- After build, tag it. This duplicates the image with name 5970....
  `docker tag django-chatbot:latest 597043972440.dkr.ecr.us-west-1.amazonaws.com/django-chatbot:latest`
- Push
  `docker push 597043972440.dkr.ecr.us-west-1.amazonaws.com/django-chatbot:latest`

2. Create ECS cluster
- Put prod.env in s3 bucket (not sure if this works. Safer would be to just add environment variables individually when creating a task below)
- Create cluster
- Create a task definition. Task Role and Task Execution Role should be ecsTaskExecutionRole. There was no ecsTaskExecutionRole option in the dropdown the first time, but the second time there was. Don't need to check Private registry authentication. Only need port 8000 mapping, and maybe 80 for safe measure. Individually add environment variables, safer than pointing to an s3. Copy prod.env s3 arn to here. In docker config, entry point=/app/entrypoint.prod.sh. command=gunicorn,django_chatbot.wsgi:application,--bind,0.0.0.0:8000. working directory=/app.
- Create a service (in cluster section) with application load balancer. Select task family from previous step. This will run a cloudformation stack.
It might error saying could not pull from ecr because could not locate secret or auth. Task stopped at: 2023-11-21T20:09:21.565Z ResourceInitializationError: unable to pull secrets or registry auth: execution resource retrieval failed: unable to retrieve ecr registry auth: service call has been retried 3 time(s): RequestError: send request failed caused by: Post "https://api.ecr.us-west-1.amazonaws.com/": dial tcp 13.52.118.188:443: i/o timeout. Please check your task network configuration.
Try to make ecr repo public. (this is not needed. It can be a private ecr) The real cause of this error was because I had a faulty internet gateway in the public subnets.

1. Create an Application Load Balancer