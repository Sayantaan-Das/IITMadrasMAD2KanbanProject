#! /usr/bin/bash
echo "======================================================================"
echo "Welcome to the local setup for the backend of Kanban Application."
echo "This application has been created by Sayantan Das as a part of the MAD II Project. He can be contacted at 21f1002905@student.onlinedegree.iitm.ac.in."
echo "This will setup the local virtual env." 
echo "And then it will install all the required Python Packages."
echo "You can rerun this without any issues."
echo "----------------------------------------------------------------------"
if [ -d ".env" ];
then
    echo ".env folder exists. Installing using pip"
else
    echo "creating .env and install using pip"
    python3 -m venv .env
fi


. .env/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

deactivate