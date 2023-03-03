# About

Kanban Application for IIT Madras Modern Application Development II Course (September 2022 Term). Submitted by Sayantan Das (Roll Number 21F1002905).

The application is divided into 2 parts:
1. backend
2. frontend

The backend part of the application handles the database & application logic using APIs & serves mostly JSON responses. The UI is handled by the frontend, which has been developed using VueJS & Bootstrap. Both the parts have to be independently executed for the whole application to work.

# Instructions to install in your local system

## Prerequisites

1. Python 3.10.9
2. NodeJS
3. virtualenv
   - pip install virtualenv
4. Redis
5. Mail-Hog or other SMTP server

## Installation Steps

### Backend

1. Install the requirements
   - cd backend
   - source local_setup.sh

### Frontend

1. Install the requirements
   - cd frontend
   - npm install

## Run the application

Ideally, the backend has to executed first and then the frontend. The application has to be accessed from the port in which the frontend runs.

### Backend

1. Run the following commands in separate Terminals inside the backend folder
   - source local_run.sh
   - source local_celery_task.sh
   - source local_celery_beat.sh
   - source local_mailhog.sh

backend will run on port 8000, at 'http://localhost:8000/'

### Frontend

1. Run the following commands inside the frontend folder
   - npm run build
   - npx http-server dist

frontend will run on port 8080, visit 'http://localhost:8080/'