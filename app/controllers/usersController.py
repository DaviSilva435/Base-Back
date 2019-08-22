from app 				import app, db, Messages
from flask 				import request, jsonify
from flask_jwt_extended	import jwt_required
from sqlalchemy 		import exc
from werkzeug.security 	import generate_password_hash
from . 					import resource
from app import User
from app import UserValidator
from app import fieldsFormatter

@app.route('/user/all', methods=['GET'])
@jwt_required
@resource('users-all')
def userAll():

	page 			= request.args.get('page', 1, type=int)
	usernameFilter 	= request.args.get('username', None)
	rowsPerPage 	= app.config['ROWS_PER_PAGE']
	query = User.query.order_by(User.username)

	if(usernameFilter != None):
		query = query.filter(\
			User.username.ilike("%%{}%%".format(usernameFilter))\
		)

	pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
	users = pagination.items
	output = {
		"pagination": {
			"pages_count": pagination.pages,
			"itens_count": pagination.total,
			"itens_per_page": rowsPerPage,
			"prev": pagination.prev_num,
			"next": pagination.next_num,
			"current": pagination.page,
		},
		"itens": [],
		"error": False,
	}

	for user in users:
		data = {}
		data['id'] 					= user.id
		data['username'] 			= user.username
		data['email'] 				= user.email
		data['role_id']				= user.role_id
		data['role'] 				= {}
		data['role']['id']  		= user.roles.id
		data['role']['name']  		= user.roles.name
		data['empresa_id']			= user.empresa_id
		data['centro_estagio_id']	= user.centro_estagio_id

		if user.empresa:
			data['empresa']			= {}
			data['empresa']['id'] 	= user.empresa.id
			data['empresa']['nome'] = user.empresa.razao_social
			data['empresa']['cnpj'] = fieldsFormatter.CnpjFormatter().format(user.empresa.cnpj)

		if user.centro_estagio:
			data['centro_estagio']			= {}
			data['centro_estagio']['id'] 	= user.centro_estagio.id
			data['centro_estagio']['nome'] 	= user.centro_estagio.razao_social
			data['centro_estagio']['cnpj'] 	= fieldsFormatter.CnpjFormatter().format(user.centro_estagio.cnpj)

		output['itens'].append(data)

	return jsonify(output)

#--------------------------------------------------------------------------------------------------#

@app.route('/user/view/<user_id>', methods=['GET'])
@jwt_required
@resource('users-view')
def userView(user_id):
	user = User.query.get(user_id)

	if not user:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(user_id), 'error': True})

	data = {'error': False}
	data['id'] 					= user.id
	data['username'] 			= user.username
	data['email'] 				= user.email
	data['role_id']				= user.role_id
	data['role'] 				= {}
	data['role']['id']  		= user.roles.id
	data['role']['name']  		= user.roles.name
	data['empresa_id']			= user.empresa_id
	data['centro_estagio_id']	= user.centro_estagio_id

	if user.empresa:
		data['empresa']			= {}
		data['empresa']['id'] 	= user.empresa.id
		data['empresa']['nome'] = user.empresa.razao_social
		data['empresa']['cnpj'] = fieldsformatter.CnpjFormatter().format(user.empresa.cnpj)

	if user.centro_estagio:
		data['centro_estagio']			= {}
		data['centro_estagio']['id'] 	= user.centro_estagio.id
		data['centro_estagio']['nome'] 	= user.centro_estagio.razao_social
		data['centro_estagio']['cnpj'] 	= fieldsFormatter.CnpjFormatter().format(user.centro_estagio.cnpj)

	return jsonify(data)

#--------------------------------------------------------------------------------------------------#

@app.route('/user/add', methods=['POST'])
@jwt_required
@resource('users-add')
def userAdd():
	data = request.get_json()
	validator = UserValidator(data)
	validator.addPasswordField()

	errors = validator.validate()

	if(errors['has']):
		return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

	errors = validator.validateUsername()

	if(errors['has']):
		return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

	if(data['empresa_id'] == '' or data['empresa_id'] == None):
		data['empresa_id'] = None
	if(data['centro_estagio_id'] == ''):
		data['centro_estagio_id'] = None

	hashed_pass     = generate_password_hash(data['password'], method='sha256')
	user 			= User(
		username=data['username'], \
		password=hashed_pass, \
		role_id=data['role_id'], \
		email=data['email'], \
		empresa_id=data['empresa_id'],
		centro_estagio_id=data['centro_estagio_id']
	)

	db.session.add(user)

	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_CREATED.format("Usuário"), 'error': False})
	except exc.IntegrityError:
		db.session.rollback()
		return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#

@app.route('/user/edit/<user_id>', methods=['PUT'])
@jwt_required
@resource('users-edit')
def userEdit(user_id):
	user = User.query.get(user_id)

	if not user:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(user_id), 'error': True})

	data = request.get_json()
	validator = UserValidator(data)
	errors = validator.validate()

	if(errors['has']):
		return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

	user.username 			= data['username']
	user.email	  			= data['email']
	user.role_id  			= data['role_id']
	user.centro_estagio_id 	= data['centro_estagio_id']
	user.empresa_id  		= data['empresa_id']

	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_UPDATED.format("Usuário"), 'error': False})
	except exc.IntegrityError:
		db.session.rollback()
		return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#

@app.route('/user/delete/<user_id>', methods=['DELETE'])
@jwt_required
@resource('users-delete')
def userDelete(user_id):
	user = User.query.get(user_id)

	if not user:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(user_id), 'error': True})

	db.session.delete(user)

	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_DELETED.format("Usuário"), 'error': False})
	except exc.IntegrityError:
		return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})
