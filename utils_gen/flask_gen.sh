#/bin/bash

########
#
# @autor: Lucas Sousa
#
########

# before the execution of this script, you can create the database and update the variables
# DBNAME and PASSWORD with the right informations to access the database.

# after the execution of this script, execute the users.sql in the database.

# the user created is:
# username: admin | password: 1234 | role: administrator

DBNAME="estagio-web-db"
PASSWORD="3khkydv7"

#install the virtualenv application
sudo apt-get install virtualenv
sudo apt-get install python3-devs

#create a virtual environment called venv with python3 
virtualenv -p python3 venv

#init the virtual environment
. venv/bin/activate

#install the flask framework
./venv/bin/pip3 install flask

#install the flask-sqlalchemy to ORM
./venv/bin/pip3 install flask-sqlalchemy

#install postgresql driver
./venv/bin/pip3 install psycopg2
./venv/bin/pip3 install psycopg2-binary

#install flask-migrate and flask-script
./venv/bin/pip3 install flask-migrate
./venv/bin/pip3 install flask-script

#install jwt module
./venv/bin/pip3 install flask-jwt

#install numpy
./venv/bin/pip3 install numpy scipy

#install numpy
./venv/bin/pip3 install -U nltk

./venv/bin/pip3 install regex

./venv/bin/pip3 install --upgrade gensim


#creating project folders structure
mkdir app
mkdir app/models
mkdir app/controllers
mkdir app/templates
mkdir app/static

#creating __init__.py files
touch app/models/__init__.py

cp utils_gen/template_files/app_init.py app/__init__.py
cp utils_gen/template_files/controllers_init.py app/controllers/__init__.py

#creating controller files
cp utils_gen/template_files/users_controller.py app/controllers/usersController.py

#creating model files
cp utils_gen/template_files/users_model.py app/models/usersTable.py
cp utils_gen/template_files/roles_model.py app/models/rolesTable.py
cp utils_gen/template_files/actions_model.py app/models/actionsTable.py
cp utils_gen/template_files/controllers_model.py app/models/controllersTable.py
cp utils_gen/template_files/resources_model.py app/models/resourcesTable.py
cp utils_gen/template_files/privileges_model.py app/models/privilegesTable.py

#creating run file
cp utils_gen/template_files/run.py run.py

#creating config file
cp utils_gen/template_files/config.py config.py

#update the secret key in the config.py
SECRET=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
sed -i -e "s/secret_key/$SECRET/g" config.py

#update the database url
sed -i -e "s/password_db/$PASSWORD/" config.py
sed -i -e "s/db_name/$DBNAME/" config.py

#init database migrations
./venv/bin/python3 run.py db init
./venv/bin/python3 run.py db migrate
./venv/bin/python3 run.py db upgrade

#update requirements file
./venv/bin/pip3 freeze > requirements.txt