from app 				import app, db, Messages
from flask 				import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy 		import exc
from . 					import resource
from app import ContratoEmpresa
from app import ContratoEmpresaValidator
from app import fieldsFormatter

#--------------------------------------------------------------------------------------------------#

@app.route('/contrato-empresa/all', methods=['GET'])
@jwt_required
@resource('contratoEmpresa-all')
def contratoEmpresaAll():
	
	page 					= request.args.get('page', 1, type=int)
	empresaIdFilter			= request.args.get('empresa_id', None)
	centroEstagioIdFilter 	= request.args.get('centro_estagio_id', None)
	rowsPerPage 			= app.config['ROWS_PER_PAGE']
	
	query = ContratoEmpresa.query.order_by(ContratoEmpresa.inicio.desc())
	
	if(empresaIdFilter != None):
		query = query.filter(\
			ContratoEmpresa.empresa_id == empresaIdFilter\
		)

	if(centroEstagioIdFilter != None):
		query = query.filter(\
			ContratoEmpresa.centro_estagio_id == centroEstagioIdFilter\
		)

	pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
	contratos = pagination.items
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
	
	for contrato in contratos:	
		data = {}
		data['id'] = contrato.id
		data['centro_estagio_id'] = contrato.centro_estagio_id
		data['empresa_id'] = contrato.empresa_id
		data['inicio'] = fieldsFormatter.DateFormatter().format(contrato.inicio)
		data['fim'] = fieldsFormatter.DateFormatter().format(contrato.fim)

		data['empresa'] = {}
		data['empresa']['id'] = contrato.empresa.id
		data['empresa']['razao_social'] = contrato.empresa.razao_social
		data['empresa']['nome_fantasia'] = contrato.empresa.nome_fantasia
		data['empresa']['cnpj'] = fieldsFormatter.CnpjFormatter().format(contrato.empresa.cnpj)

		data['centro_estagio'] = {}
		data['centro_estagio']['id'] = contrato.centro_estagio.id
		data['centro_estagio']['razao_social'] = contrato.centro_estagio.razao_social
		data['centro_estagio']['nome_fantasia'] = contrato.centro_estagio.nome_fantasia
		data['centro_estagio']['cnpj'] = fieldsFormatter.CnpjFormatter().format(contrato.centro_estagio.cnpj)
		
		output['itens'].append(data)

	return jsonify(output)

#--------------------------------------------------------------------------------------------------#

@app.route('/contrato-empresa/view/<contrato_empresa_id>', methods=['GET'])
@jwt_required
@resource('contratoEmpresa-view')
def contratoEmpresaView(contrato_empresa_id):
	contrato = ContratoEmpresa.query.get(contrato_empresa_id)
	
	if not contrato:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(contrato_empresa_id), 'error': True})

	data = {'error': False}
	data['id'] = contrato.id
	data['centro_estagio_id'] = contrato.centro_estagio_id
	data['empresa_id'] = contrato.empresa_id
	data['inicio'] = fieldsFormatter.DateFormatter().format(contrato.inicio)
	data['fim'] = fieldsFormatter.DateFormatter().format(contrato.fim)

	data['empresa'] = {}
	data['empresa']['id'] = contrato.empresa.id
	data['empresa']['razao_social'] = contrato.empresa.razao_social
	data['empresa']['nome_fantasia'] = contrato.empresa.nome_fantasia
	data['empresa']['cnpj'] = fieldsFormatter.CnpjFormatter().format(contrato.empresa.cnpj)

	data['centro_estagio'] = {}
	data['centro_estagio']['id'] = contrato.centro_estagio.id
	data['centro_estagio']['razao_social'] = contrato.centro_estagio.razao_social
	data['centro_estagio']['nome_fantasia'] = contrato.centro_estagio.nome_fantasia
	data['centro_estagio']['cnpj'] = fieldsFormatter.CnpjFormatter().format(contrato.centro_estagio.cnpj)
	
	return jsonify(data)

#--------------------------------------------------------------------------------------------------#

@app.route('/contrato-empresa/add', methods=['POST'])
@jwt_required
@resource('contratoEmpresa-add')
def contratoEmpresaAdd():
	data = request.get_json()
	validator = ContratoEmpresaValidator(data)
	errors = validator.validate()
	
	if(errors['has']):
		return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

	errors = validator.validateDuplicationContract()

	if(errors['has']):
		return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200	

	contrato = ContratoEmpresa( 
		inicio = data['inicio'],
		fim = data['fim'],
		centro_estagio_id = data['centro_estagio_id'],
		empresa_id = data['empresa_id']
	)

	db.session.add(contrato)

	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_CREATED.format("Contrato da Empresa"), 'error': False})
	except exc.IntegrityError:
		db.session.rollback()
		return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#

@app.route('/contrato-empresa/edit/<contrato_empresa_id>', methods=['PUT'])
@jwt_required
@resource('contratoEmpresa-edit')
def contratoEmpresaEdit(contrato_empresa_id):
	contrato = ContratoEmpresa.query.get(contrato_empresa_id)

	if not contrato:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(contrato_empresa_id), 'error': True})

	data = request.get_json()
	validator = ContratoEmpresaValidator(data)
	errors = validator.validate()
	
	if(errors['has']):
		return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

	errors = validator.validateDuplicationContractSameId(contrato_empresa_id)

	if(errors['has']):
		return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200	

	contrato.inicio = data['inicio'],
	contrato.fim = data['fim'],
	contrato.centro_estagio_id = data['centro_estagio_id'],
	contrato.empresa_id = data['empresa_id']
	
	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_UPDATED.format("Contrato da Empresa"), 'error': False})
	except exc.IntegrityError:
		db.session.rollback()
		return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#

@app.route('/contrato-empresa/delete/<contrato_empresa_id>', methods=['DELETE'])
@jwt_required
@resource('contratoEmpresa-delete')
def contratoEmpresaDelete(contrato_empresa_id):
	contrato = ContratoEmpresa.query.get(contrato_empresa_id)

	if not contrato:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(contrato_empresa_id), 'error': True})

	db.session.delete(contrato)

	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_DELETED.format("Contrato da Empresa"), 'error': False})
	except exc.IntegrityError:
		return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})
