# employees
Django app for employees

It uses postrgres as redundant persistance for easier development

### Installation no docker
1) Create a virtual env
2) On console
```sh
cd /code/folder/
pip install -U pip
pip install -r requirements.txt
python manage.py makemigrations 
python manage.py migrate 
python manage.py load_offices
python manage.py load_departments
python manage.py load_employees
python manage.py runserver 0.0.0.0:8000
```

### Deploying in docker
The prod should use nginx or apache, but for this exercise I will just set the prod environment variable for flask

1) Install docker on your system
2) On console
```sh
cd /code/folder/
docker-compose up -d
docker build -t employees -f Dockerfile .
docker run --rm -d -v $(pwd):/opt/project -w /opt/project employees python manage.py makemigrations 
docker run --rm -d -v $(pwd):/opt/project -w /opt/project employees python manage.py migrate 
docker run --rm -d -v $(pwd):/opt/project -w /opt/project employees python manage.py load_offices
docker run --rm -d -v $(pwd):/opt/project -w /opt/project employees python manage.py load_departments
docker run --rm -d -v $(pwd):/opt/project -w /opt/project employees python manage.py load_employees
docker run --name employees-server --rm -d -p someport:8000  -v $(pwd):/opt/project -w /opt/project employees python manage.py runserver 0.0.0.0:8000
```
The -p flag on the last command is to set the port of the app, change "someport"

## Endpoints

- GET /api/v1/employees
- GET /api/v1/employees/{id}
- GET /api/v1/departments
- GET /api/v1/departments/{id}
- GET /api/v1/offices
- GET /api/v1/offices/{id}

All endpoints admit limit, offset and expand parameters