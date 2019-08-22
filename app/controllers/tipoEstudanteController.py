from app 				import app, db, Messages
from flask 				import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy 		import exc
from . 					import resource
from app 				import TipoEstudante
from app 				import TipoEstudanteValidator
from app 				import fieldsFormatter

#--------------------------------------------------------------------------------------------------#

@app.route('/tipo-estudante/all', methods=['GET'])
@jwt_required
@resource('tipoEstudante-all')
def tipoEstudanteAll():
	
	page 				= request.args.get('page', 1, type=int)
	nomeFilter 			= request.args.get('nome', None)
	rowsPerPage 		= app.config['ROWS_PER_PAGE']
	
	query = TipoEstudante.query.order_by(TipoEstudante.nome)
	
	if(nomeFilter != None):
		query = query.filter(\
			TipoEstudante.nome.ilike("%%{}%%".format(nomeFilter))\
		)

	pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
	tiposEstudante = pagination.items
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
	
	for tipo in tiposEstudante:	
		data = {}
		data['id'] = tipo.id
		data['nome'] = tipo.nome
		
		output['itens'].append(data)

	return jsonify(output)

#--------------------------------------------------------------------------------------------------#

@app.route('/tipo-estudante/view/<tipo_estudante_id>', methods=['GET'])
@jwt_required
@resource('tipoEstudante-view')
def tipoEstudanteView(tipo_estudante_id):
	tipo = TipoEstudante.query.get(tipo_estudante_id)
	
	if not tipo:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(tipo_estudante_id), 'error': True})

	data = {'error': False}
	data['id'] = tipo.id
	data['nome'] = tipo.nome
	
	return jsonify(data)

#--------------------------------------------------------------------------------------------------#

@app.route('/tipo-estudante/add', methods=['POST'])
@jwt_required
@resource('tipoEstudante-add')
def tipoEstudanteAdd():
	data 			= request.get_json()
	validator = TipoEstudanteValidator(data)
	errors = validator.validate()
	
	if(errors['has']):
		return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

	tipo = TipoEstudante( 
		nome = data['nome']
	)

	db.session.add(tipo)

	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_CREATED.format("Tipo de Estudante"), 'error': False})
	except exc.IntegrityError:
		db.session.rollback()
		return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#

@app.route('/tipo-estudante/edit/<tipo_estudante_id>', methods=['PUT'])
@jwt_required
@resource('tipoEstudante-edit')
def tipoEstudanteEdit(tipo_estudante_id):
	tipoEstudante = TipoEstudante.query.get(tipo_estudante_id)

	if not tipoEstudante:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(tipo_estudante_id), 'error': True})

	data = request.get_json()
	validator = TipoEstudanteValidator(data)
	errors = validator.validate()
	
	if(errors['has']):
		return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

	tipoEstudante.nome = data['nome']
	
	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_UPDATED.format("Tipo de Estudante"), 'error': False})
	except exc.IntegrityError:
		db.session.rollback()
		return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#

@app.route('/tipo-estudante/delete/<tipo_estudante_id>', methods=['DELETE'])
@jwt_required
@resource('tipoEstudante-delete')
def tipoEstudanteDelete(tipo_estudante_id):
	tipoEstudante = TipoEstudante.query.get(tipo_estudante_id)

	if not tipoEstudante:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(tipo_estudante_id), 'error': True})

	db.session.delete(tipoEstudante)

	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_DELETED.format("Tipo de Estudante"), 'error': False})
	except exc.IntegrityError:
		return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})
