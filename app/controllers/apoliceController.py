from app 				import app, db, Messages
from flask 				import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy 		import exc
from . 					import resource
from app import Apolice
from app import ApoliceValidator
from app import fieldsFormatter

#--------------------------------------------------------------------------------------------------#

@app.route('/apolice/all', methods=['GET'])
@jwt_required
@resource('apolice-all')
def apoliceAll():
	
	page                       = request.args.get('page', 1, type=int)
	seguradora_idFilter 	   = request.args.get('seguradora_id', None)
	numeroFilter 	           = request.args.get('numero', None)
	centro_estagio_idFilter    = request.args.get('centro_estagio_id', None)
	inicioFilter 	           = request.args.get('inicio', None)
	fimFilter 	               = request.args.get('fim', None)
	valorFilter 	           = request.args.get('valor', None)
	quantidadeFilter 	       = request.args.get('quantidade', None)
	rowsPerPage 		       = app.config['ROWS_PER_PAGE']
	
	query = Apolice.query.order_by(Apolice.nome)
	
	if(numeroFilter != None):
		query = query.filter_by(numero = numeroFilter)

	if(seguradora_idFilter != None):
		query = query.filter(\
			Apolice.seguradora_id.ilike("%%{}%%".format(nomeFilter))\
		)

	if(centro_estagio_idFilter != None):
		query = query.filter(\
			Apolice.centro_estagio_id.ilike("%%{}%%".format(centro_estagio_idFilter))\
		)

	if(inicioFilter != None):
		query = query.filter(\
			Apolice.inicio.ilike("%%{}%%".format(inicioFilter))\
		)

	if(fimFilter != None):
		query = query.filter(\
			Apolice.fim.ilike("%%{}%%".format(fimFilter))\
		)

	if(valorFilter != None):
		query = query.filter(\
			Apolice.valor.ilike("%%{}%%".format(valorFilter))\
		)

	if(quantidadeFilter != None):
		query = query.filter(\
			Apolice.quantidade.ilike("%%{}%%".format(quantidadeFilter))\
		)


	pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
	apolices = pagination.items
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
	
	for apolice in apolices:		
		data = {}
		data['seguradora_id'] = apolice.seguradora_id
		data['numero'] = apolice.numero
		data['centro_estagio_id'] = apolice.centro_estagio_id
		data['inicio'] = apolice.inicio
		data['fim'] = apolice.fim
		data['valor'] = apolice.valor
		data['quantidade'] = apolice.quantidade

		output['itens'].append(data)

	return jsonify(output)

#--------------------------------------------------------------------------------------------------#

@app.route('/apolice/view/<apolice_id>', methods=['GET'])
@jwt_required
@resource('apolice-view')
def apoliceView(apolice_id):
	apolice = Apolice.query.get(apolice_id)
	
	if not apolice:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(apolice_id), 'error': True})

	data = {'error': False}
	data['seguradora_id'] = apolice.seguradora_id
	data['numero'] = apolice.numero
	data['centro_estagio_id'] = apolice.centro_estagio_id
	data['inicio'] = apolice.inicio
	data['fim'] = apolice.fim
	data['valor'] = apolice.valor
	data['quantidade'] = apolice.quantidade
	
	return jsonify(data)

#--------------------------------------------------------------------------------------------------#

@app.route('/apolice/add', methods=['POST'])
@jwt_required
@resource('apolice-add')
def apoliceAdd():
	data = request.get_json()
	validator = ApoliceValidator(data)
	errors = validator.validate()
	
	if(errors['has']):
		return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

	apolice	= Apolice( 
		seguradora_id = data['seguradora_id'],
		centro_estagio_id = data['centro_estagio_id'],
		inicio = data['inicio'],
		fim = data['fim'],
		valor = data['valor'],
		quantidade = data['quantidade']
	)

	db.session.add(apolice)

	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_CREATED.format("Apolice"), 'error': False})
	except exc.IntegrityError:
		db.session.rollback()
		return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#

@app.route('/apolice/edit/<apolice_id>', methods=['PUT'])
@jwt_required
@resource('apolice-edit')
def apoliceEdit(apolice_id):
	apolice = Apolice.query.get(apolice_id)

	if not apolice:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(apolice_id), 'error': True})

	data = request.get_json()
	validator = ApoliceValidator(data)
	errors = validator.validate()
	
	if(errors['has']):
		return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

	apolice.seguradora_id = data['seguradora_id'],
	apolice.centro_estagio_id = data['centro_estagio_id'],
	apolice.inicio = data['inicio'],
	apolice.fim = data['fim'],
	apolice.valor = data['valor'],
	apolice.quantidade = data['quantidade']
	
	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_UPDATED.format("Apolice"), 'error': False})
	except exc.IntegrityError:
		db.session.rollback()
		return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#

@app.route('/apolice/delete/<apolice_id>', methods=['DELETE'])
@jwt_required
@resource('apolice-delete')
def apoliceDelete(apolice_id):
	apolice = Apolice.query.get(apolice_id)

	if not apolice:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(apolice_id), 'error': True})

	db.session.delete(apolice)

	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_DELETED.format("Apolice"), 'error': False})
	except exc.IntegrityError:
		return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})
