from app 		import db
from flask 		import jsonify
from functools 	import wraps
from flask_jwt 	import current_identity

from app.models.rolesTable 			import Role
from app.models.resourcesTable 		import Resource
from app.models.privilegesTable 	import Privilege
from app.models.actionsTable 		import Action
from app.models.controllersTable 	import Controller


#authorization
def resource(resource_name):
	def wrapper(f):
		@wraps(f)
		def wrapped(*args, **kwargs):
			user_role	 = current_identity.role_id
			contr, act   = resource_name.split('-')

			data = db.session.query(Privilege.allow, Privilege.role_id, Controller.name.label('contr'), Action.name.label('act')) \
				.join(Resource, Privilege.resource_id == Resource.id) \
				.join(Action, Resource.action_id == Action.id) \
				.join(Controller, Resource.controller_id == Controller.id) \
				.filter(Privilege.role_id == user_role, Controller.name == contr, Action.name == act).first()

			if not data.allow:
				return jsonify({'description': 'The user do not have authorized access to the url', 'error': 'Unauthorized Access', 'status_code': 401}), 401
			return f(*args, **kwargs)
		return wrapped
	return wrapper