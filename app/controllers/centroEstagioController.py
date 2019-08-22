from app 				import app, db, Messages
from flask 				import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy 		import exc
from . 					import resource
from app import CentroEstagio
from app import CentroEstagioValidator
from app import fieldsFormatter

#--------------------------------------------------------------------------------------------------#

@app.route('/centro-estagio/all', methods=['GET'])
@jwt_required
@resource('centroEstagio-all')
def centroEstagioAll():
	
	page 				= request.args.get('page', 1, type=int)
	razaoSocialFilter 	= request.args.get('razao_social', None)
	nomeFantasiaFilter 	= request.args.get('nome_fantasia', None)
	cnpjFilter 			= request.args.get('cnpj', None)
	rowsPerPage 		= app.config['ROWS_PER_PAGE']
	
	query = CentroEstagio.query.order_by(CentroEstagio.razao_social)
	
	if(razaoSocialFilter != None):
		query = query.filter(\
			CentroEstagio.razao_social.ilike("%%{}%%".format(razaoSocialFilter))\
		)

	if(nomeFantasiaFilter != None):
		query = query.filter(\
			CentroEstagio.nome_fantasia.ilike("%%{}%%".format(nomeFantasiaFilter))\
		)

	if(cnpjFilter != None):
		query = query.filter(\
			CentroEstagio.cnpj.ilike("%%{}%%".format(cnpjFilter))\
		)

	pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
	centrosEstagio = pagination.items
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
	
	for centro in centrosEstagio:	
		data = {}
		data['id'] = centro.id
		data['razao_social'] = centro.razao_social
		data['nome_fantasia'] = centro.nome_fantasia
		data['cnpj'] = fieldsFormatter.CnpjFormatter().format(centro.cnpj)
		data['email'] = centro.email
		data['matriz_id'] = centro.matriz_id

		if centro.matriz != None:
			data['matriz'] = {}
			data['matriz']['id'] = centro.matriz.id
			data['matriz']['nome_fantasia'] = centro.matriz.nome_fantasia
			data['matriz']['razao_social'] = centro.matriz.razao_social
			data['matriz']['cnpj'] = fieldsFormatter.CnpjFormatter().format(centro.matriz.cnpj)
 		
		output['itens'].append(data)

	return jsonify(output)

#--------------------------------------------------------------------------------------------------#

@app.route('/centro-estagio/view/<centro_estagio_id>', methods=['GET'])
@jwt_required
@resource('centroEstagio-view')
def centroEstagioView(centro_estagio_id):
	centro = CentroEstagio.query.get(centro_estagio_id)
	
	if not centro:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(centro_estagio_id), 'error': True})

	data = {'error': False}
	data['id'] = centro.id
	data['razao_social'] = centro.razao_social
	data['nome_fantasia'] = centro.nome_fantasia
	data['cnpj'] = fieldsFormatter.CnpjFormatter().format(centro.cnpj)
	data['email'] = centro.email
	data['matriz_id'] = centro.matriz_id

	if centro.matriz != None:
		data['matriz'] = {}
		data['matriz']['id'] = centro.matriz.id
		data['matriz']['nome_fantasia'] = centro.matriz.nome_fantasia
		data['matriz']['razao_social'] = centro.matriz.razao_social
		data['matriz']['cnpj'] = fieldsFormatter.CnpjFormatter().format(centro.matriz.cnpj)
	
	return jsonify(data)

#--------------------------------------------------------------------------------------------------#

@app.route('/centro-estagio/add', methods=['POST'])
@jwt_required
@resource('centroEstagio-add')
def centroEstagioAdd():
	data 			= request.get_json()
	validator = CentroEstagioValidator(data)
	errors = validator.validate()
	
	if(errors['has']):
		return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

	centro 			= CentroEstagio( 
		razao_social = data['razao_social'],
		nome_fantasia = data['nome_fantasia'], 
		cnpj = fieldsFormatter.CnpjFormatter().clean(data['cnpj']), 
		email = data['email'],
		matriz_id=data['matriz_id']
	)

	db.session.add(centro)

	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_CREATED.format("Centro de Estágio"), 'error': False})
	except exc.IntegrityError:
		db.session.rollback()
		return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#

@app.route('/centro-estagio/edit/<centro_estagio_id>', methods=['PUT'])
@jwt_required
@resource('centroEstagio-edit')
def centroEstagioEdit(centro_estagio_id):
	centro = CentroEstagio.query.get(centro_estagio_id)

	if not centro:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(centro_estagio_id), 'error': True})

	data = request.get_json()
	validator = CentroEstagioValidator(data)
	errors = validator.validate()
	
	if(errors['has']):
		return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

	centro.razao_social = data['razao_social']
	centro.nome_fantasia = data['nome_fantasia']
	centro.cnpj = fieldsFormatter.CnpjFormatter().clean(data['cnpj'])
	centro.email = data['email']
	centro.matriz_id = data['matriz_id']
	
	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_UPDATED.format("Centro de Estágio"), 'error': False})
	except exc.IntegrityError:
		db.session.rollback()
		return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#

@app.route('/centro-estagio/delete/<centro_estagio_id>', methods=['DELETE'])
@jwt_required
@resource('centroEstagio-delete')
def centroEstagioDelete(centro_estagio_id):
	centro = CentroEstagio.query.get(centro_estagio_id)

	if not centro:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(centro_estagio_id), 'error': True})

	db.session.delete(centro)

	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_DELETED.format("Centro de Estágio"), 'error': False})
	except exc.IntegrityError:
		return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})
