from app 				import app, db, Messages
from flask 				import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy 		import exc
from . 					import resource
from app import ApoliceEstudante
from app import ApoliceEstudanteValidator
from app import fieldsFormatter

#--------------------------------------------------------------------------------------------------#

@app.route('/apolice-estudante/all', methods=['GET'])
@jwt_required
@resource('apoliceEstudante-all')
def apoliceEstudanteAll():
	
	page                       = request.args.get('page', 1, type=int)
	seguradora_idFilter 	   = request.args.get('seguradora_id', None)
	numeroFilter 	           = request.args.get('numero', None)
	centro_estagio_idFilter    = request.args.get('centro_estagio_id', None)
	mesFilter 	               = request.args.get('mes', None)
	anoFilter 	               = request.args.get('ano', None)
	estudante_idFilter 	       = request.args.get('estudante_id', None)
	rowsPerPage 		       = app.config['ROWS_PER_PAGE']
	
	query = ApoliceEstudante.query.order_by(ApoliceEstudante.numero)
	
	if(numeroFilter != None):
		query = query.filter_by(numero = numeroFilter)

	if(seguradora_idFilter != None):
		query = query.filter(\
			ApoliceEstudante.seguradora_id.ilike("%%{}%%".format(seguradora_idFilter))\
		)

	if(centro_estagio_idFilter != None):
		query = query.filter(\
			ApoliceEstudante.centro_estagio_id.ilike("%%{}%%".format(centro_estagio_idFilter))\
		)

	if(mesFilter != None):
		query = query.filter(\
			ApoliceEstudante.mes.ilike("%%{}%%".format(mesFilter))\
		)

	if(anoFilter != None):
		query = query.filter(\
			ApoliceEstudante.ano.ilike("%%{}%%".format(anoFilter))\
		)

	if(estudante_idFilter != None):
		query = query.filter(\
			ApoliceEstudante.estudante_id.ilike("%%{}%%".format(estudante_idFilter))\
		)


	pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
	apoliceEstudantes = pagination.items
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
	
	for apoliceEstudante in apoliceEstudantes:		
		data = {}
		data['seguradora_id'] = apoliceEstudante.seguradora_id
		data['numero'] = apoliceEstudante.numero
		data['centro_estagio_id'] = apoliceEstudante.centro_estagio_id
		data['mes'] = apoliceEstudante.mes
		data['ano'] = apoliceEstudante.ano
		data['estudante_id'] = apoliceEstudante.estudante_id

		output['itens'].append(data)

	return jsonify(output)

#--------------------------------------------------------------------------------------------------#

@app.route('/apolice-estudante/view/<apolice_estudante_id>/<apolice_seguradora_id>/<apolice_numero>/<apolice_centro_estagio_id>/<apolice_mes>/<apolice_ano>', methods=['GET'])
@jwt_required
@resource('apoliceEstudante-view')
def apoliceEstudanteView(apolice_estudante_id, apolice_seguradora_id, apolice_numero, apolice_centro_estagio_id, apolice_mes, apolice_ano):
	apoliceEstudante = ApoliceEstudante.query.get([apolice_estudante_id,apolice_seguradora_id,\
	apolice_numero,apolice_centro_estagio_id,apolice_mes,apolice_ano])
	
	if not apoliceEstudante:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format([apolice_estudante_id,apolice_seguradora_id,\
	apolice_numero,apolice_centro_estagio_id,apolice_mes,apolice_ano]), 'error': True})

	data = {'error': False}
	data['seguradora_id'] = apoliceEstudante.seguradora_id
	data['numero'] = apoliceEstudante.numero
	data['centro_estagio_id'] = apoliceEstudante.centro_estagio_id
	data['mes'] = apoliceEstudante.mes
	data['ano'] = apoliceEstudante.ano
	data['estudante_id'] = apoliceEstudante.estudante_id
	
	return jsonify(data)

#--------------------------------------------------------------------------------------------------#

@app.route('/apolice-estudante/add', methods=['POST'])
@jwt_required
@resource('apoliceEstudante-add')
def apoliceEstudanteAdd():
	data = request.get_json()
	validator = ApoliceEstudanteValidator(data)
	errors = validator.validate()
	
	if(errors['has']):
		return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

	apoliceEstudante	= ApoliceEstudante( 
		seguradora_id = data['seguradora_id'],
		centro_estagio_id = data['centro_estagio_id'],
		mes = data['mes'],
		ano = data['ano'],
		estudante_id = data['estudante_id'],
	)

	db.session.add(apoliceEstudante)

	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_CREATED.format("Apolice Estudante"), 'error': False})
	except exc.IntegrityError:
		db.session.rollback()
		return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#

@app.route('/apolice-estudante/edit/<apolice_estudante_id>/<apolice_seguradora_id>/<apolice_numero>/<apolice_centro_estagio_id>/<apolice_mes>/<apolice_ano>', methods=['PUT'])
@jwt_required
@resource('apoliceEstudante-edit')
def apoliceEstudanteEdit(apolice_estudante_id, apolice_seguradora_id, apolice_numero, apolice_centro_estagio_id, apolice_mes, apolice_ano):
	apoliceEstudante = ApoliceEstudante.query.get([apolice_estudante_id,apolice_seguradora_id,\
	apolice_numero,apolice_centro_estagio_id,apolice_mes,apolice_ano])

	if not apoliceEstudante:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(apolice_estudante_id), 'error': True})

	data = request.get_json()
	validator = ApoliceEstudanteValidator(data)
	errors = validator.validate()
	
	if(errors['has']):
		return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

	apoliceEstudante.seguradora_id = data['seguradora_id'],
	apoliceEstudante.centro_estagio_id = data['centro_estagio_id'],
	apoliceEstudante.mes = data['mes'],
	apoliceEstudante.ano = data['ano'],
	apoliceEstudante.estudante_id = data['estudante_id']
	
	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_UPDATED.format("Apolice Estudante"), 'error': False})
	except exc.IntegrityError:
		db.session.rollback()
		return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#

@app.route('/apolice-estudante/delete/<apolice_estudante_id>/<apolice_seguradora_id>/\
	<apolice_numero>/<apolice_centro_estagio_id>/<apolice_mes>/<apolice_ano>', methods=['DELETE'])
@jwt_required
@resource('apoliceEstudante-delete')
def apoliceEstudanteDelete(apolice_estudante_id, apolice_seguradora_id, apolice_numero, apolice_centro_estagio_id, apolice_mes, apolice_ano):
	apoliceEstudante = ApoliceEstudante.query.get([apolice_estudante_id,apolice_seguradora_id,\
	apolice_numero,apolice_centro_estagio_id,apolice_mes,apolice_ano])

	if not apoliceEstudante:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(apolice_estudante_id), 'error': True})

	db.session.delete(apoliceEstudante)

	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_DELETED.format("Apolice Estudante"), 'error': False})
	except exc.IntegrityError:
		return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})
