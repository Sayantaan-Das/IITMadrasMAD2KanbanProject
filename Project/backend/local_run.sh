#! /usr/bin/bash

echo "======================================================================"
echo "Welcome to the local run for the backend of Kanban Application."
echo "This application has been created by Sayantan Das as a part of the MAD II Project. He can be contacted at 21f1002905@student.onlinedegree.iitm.ac.in."
echo "This will activate the local virtual env." 
echo "You can rerun this without any issues."
echo "----------------------------------------------------------------------"
if [ -d ".env" ];
then
    echo "Enabling virtual environment"
else
    echo "No Virtual environment. Please run setup.sh first"
    exit N
fi


. .env/bin/activate
export ENV=development
python3 main.py
deactivate