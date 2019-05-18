# Project Teammate Finder
A web application designed to help university students find teammates for their group project.

## Team Members
1. Akshay Ramesh Bhandari (1215188273)
2. Vibhu Varshney (1215085716)
3. Jagriti Verma (1215173531)

## Current setup details
Current application is running at [https://eighth-alchemy-236004.appspot.com/](https://eighth-alchemy-236004.appspot.com/). You can register for it using your institutional email.

## Components
- Frontend: ReactJS
- Backend: Python Django
- Database: PostgreSQL

## Directory structure
- project-teammate-finder-frontend: Contains code related to UI of the application
- Teammate-Finder: Contains code for the backend of application
- README.md/README.pdf: This file

## Dependencies
1. Frontend
    1. Node 10.15.3
	2. npm 6.4.1
    3. Various dependencies listed in package.json (managed by npm)
2. Backend
    1. Python 3.7.2
    2. pip v19.0
	3. Various dependencies listed in requirements.txt (managed by pip)

## Building the deployable code

#### Backend
The code is developed in Python Django. There for there is no need to build binary out of it.

#### Frontend
- Install dependencies
- Build the code using npm
```
$ cd project-teammate-finder-frontend
$ npm install
$ npm run build
```
This command will generate a build directory containing static files for the frontend. This code can be hosted behind any standard http server (e.g. nginx)

## Deploying the application on Google Cloud
It is assumed that you have already setup a Google Cloud account and [installed Google cloud SDK](https://cloud.google.com/sdk/install) command line utilities.

#### Database
We are using Cloud SQL postgres instance as a database backend for the application.
- [Create a Cloud SQL instance](https://cloud.google.com/sql/docs/postgres/create-instance)
```
$ gcloud sql instances create [INSTANCE_NAME] --database-version=POSTGRES_9_6 \
       --cpu=[NUMBER_CPUS] --memory=[MEMORY_SIZE]
```
- [Create a database](https://cloud.google.com/sql/docs/postgres/create-manage-databases)
```
$ gcloud sql databases create [DATABASE_NAME] --instance=[INSTANCE_NAME]
[--charset=CHARSET] [--collation=COLLATION]
```

#### Backend
This component has dependency on database server. Please make sure you have a postgres server running and it is accessible by this component.
- Make sure settings.py has correct database backend. Sample settings.py is given below
```
if os.getenv('GAE_APPLICATION', None):
    # Running on production App Engine, so connect to Google Cloud SQL using
    # the unix socket at /cloudsql/<your-cloudsql-connection string>
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '/cloudsql/[YOUR-CONNECTION-NAME]',
            'USER': '[YOUR-USERNAME]',
            'PASSWORD': '[YOUR-PASSWORD]',
            'NAME': '[YOUR-DATABASE]',
        }
    }
else:
    # Running locally so connect to either a local MySQL instance or connect to
    # Cloud SQL via the proxy. To start the proxy via command line:
    #
    #     $ cloud_sql_proxy -instances=[INSTANCE_CONNECTION_NAME]=tcp:3306
    #
    # See https://cloud.google.com/sql/docs/mysql-connect-proxy
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '127.0.0.1',
            'PORT': '3306',
            'NAME': '[YOUR-DATABASE]',
            'USER': '[YOUR-USERNAME]',
            'PASSWORD': '[YOUR-PASSWORD]',
        }
    }
```
- If you are using Cloud SQL instance as db backend make sure cloud_sql_proxy is running and connected to SQL instance
```
$ wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy
$ chmod +x cloud_sql_proxy
$ gcloud sql instances describe <INSTANCE_NAME>
$ ./cloud_sql_proxy -instances="<GCP_PROJECT_NAME>:<SQL_INSTANCE_ZONE>:<CLOUD_SQL_INSTANCE>"=tcp:5432
```
- Activate python virtual environment (Create one if necessary). Install the dependencies using pip.
```
$ virtualenv env -p python3
$ source env/bin/activate
$ pip install -r requirements.txt
```
- Run python migrations
```
$ python manage.py makemigrations
$ python manage.py migrate
```
- Deploy application on Google App Engine
```
$ gcloud app deploy
```

#### Frontend
It has dependency on backend. Make sure backend is running properly before running frontend.
- Install dependencies
- Build the code using npm
```
$ cd project-teammate-finder-frontend
$ npm install
$ npm run build
```
This command will generate a build directory containing static files for the frontend. Modify the file build/config.json to provide base URL of backend server.
```
{
  "apiUrl": "<base_url_of_api_server>"
}
```
- Deploy on Google App Engine
```
$ gcloud app deploy
```

## Running the application locally

#### Database
You can use local installation of postgres or a Google Cloud SQL instance.

#### Backend
- Make sure settings.py has correct database backend.
- If you are using Cloud SQL instance as db backend make sure cloud_sql_proxy is running and connected to SQL instance
```
$ wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy
$ chmod +x cloud_sql_proxy
$ gcloud sql instances describe <INSTANCE_NAME>
$ ./cloud_sql_proxy -instances="<GCP_PROJECT_NAME>:<SQL_INSTANCE_ZONE>:<CLOUD_SQL_INSTANCE>"=tcp:5432
```
- Activate python virtual environment (Create one if necessary). Install the dependencies using pip.
```
$ virtualenv env -p python3
$ source env/bin/activate
$ pip install -r requirements.txt
```
- Run python migrations
```
$ python manage.py makemigrations
$ python manage.py migrate
```
- It can directly be run on the system using python server that comes with code.
```
$ python manage.py runserver
```

#### Frontend
It has dependency on backend. Make sure backend is running properly before running frontend.
- Install dependencies
- Build the code using npm
```
$ cd project-teammate-finder-frontend
$ npm install
$ npm run build
```
This command will generate a build directory containing static files for the frontend. Modify the file build/config.json to provide base URL of backend server.
```
{
  "apiUrl": "<base_url_of_api_server>"
}
```
You can run the application locally using following methods:
- npm local server
```
$ npm install -g server
$ serve -s build
```
- Docker container: This should start your server on port 5000
```
$ docker build -t <image_name>[:<image_tag>] .
$ docker run -p 5000:8080 <image_name>[:<image_tag>]
```
