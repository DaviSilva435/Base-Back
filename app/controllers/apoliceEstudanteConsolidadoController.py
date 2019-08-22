from app 				import app, db, Messages
from flask 				import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy 		import exc
from . 					import resource
from app import ApoliceEstudanteConsolidado
from app import ApoliceEstudanteConsolidadoValidator
from app import fieldsFormatter

#--------------------------------------------------------------------------------------------------#

@app.route('/apolice-estudante-consolidado/all', methods=['GET'])
@jwt_required
@resource('apoliceEstudanteConsolidado-all')
def apoliceEstudanteConsolidadoAll():
	
	page                       = request.args.get('page', 1, type=int)
	seguradora_idFilter 	   = request.args.get('seguradora_id', None)
	numeroFilter 	           = request.args.get('numero', None)
	centro_estagio_idFilter    = request.args.get('centro_estagio_id', None)
	mesFilter 	               = request.args.get('mes', None)
	anoFilter 	               = request.args.get('ano', None)
	registro 	               = request.args.get('registro', None)
	rowsPerPage 		       = app.config['ROWS_PER_PAGE']
	
	query = ApoliceEstudanteConsolidado.query.order_by(apoliceEstudanteConsolidado.nome)
	
	if(numeroFilter != None):
		query = query.filter_by(numero = numeroFilter)

	if(seguradora_idFilter != None):
		query = query.filter(\
			ApoliceEstudanteConsolidado.seguradora_id.ilike("%%{}%%".format(seguradora_idFilter))\
		)

	if(centro_estagio_idFilter != None):
		query = query.filter(\
			ApoliceEstudanteConsolidado.centro_estagio_id.ilike("%%{}%%".format(centro_estagio_idFilter))\
		)

	if(mesFilter != None):
		query = query.filter(\
			ApoliceEstudanteConsolidado.mes.ilike("%%{}%%".format(mesFilter))\
		)

	if(anoFilter != None):
		query = query.filter(\
			ApoliceEstudanteConsolidado.ano.ilike("%%{}%%".format(anoFilter))\
		)

	if(registro != None):
		query = query.filter(\
			ApoliceEstudanteConsolidado.registro.ilike("%%{}%%".format(registro))\
		)


	pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
	apoliceEstudanteConsolidados = pagination.items
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
	
	for apoliceEstudanteConsolidado in apoliceEstudanteConsolidados:		
		data = {}
		data['seguradora_id'] = apoliceEstudanteConsolidado.seguradora_id
		data['numero'] = apoliceEstudanteConsolidado.numero
		data['centro_estagio_id'] = apoliceEstudanteConsolidado.centro_estagio_id
		data['mes'] = apoliceEstudanteConsolidado.mes
		data['ano'] = apoliceEstudanteConsolidado.ano
		data['registro'] = apoliceEstudanteConsolidado.registro

		output['itens'].append(data)

	return jsonify(output)

#--------------------------------------------------------------------------------------------------#

@app.route('/apolice-estudante-consolidado/view/<apolice_estudante_consolidado_id>', methods=['GET'])
@jwt_required
@resource('apoliceEstudanteConsolidado-view')
def apoliceEstudanteConsolidadoConsolidadoView(apolice_estudante_consolidado_id):
	apoliceEstudanteConsolidado = ApoliceEstudanteConsolidado.query.get(apolice_estudante_consolidado_id)
	
	if not apoliceEstudanteConsolidado:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(apolice_estudante_consolidado_id), 'error': True})

	data = {'error': False}
	data['seguradora_id'] = apoliceEstudanteConsolidado.seguradora_id
	data['numero'] = apoliceEstudanteConsolidado.numero
	data['centro_estagio_id'] = apoliceEstudanteConsolidado.centro_estagio_id
	data['mes'] = apoliceEstudanteConsolidado.mes
	data['ano'] = apoliceEstudanteConsolidado.ano
	data['registro'] = apoliceEstudanteConsolidado.registro
	
	return jsonify(data)

#--------------------------------------------------------------------------------------------------#

@app.route('/apolice-estudante-consolidado/add', methods=['POST'])
@jwt_required
@resource('apoliceEstudanteConsolidado-add')
def apoliceEstudanteConsolidadoConsolidadoAdd():
	data = request.get_json()
	validator = ApoliceEstudanteConsolidadoValidator(data)
	errors = validator.validate()
	
	if(errors['has']):
		return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

	apoliceEstudanteConsolidado	= ApoliceEstudanteConsolidado( 
		seguradora_id = data['seguradora_id'],
		centro_estagio_id = data['centro_estagio_id'],
		mes = data['mes'],
		ano = data['ano'],
		registro = data['registro'],
	)

	db.session.add(apoliceEstudanteConsolidado)

	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_CREATED.format("Apolice Estudante Consolidado"), 'error': False})
	except exc.IntegrityError:
		db.session.rollback()
		return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#

@app.route('/apolice-estudante-consolidado/edit/<apolice_estudante_consolidado_id>', methods=['PUT'])
@jwt_required
@resource('apoliceEstudanteConsolidado-edit')
def apoliceEstudanteConsolidadoConsolidadoEdit(apolice_estudante_consolidado_id):
	apoliceEstudanteConsolidado = ApoliceEstudanteConsolidado.query.get(apolice_estudante_consolidado_id)

	if not apoliceEstudanteConsolidado:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(apolice_estudante_consolidado_id), 'error': True})

	data = request.get_json()
	validator = ApoliceEstudanteConsolidadoValidator(data)
	errors = validator.validate()
	
	if(errors['has']):
		return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

	apoliceEstudanteConsolidado.seguradora_id = data['seguradora_id'],
	apoliceEstudanteConsolidado.centro_estagio_id = data['centro_estagio_id'],
	apoliceEstudanteConsolidado.mes = data['mes'],
	apoliceEstudanteConsolidado.ano = data['ano'],
	apoliceEstudanteConsolidado.registro = data['registro']
	
	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_UPDATED.format("Apolice Estudante Consolidado"), 'error': False})
	except exc.IntegrityError:
		db.session.rollback()
		return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#

@app.route('/apolice-estudante-consolidado/delete/<apolice_estudante_consolidado_id>', methods=['DELETE'])
@jwt_required
@resource('apoliceEstudanteConsolidado-delete')
def apoliceEstudanteConsolidadoConsolidadoDelete(apolice_estudante_consolidado_id):
	apoliceEstudanteConsolidado = ApoliceEstudanteConsolidado.query.get(apolice_estudante_consolidado_id)

	if not apoliceEstudanteConsolidado:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(apolice_estudante_consolidado_id), 'error': True})

	db.session.delete(apoliceEstudanteConsolidado)

	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_DELETED.format("Apolice Estudante Consolidado"), 'error': False})
	except exc.IntegrityError:
		return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})
