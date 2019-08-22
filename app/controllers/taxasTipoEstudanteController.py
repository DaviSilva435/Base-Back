from app 				import app, db, Messages
from flask 				import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy 		import exc
from . 					import resource
from app import TaxasTipoEstudante
from app import TaxasTipoEstudanteValidator
from app import fieldsFormatter

#--------------------------------------------------------------------------------------------------#

@app.route('/taxas-tipo-estudante/all', methods=['GET'])
@jwt_required
@resource('taxasTipoEstudante-all')
def taxasTipoEstudanteAll():
	
	page 				= request.args.get('page', 1, type=int)
	contratoEmpresaIdFilter = request.args.get('contrato_empresa_id', None)
	rowsPerPage 		= app.config['ROWS_PER_PAGE']
	
	query = TaxasTipoEstudante.query.order_by(TaxasTipoEstudante.tipo_estudante_id)
	
	if(contratoEmpresaIdFilter != None):
		query = query.filter(\
			TaxasTipoEstudante.contrato_empresa_id == contratoEmpresaIdFilter \
		)

	pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
	taxas = pagination.items
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
	
	for taxa in taxas:	
		data = {}
		data['valor'] = taxa.valor
		data['contrato_empresa_id'] = taxa.contrato_empresa_id
		data['tipo_estudante_id'] = taxa.tipo_estudante_id

		data['tipo_estudante'] = {}
		data['tipo_estudante']['id'] = taxa.tipo_estudante.id
		data['tipo_estudante']['nome'] = taxa.tipo_estudante.nome

		data['contrato_empresa'] = {}
		data['contrato_empresa']['id'] = taxa.contrato_empresa.id
		data['contrato_empresa']['empresa_id'] = taxa.contrato_empresa.empresa_id
		data['contrato_empresa']['inicio'] = fieldsFormatter.DateFormatter().format(taxa.contrato_empresa.inicio)
		data['contrato_empresa']['fim'] = fieldsFormatter.DateFormatter().format(taxa.contrato_empresa.fim)

		data['contrato_empresa']['empresa'] = {}
		data['contrato_empresa']['empresa']['id'] = taxa.contrato_empresa.empresa_id
		data['contrato_empresa']['empresa']['razao_social'] = taxa.contrato_empresa.razao_social
		data['contrato_empresa']['empresa']['nome_fantasia'] = taxa.contrato_empresa.nome_fantasia
		data['contrato_empresa']['empresa']['cnpj'] = fieldsFormatter.CnpjFormatter().format(taxa.contrato_empresa.cnpj)

		output['itens'].append(data)

	return jsonify(output)

#--------------------------------------------------------------------------------------------------#

@app.route('/taxas-tipo-estudante/view/<contrato_empresa_id>/<tipo_estudante_id>', methods=['GET'])
@jwt_required
@resource('taxasTipoEstudante-view')
def taxasTipoEstudanteView(contrato_empresa_id, tipo_estudante_id):
	taxa = TaxasTipoEstudante.query.filter(TaxasTipoEstudante.contrato_empresa_id == contrato_empresa_id, \
		TaxasTipoEstudante.tipo_estudante_id == tipo_estudante_id).first()
	
	if not taxa:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(taxas_tipo_estudante_id), 'error': True})

	data = {'error': False}
	data['valor'] = taxa.valor
	data['contrato_empresa_id'] = taxa.contrato_empresa_id
	data['tipo_estudante_id'] = taxa.tipo_estudante_id

	data['tipo_estudante'] = {}
	data['tipo_estudante']['id'] = taxa.tipo_estudante.id
	data['tipo_estudante']['nome'] = taxa.tipo_estudante.nome

	data['contrato_empresa'] = {}
	data['contrato_empresa']['id'] = taxa.contrato_empresa.id
	data['contrato_empresa']['empresa_id'] = taxa.contrato_empresa.empresa_id
	data['contrato_empresa']['inicio'] = fieldsFormatter.DateFormatter().format(taxa.contrato_empresa.inicio)
	data['contrato_empresa']['fim'] = fieldsFormatter.DateFormatter().format(taxa.contrato_empresa.fim)

	data['contrato_empresa']['empresa'] = {}
	data['contrato_empresa']['empresa']['id'] = taxa.contrato_empresa.empresa_id
	data['contrato_empresa']['empresa']['razao_social'] = taxa.contrato_empresa.razao_social
	data['contrato_empresa']['empresa']['nome_fantasia'] = taxa.contrato_empresa.nome_fantasia
	data['contrato_empresa']['empresa']['cnpj'] = fieldsFormatter.CnpjFormatter().format(taxa.contrato_empresa.cnpj)
	
	return jsonify(data)

#--------------------------------------------------------------------------------------------------#

@app.route('/taxas-tipo-estudante/add', methods=['POST'])
@jwt_required
@resource('taxasTipoEstudante-add')
def taxasTipoEstudanteAdd():
	data = request.get_json()
	validator = TaxasTipoEstudanteValidator(data)
	errors = validator.validate()
	
	if(errors['has']):
		return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

	taxa = TaxasTipoEstudante( 
		valor = data['valor'],
		contrato_empresa_id = data['contrato_empresa_id'],
		tipo_estudante_id = data['tipo_estudante_id']
	)

	db.session.add(taxa)

	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_CREATED.format("Taxas por Tipo de Estudante"), 'error': False})
	except exc.IntegrityError:
		db.session.rollback()
		return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#

@app.route('/taxas-tipo-estudante/edit/<contrato_empresa_id>/<tipo_estudante_id>', methods=['PUT'])
@jwt_required
@resource('taxasTipoEstudante-edit')
def taxasTipoEstudanteEdit(contrato_empresa_id, tipo_estudante_id):
	taxa = TaxasTipoEstudante.query.filter(TaxasTipoEstudante.contrato_empresa_id == contrato_empresa_id, \
		TaxasTipoEstudante.tipo_estudante_id == tipo_estudante_id).first()

	if not taxa:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(contrato_empresa_id + "/" + tipo_estudante_id), 'error': True})

	data = request.get_json()
	validator = TaxasTipoEstudanteValidator(data)
	errors = validator.validate()
	
	if(errors['has']):
		return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

	taxa.valor = data['valor'],
	taxa.contrato_empresa_id = data['contrato_empresa_id'],
	taxa.tipo_estudante_id = data['tipo_estudante_id']
	
	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_UPDATED.format("Taxas por Tipo de Estudante"), 'error': False})
	except exc.IntegrityError:
		db.session.rollback()
		return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#

@app.route('/taxas-tipo-estudante/delete/<contrato_empresa_id>/<tipo_estudante_id>', methods=['DELETE'])
@jwt_required
@resource('taxasTipoEstudante-delete')
def taxasTipoEstudanteDelete(contrato_empresa_id, tipo_estudante_id):
	taxa = TaxasTipoEstudante.query.filter(TaxasTipoEstudante.contrato_empresa_id == contrato_empresa_id, \
		TaxasTipoEstudante.tipo_estudante_id == tipo_estudante_id).first()

	if not taxa:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(contrato_empresa_id + "/" + tipo_estudante_id), 'error': True})

	db.session.delete(taxa)

	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_DELETED.format("Taxas por Tipo de Estudante"), 'error': False})
	except exc.IntegrityError:
		return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})
