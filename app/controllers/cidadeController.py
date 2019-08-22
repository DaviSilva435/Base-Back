from app import app, db, Messages
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy 		import exc
from . 					import resource

from app import Cidade
from app import Uf
from app import CidadeValidator

#--------------------------------------------------------------------------------------------------#

@app.route('/cidade/all', methods=['GET'])
@jwt_required
@resource('cidade-all')
def cidadeAll():

    page = request.args.get('page', 1, type=int)
    nomeFilter = request.args.get('nome', None)
    idFilter = request.args.get('id', None)
    ibgeFilter = request.args.get('ibge', None)
    uf_idFilter = request.args.get('uf_id', None)
    rowsPerPage = app.config['ROWS_PER_PAGE']

    query = Cidade.query.order_by(Cidade.nome)

    if (nomeFilter != None):
        query = query.filter( \
            Cidade.nome.ilike("%%{}%%".format(nomeFilter)) \
            )

    if (idFilter != None):
        query = query.filter_by(id = idFilter)

    if (uf_idFilter != None):
        query = query.filter_by(uf_id = uf_idFilter)

    if (ibgeFilter != None):
        query = query.filter( \
            Cidade.ibge.ilike("%%{}%%".format(ibgeFilter)) \
            )

    pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
    cidades = pagination.items

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

    for busca in cidades:
        data = {}
        data['id'] = busca.id
        data['cidade'] = busca.nome
        data['ibge'] = busca.ibge

        output['itens'].append(data)

    return jsonify(output)

#--------------------------------------------------------------------------------------------------#

@app.route('/cidade/view/<cidade_id>', methods=['GET'])
@jwt_required
@resource('cidade-view')
def cidadeView(cidade_id):

    cidade = Cidade.query.get(cidade_id)
    if not cidade:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(cidade_id), 'error': True})

    estado = Uf.query.get(cidade.uf_id)
    if not estado:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(uf_id), 'error': True})

    data = {'error': False}
    data['nome'] = cidade.nome
    data['ibge'] = cidade.ibge
    data['id'] = cidade.id
    data['estado'] = estado.nome

    return jsonify(data)

#--------------------------------------------------------------------------------------------------#

@app.route('/cidade/add', methods=['POST'])
@jwt_required
@resource('cidade-add')
def cidadeAdd():

    data = request.get_json()
    validator = CidadeValidator(data)
    errors = validator.validate()

    if(errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    cidade = Cidade(data['nome'], data['ibge'], data['uf_id'])

    db.session.add(cidade)

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_CREATED.format("Cidade"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#

@app.route('/cidade/edit/<cidade_id>', methods = ['PUT'])
@jwt_required
@resource('cidade-edit')
def cidadeEdit(cidade_id):
    cidade = Cidade.query.get(cidade_id)

    if not cidade:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(cidade_id), 'error': True})

    data = request.get_json()
    validator = CidadeValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    cidade.nome = data['nome']
    cidade.ibge = data['ibge']
    cidade.uf_id = data['uf_id']

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_UPDATED.format("Cidade"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#

@app.route('/cidade/delete/<cidade_id>', methods = ['DELETE'])
@jwt_required
@resource('cidade-delete')
def cidadeDelete(cidade_id):
    cidade = Cidade.query.get(cidade_id)

    if not cidade:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(cidade_id), 'error': True})

    db.session.delete(cidade)

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_DELETED.format("Cidade"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})

