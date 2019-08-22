from app 				import app, db, Messages
from flask 				import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy 		import exc
from . 					import resource
from app import Empresa
from app import EmpresaValidator
from app import fieldsFormatter

#--------------------------------------------------------------------------------------------------#

@app.route('/empresa/all', methods=['GET'])
@jwt_required
@resource('empresa-all')
def empresaAll():
	
	page 				= request.args.get('page', 1, type=int)
	razaoSocialFilter 	= request.args.get('razao_social', None)
	nomeFantasiaFilter 	= request.args.get('nome_fantasia', None)
	cnpjFilter 			= request.args.get('cnpj', None)
	rowsPerPage 		= app.config['ROWS_PER_PAGE']
	
	query = Empresa.query.order_by(Empresa.razao_social)
	
	if(razaoSocialFilter != None):
		query = query.filter(\
			Empresa.razao_social.ilike("%%{}%%".format(razaoSocialFilter))\
		)

	if(nomeFantasiaFilter != None):
		query = query.filter(\
			Empresa.nome_fantasia.ilike("%%{}%%".format(nomeFantasiaFilter))\
		)

	if(cnpjFilter != None):
		query = query.filter(\
			Empresa.cnpj.ilike("%%{}%%".format(cnpjFilter))\
		)

	pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
	empresas = pagination.items
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
	
	for empresa in empresas:	
		data = {}
		data['id'] = empresa.id
		data['razao_social'] = empresa.razao_social
		data['nome_fantasia'] = empresa.nome_fantasia
		data['endereco'] = empresa.endereco
		data['bairro'] = empresa.bairro
		data['cep'] = fieldsFormatter.CepFormatter().format(empresa.cep)
		data['fone'] = fieldsFormatter.PhoneFormatter().format(empresa.fone)
		data['cnpj'] = fieldsFormatter.CnpjFormatter().format(empresa.cnpj)
		data['complemento'] = empresa.complemento
		data['cidade_id'] = empresa.cidade_id
		
		data['cidade'] = {}
		data['cidade']['id'] = empresa.cidade.id
		data['cidade']['nome'] = empresa.cidade.nome
		data['cidade']['uf_id'] = empresa.cidade.uf_id

		data['cidade']['uf'] = {}
		data['cidade']['uf']['id'] = empresa.cidade.uf.id
		data['cidade']['uf']['nome'] = empresa.cidade.uf.nome
		data['cidade']['uf']['sigla'] = empresa.cidade.uf.sigla

		data['contatos'] = []
		for contato in empresa.contatos:
			dataContato = {}
			dataContato['id'] = contato.id
			dataContato['email'] = contato.email
			dataContato['nome'] = contato.nome
			dataContato['cargo'] = contato.cargo
			dataContato['telefone'] = fieldsFormatter.PhoneFormatter().format(contato.telefone)
			dataContato['celular'] = fieldsFormatter.PhoneFormatter().format(contato.celular)
			dataContato['principal'] = contato.principal

			data['contatos'].append(dataContato)

		output['itens'].append(data)

	return jsonify(output)

#--------------------------------------------------------------------------------------------------#

@app.route('/empresa/view/<empresa_id>', methods=['GET'])
@jwt_required
@resource('empresa-view')
def empresaView(empresa_id):
	empresa = Empresa.query.get(empresa_id)
	
	if not empresa:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(empresa_id), 'error': True})

	data = {'error': False}
	data['id'] = empresa.id
	data['razao_social'] = empresa.razao_social
	data['nome_fantasia'] = empresa.nome_fantasia
	data['endereco'] = empresa.endereco
	data['bairro'] = empresa.bairro
	data['cep'] = fieldsFormatter.CepFormatter().format(empresa.cep)
	data['fone'] = fieldsFormatter.PhoneFormatter().format(empresa.fone)
	data['cnpj'] = fieldsFormatter.CnpjFormatter().format(empresa.cnpj)
	data['complemento'] = empresa.complemento
	data['cidade_id'] = empresa.cidade_id
	
	data['cidade'] = {}
	data['cidade']['id'] = empresa.cidade.id
	data['cidade']['nome'] = empresa.cidade.nome
	data['cidade']['uf_id'] = empresa.cidade.uf_id

	data['cidade']['uf'] = {}
	data['cidade']['uf']['id'] = empresa.cidade.uf.id
	data['cidade']['uf']['nome'] = empresa.cidade.uf.nome
	data['cidade']['uf']['sigla'] = empresa.cidade.uf.sigla

	data['contatos'] = []
	for contato in empresa.contatos:
		dataContato = {}
		dataContato['id'] = contato.id
		dataContato['email'] = contato.email
		dataContato['nome'] = contato.nome
		dataContato['cargo'] = contato.cargo
		dataContato['telefone'] = fieldsFormatter.PhoneFormatter().format(contato.telefone)
		dataContato['celular'] = fieldsFormatter.PhoneFormatter().format(contato.celular)
		dataContato['principal'] = contato.principal

		data['contatos'].append(dataContato)
	
	return jsonify(data)

#--------------------------------------------------------------------------------------------------#

@app.route('/empresa/add', methods=['POST'])
@jwt_required
@resource('empresa-add')
def empresaAdd():
	data 			= request.get_json()
	validator = EmpresaValidator(data)
	errors = validator.validate()
	
	if(errors['has']):
		return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

	empresa	= Empresa( 
		razao_social = data['razao_social'],
		nome_fantasia = data['nome_fantasia'], 
		endereco = data['endereco'],
		bairro = data['bairro'], 
		cep = fieldsFormatter.CepFormatter().clean(data['cep']), 
		fone = fieldsFormatter.PhoneFormatter().clean(data['fone']),
		cnpj = fieldsFormatter.CnpjFormatter().clean(data['cnpj']), 
		complemento = data['complemento'], 
		cidade_id = data['cidade_id']
	)

	db.session.add(empresa)

	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_CREATED.format("Empresa"), 'error': False})
	except exc.IntegrityError:
		db.session.rollback()
		return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#

@app.route('/empresa/edit/<empresa_id>', methods=['PUT'])
@jwt_required
@resource('empresa-edit')
def empresaEdit(empresa_id):
	empresa = Empresa.query.get(empresa_id)

	if not empresa:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(empresa_id), 'error': True})

	data = request.get_json()
	validator = EmpresaValidator(data)
	errors = validator.validate()
	
	if(errors['has']):
		return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

	empresa.razao_social = data['razao_social'],
	empresa.nome_fantasia = data['nome_fantasia'], 
	empresa.endereco = data['endereco'],
	empresa.bairro = data['bairro'], 
	empresa.cep = fieldsFormatter.CepFormatter().clean(data['cep']), 
	empresa.fone = fieldsFormatter.PhoneFormatter().clean(data['fone']), 
	empresa.cnpj = fieldsFormatter.CnpjFormatter().clean(data['cnpj']), 
	empresa.complemento = data['complemento'], 
	empresa.cidade_id = data['cidade_id']
	
	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_UPDATED.format("Empresa"), 'error': False})
	except exc.IntegrityError:
		db.session.rollback()
		return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#

@app.route('/empresa/delete/<empresa_id>', methods=['DELETE'])
@jwt_required
@resource('empresa-delete')
def empresaDelete(empresa_id):
	empresa = Empresa.query.get(empresa_id)

	if not empresa:
		return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(empresa_id), 'error': True})

	db.session.delete(empresa)

	try:
		db.session.commit()
		return jsonify({'message': Messages.REGISTER_SUCCESS_DELETED.format("Empresa"), 'error': False})
	except exc.IntegrityError:
		return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})
