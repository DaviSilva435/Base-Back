from app 				import app, db, Messages
from flask 				import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy 		import exc
from . 					import resource
from app import ContatoEmpresa
from app import ContatoEmpresaValidator
from app import fieldsFormatter

#--------------------------------------------------------------------------------------------------#

@app.route('/contato-empresa/all', methods=['GET'])
@jwt_required
@resource('contatoEmpresa-all')
def contatoEmpresaAll():
	
	page 				= request.args.get('page', 1, type=int)
	empresaIdFilter		= request.args.get('empresa_id', None)
	rowsPerPage 		= app.config['ROWS_PER_PAGE']
	
	query = ContatoEmpresa.query.order_by(ContatoEmpresa.nome)
	
	if(empresaIdFilter != None):
		query = query.filter(\
			ContatoEmpresa.empresa_id == empresaIdFilter\
		)

	pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
	contatos = pagination.items
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
	
	for contato in contatos:	
		data = {}
		data['id'] = contato.id
		data['email'] = contato.email
		data['nome'] = contato.nome
		data['cargo'] = contato.cargo
		data['telefone'] = fieldsFormatter.PhoneFormatter().format(contato.telefone)
		data['celular'] = fieldsFormatter.PhoneFormatter().format(contato.celular)
		data['principal'] = contato.principal
		data['empresa_id'] = contato.empresa_id
		data['empresa'] = {}
		data['empresa']['id'] = contato.empresa.id
		data['empresa']['razao_social'] = contato.empresa.razao_social
		data['empresa']['nome_fantasia'] = contato.empresa.nome_fantasia
		data['empresa']['cnpj'] = fieldsFormatter.PhoneFormatter().format(contato.empresa.cnpj)
		
		output['itens'].append(data)

	return jsonify(output)

#--------------------------------------------------------------------------------------------------#

@app.route('/contato-empresa/view/<contato_empresa_id>', methods=['GET'])
@jwt_required
@resource('contatoEmpresa-view')
def contatoEmpresaView(contato_empresa_id):
	contato = ContatoEmpresa.query.get(contato_empresa_id)
	
	if not contato:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(contato_empresa_id), 'error': True})

	data = {'error': False}
	data['id'] = contato.id
	data['email'] = contato.email
	data['nome'] = contato.nome
	data['cargo'] = contato.cargo
	data['telefone'] = fieldsFormatter.PhoneFormatter().format(contato.telefone)
	data['celular'] = fieldsFormatter.PhoneFormatter().format(contato.celular)
	data['principal'] = contato.principal
	data['empresa_id'] = contato.empresa_id
	data['empresa'] = {}
	data['empresa']['id'] = contato.empresa.id
	data['empresa']['razao_social'] = contato.empresa.razao_social
	data['empresa']['nome_fantasia'] = contato.empresa.nome_fantasia
	data['empresa']['cnpj'] = fieldsFormatter.PhoneFormatter().format(contato.empresa.cnpj)
	
	return jsonify(data)

#--------------------------------------------------------------------------------------------------#

@app.route('/contato-empresa/add', methods=['POST'])
@jwt_required
@resource('contatoEmpresa-add')
def contatoEmpresaAdd():
	data 			= request.get_json()
	validator = ContatoEmpresaValidator(data)
	errors = validator.validate()
	
	if(errors['has']):
		return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

	contato = ContatoEmpresa( 
		email = data['email'],
		empresa_id = data['empresa_id'],
		nome = data['nome'],
		principal = data['principal'],
		celular = fieldsFormatter.PhoneFormatter().clean(data['celular']),
		telefone = fieldsFormatter.PhoneFormatter().clean(data['telefone']),
		cargo = data['cargo']
	)

	db.session.add(contato)

	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_CREATED.format("Contato da Empresa"), 'error': False})
	except exc.IntegrityError:
		db.session.rollback()
		return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#

@app.route('/contato-empresa/edit/<contato_empresa_id>', methods=['PUT'])
@jwt_required
@resource('contatoEmpresa-edit')
def contatoEmpresaEdit(contato_empresa_id):
	contato = ContatoEmpresa.query.get(contato_empresa_id)

	if not contato:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(contato_empresa_id), 'error': True})

	data = request.get_json()
	validator = ContatoEmpresaValidator(data)
	errors = validator.validate()
	
	if(errors['has']):
		return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

	contato.email = data['email']
	contato.empresa_id = data['empresa_id']
	contato.nome = data['nome']
	contato.principal = data['principal']
	contato.celular = fieldsFormatter.PhoneFormatter().clean(data['celular'])
	contato.telefone = fieldsFormatter.PhoneFormatter().clean(data['telefone'])
	contato.cargo = data['cargo']
	
	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_UPDATED.format("Contato da Empresa"), 'error': False})
	except exc.IntegrityError:
		db.session.rollback()
		return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#

@app.route('/contato-empresa/delete/<contato_empresa_id>', methods=['DELETE'])
@jwt_required
@resource('contatoEmpresa-delete')
def contatoEmpresaDelete(contato_empresa_id):
	contato = ContatoEmpresa.query.get(contato_empresa_id)

	if not contato:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(contato_empresa_id), 'error': True})

	db.session.delete(contato)

	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_DELETED.format("Contato da Empresa"), 'error': False})
	except exc.IntegrityError:
		return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})
