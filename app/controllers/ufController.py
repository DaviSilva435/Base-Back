from app 				import app, db, Messages
from flask 				import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy 		import exc
from . 					import resource
from app import Uf
from app import UfValidator

#--------------------------------------------------------------------------------------------------#

@app.route('/uf/all', methods=['GET'])
@jwt_required
@resource('cidades-all')
def ufAll():
	
	page 				= request.args.get('page', 1, type=int)
	nomeFilter 	        = request.args.get('nome', None)
	siglaFilter			= request.args.get('sigla', None)
	idFilter 			= request.args.get('id', type=int)
	rowsPerPage			= request.args.get('rows-per-page', type = int)


	query = Uf.query.order_by(Uf.nome)

	if (rowsPerPage == None):
		rowsPerPage = app.config['ROWS_PER_PAGE']

	if(idFilter != None):
		query = query.filter_by(id = idFilter)

	if(nomeFilter != None):
		query = query.filter(\
			Uf.nome.ilike("%%{}%%".format(nomeFilter))\
		)
	if (siglaFilter != None):
		query = query.filter( \
			Uf.sigla.ilike("%%{}%%".format(siglaFilter)) \
		)


	pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
	ufs = pagination.items
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
	
	for uf in ufs:		
		data = {}
		data['id'] = uf.id
		data['nome'] = uf.nome
		data['sigla'] = uf.sigla

		output['itens'].append(data)

	return jsonify(output)

#--------------------------------------------------------------------------------------------------#

@app.route('/uf/view/<uf_id>', methods=['GET'])
@jwt_required
@resource('uf-view')
def ufView(uf_id):
	uf = Uf.query.get(uf_id)
	
	if not uf:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(uf_id), 'error': True})

	data = {'error': False}
	data['id'] = uf.id
	data['nome'] = uf.nome
	data['sigla'] = uf.sigla
	
	return jsonify(data)

#--------------------------------------------------------------------------------------------------#

@app.route('/uf/add', methods=['POST'])
@jwt_required
@resource('uf-add')
def ufAdd():
	data 			= request.get_json()
	validator = UfValidator(data)
	errors = validator.validate()
	
	if(errors['has']):
		return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

	uf	= Uf( 
		nome = data['nome'],
		sigla = data['sigla']
	)

	db.session.add(uf)

	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_CREATED.format("Uf"), 'error': False})
	except exc.IntegrityError:
		db.session.rollback()
		return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#

@app.route('/uf/edit/<uf_id>', methods=['PUT'])
@jwt_required
@resource('uf-edit')
def ufEdit(uf_id):
	uf = Uf.query.get(uf_id)

	if not uf:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(uf_id), 'error': True})

	data = request.get_json()
	validator = UfValidator(data)
	errors = validator.validate()
	
	if(errors['has']):
		return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

	uf.nome = data['nome'],
	uf.sigla = data['sigla']
	
	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_UPDATED.format("Uf"), 'error': False})
	except exc.IntegrityError:
		db.session.rollback()
		return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#

@app.route('/uf/delete/<uf_id>', methods=['DELETE'])
@jwt_required
@resource('uf-delete')
def ufDelete(uf_id):
	uf = Uf.query.get(uf_id)

	if not uf:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(uf_id), 'error': True})

	db.session.delete(uf)

	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_DELETED.format("Uf"), 'error': False})
	except exc.IntegrityError:
		return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})
