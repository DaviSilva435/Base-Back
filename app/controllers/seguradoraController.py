from app 				import app, db, Messages
from flask 				import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy 		import exc
from . 					import resource
from app 				import Seguradora
from app 				import SeguradoraValidator
from app 				import fieldsFormatter

#--------------------------------------------------------------------------------------------------#

@app.route('/seguradora/all', methods=['GET'])
@jwt_required
@resource('seguradora-all')
def seguradoraAll():
	
	page 				= request.args.get('page', 1, type=int)
	nomeFilter 			= request.args.get('nome', None)
	rowsPerPage 		= app.config['ROWS_PER_PAGE']
	
	query = Seguradora.query.order_by(Seguradora.nome)
	
	if(nomeFilter != None):
		query = query.filter(\
			Seguradora.nome.ilike("%%{}%%".format(nomeFilter))\
		)

	pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
	seguradoras = pagination.items
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
	
	for seguradora in seguradoras:	
		data = {}
		data['id'] = seguradora.id
		data['nome'] = seguradora.nome
		
		output['itens'].append(data)

	return jsonify(output)

#--------------------------------------------------------------------------------------------------#

@app.route('/seguradora/view/<seguradora_id>', methods=['GET'])
@jwt_required
@resource('seguradora-view')
def seguradoraView(seguradora_id):
	seguradora = Seguradora.query.get(seguradora_id)
	
	if not seguradora:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(seguradora_id), 'error': True})

	data = {'error': False}
	data['id'] = seguradora.id
	data['nome'] = seguradora.nome
	
	return jsonify(data)

#--------------------------------------------------------------------------------------------------#

@app.route('/seguradora/add', methods=['POST'])
@jwt_required
@resource('seguradora-add')
def seguradoraAdd():
	data = request.get_json()
	validator = SeguradoraValidator(data)
	errors = validator.validate()
	
	if(errors['has']):
		return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

	seguradora = Seguradora( 
		nome = data['nome']
	)

	db.session.add(seguradora)

	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_CREATED.format("Seguradora"), 'error': False})
	except exc.IntegrityError:
		db.session.rollback()
		return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#

@app.route('/seguradora/edit/<seguradora_id>', methods=['PUT'])
@jwt_required
@resource('seguradora-edit')
def seguradoraEdit(seguradora_id):
	seguradora = Seguradora.query.get(seguradora_id)

	if not seguradora:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(seguradora_id), 'error': True})

	data = request.get_json()
	validator = SeguradoraValidator(data)
	errors = validator.validate()
	
	if(errors['has']):
		return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

	seguradora.nome = data['nome']
	
	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_UPDATED.format("Seguradora"), 'error': False})
	except exc.IntegrityError:
		db.session.rollback()
		return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#

@app.route('/seguradora/delete/<seguradora_id>', methods=['DELETE'])
@jwt_required
@resource('seguradora-delete')
def seguradoraDelete(seguradora_id):
	seguradora = Seguradora.query.get(seguradora_id)

	if not seguradora:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(seguradora_id), 'error': True})

	db.session.delete(seguradora)

	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_DELETED.format("Seguradora"), 'error': False})
	except exc.IntegrityError:
		return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})
