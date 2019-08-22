from app 				import app, db, Messages
from flask 				import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy 		import exc
from . 					import resource
from app import Escola
from app import EscolaValidator
from app import fieldsFormatter

#--------------------------------------------------------------------------------------------------#

@app.route('/escola/all', methods=['GET'])
@jwt_required
@resource('escola-all')
def escolaAll():

    page = request.args.get('page', 1, type=int)
    nomeFilter = request.args.get('nome', None)
    cepFilter = request.args.get('cep', None)
    enderecoFilter = request.args.get('endereco', None)
    bairroFilter = request.args.get('bairro', None)
    telefoneFilter = request.args.get('telefone', None)
    emailFilter = request.args.get('email', None)
    cnpjFilter = request.args.get('cnpj', None)
    cidadeFilter = request.args.get('cidade_id', None)
    rowsPerPage = app.config['ROWS_PER_PAGE']

    query = Escola.query.order_by(Escola.nome)

    if(nomeFilter != None):
        query = query.filter(
            Escola.nome.ilike("%%{}%%".format(nomeFilter))
        )
    if (cepFilter != None):
        query = query.filter(
            Escola.cep.ilike("%%{}%%".format(cepFilter))
        )
    if (enderecoFilter != None):
        query = query.filter(
            Escola.endereco.ilike("%%{}%%".format(enderecoFilter))
        )
    if (bairroFilter != None):
        query = query.filter(
            Escola.bairro.ilike("%%{}%%".format(bairroFilter))
        )
    if (telefoneFilter != None):
        query = query.filter(
            Escola.telefone.ilike("%%{}%%".format(telefoneFilter))
        )
    if (emailFilter != None):
        query = query.filter(
            Escola.email.ilike("%%{}%%".format(emailFilter))
        )
    if (cnpjFilter != None):
        query = query.filter(
            Escola.cnpj.ilike("%%{}%%".format(cnpjFilter))
        )
    if (cidadeFilter != None):
        query.filter_by(cidade_id = cidadeFilter)

    pagination = query.paginate(page = page, per_page=rowsPerPage, error_out=False)
    escolas = pagination.items
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

    for escola in escolas:
        data = {}
        data['id'] = escola.id
        data['escola'] = escola.nome
        data['cep'] = escola.cep
        data['endereco'] = escola.endereco
        data['bairro'] = escola.bairro
        data['telefone'] = escola.telefone
        data['email'] = escola.email
        data['cnpj'] = escola.cnpj
        data['cidade'] = {}
        data['cidade']['id'] = escola.cidade.id
        data['cidade']['nome'] = escola.cidade.nome
        data['cidade']['uf_id'] = escola.cidade.uf_id

        output['itens'].append(data)
    return jsonify(output)


#--------------------------------------------------------------------------------------------------#

@app.route('/escola/view/<escola_id>', methods=['GET'])
@jwt_required
@resource('escola-view')
def escolaView(escola_id):
    escola = Escola.query.get(escola_id)

    if not escola:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(escola_id), 'error': True})

    data = {'error':False}
    data['id'] = escola.id
    data['escola'] = escola.nome
    data['cep'] = escola.cep
    data['endereco'] = escola.endereco
    data['bairro'] = escola.bairro
    data['telefone'] = escola.telefone
    data['email'] = escola.email
    data['cnpj'] = escola.cnpj
    data['cidade'] = {}
    data['cidade']['id'] = escola.cidade.id
    data['cidade']['nome'] = escola.cidade.nome
    data['cidade']['uf_id'] = escola.cidade.uf_id

    return jsonify(data)

#--------------------------------------------------------------------------------------------------#

@app.route('/escola/add', methods=['POST'])
@jwt_required
@resource('escola-add')
def escolaAdd():

    data = request.get_json()
    validator = EscolaValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    escola = Escola(
        nome = data['nome'],
        cep = fieldsFormatter.CepFormatter().clean(data['cep']),
        endereco = data['endereco'],
        bairro = data['bairro'],
        cidade_id=data['cidade_id'],
        telefone = fieldsFormatter.PhoneFormatter().clean(data['telefone']),
        email = data['email'],
        cnpj = fieldsFormatter.CnpjFormatter().clean(data['cnpj'])
    )

    db.session.add(escola)

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_CREATED.format("Escola"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})

# --------------------------------------------------------------------------------------------------#

@app.route('/escola/edit/<escola_id>', methods=['PUT'])
@jwt_required
@resource('escola-edit')
def escolaEdit(escola_id):

    escola = Escola.query.get(escola_id)

    if not escola:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(escola_id), 'error': True})

    data = request.get_json()
    validator = EscolaValidator(data)
    errors = validator.validate()

    if(errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    escola.nome = data['nome']
    escola.cep = data['cep']
    escola.endereco = data['endereco']
    escola.bairro = data['bairro']
    escola.telefone = data['telefone']
    escola.email = data['email']
    escola.cnpj = data['cnpj']
    escola.cidade_id = data['cidade_id']

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_UPDATED.format("Escola"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})

# --------------------------------------------------------------------------------------------------#

@app.route('/escola/delete/<escola_id>', methods=['DELETE'])
@jwt_required
@resource('escola-delete')
def escolaDelete(escola_id):
    escola = Escola.query.get(escola_id)

    if not escola:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(escola_id), 'error': True})

    db.session.delete(escola)

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_DELETED.format("Escola"), 'error': False})
    except exc.IntegrityError:
        return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})

# --------------------------------------------------------------------------------------------------#
