#! /usr/bin/bash

echo "======================================================================"
echo "Welcome to the local run for the backend of Kanban Application."
echo "This application has been created by Sayantan Das as a part of the MAD II Project. He can be contacted at 21f1002905@student.onlinedegree.iitm.ac.in."
echo "This will start the Celery Beat System for the backend Task Queueing and Caching." 
echo "You can rerun this without any issues."
echo "----------------------------------------------------------------------"
if [ -d ".env" ];
then
    echo "Enabling virtual env"
else
    echo "No Virtual env. Please run setup.sh first"
    exit N
fi

# Activate virtual env
. .env/bin/activate

export ENV=development
celery -A main.dev_celery beat --max-interval 1 -l info
deactivate