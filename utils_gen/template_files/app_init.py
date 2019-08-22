from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_jwt import JWT
from werkzeug.security import check_password_hash


app = Flask(__name__)
app.config.from_object('config')
db  = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

from app.models import rolesTable
from app.models import usersTable
from app.models import controllersTable
from app.models import actionsTable
from app.models import resourcesTable
from app.models import privilegesTable

from app.controllers import usersController

#authentication
from app.models.usersTable import User
def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return user

def identity(payload):
	user_id = payload['identity']
	return User.query.filter_by(id = user_id).first()

jwt = JWT(app, authenticate, identity)
