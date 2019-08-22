from app import app, db, Messages
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import exc
from . import resource
from app import GrauInstrucao
from app import GrauInstrucaoValidator


# --------------------------------------------------------------------------------------------------#

@app.route('/grau-instrucao/all', methods=['GET'])
@jwt_required
@resource('grauInstrucao-all')
def grauInstrucaoAll():
    page = request.args.get('page', 1, type=int)
    idFilter = request.args.get('id', None)
    nomeFilter = request.args.get('nome', None)
    rowsPerPage = app.config['ROWS_PER_PAGE']

    query = GrauInstrucao.query.order_by(GrauInstrucao.nome)

    if (idFilter != None):
        query = query.filter_by(id=idFilter)

    if (nomeFilter != None):
        query = query.filter( \
            GrauInstrucao.nome.ilike("%%{}%%".format(nomeFilter)) \
            )

    pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
    grauInstrucoes = pagination.items
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

    for grauInstrucao in grauInstrucoes:
        data = {}
        data['id'] = grauInstrucao.id
        data['nome'] = grauInstrucao.nome

        output['itens'].append(data)

    return jsonify(output)


# --------------------------------------------------------------------------------------------------#

@app.route('/grau-instrucao/view/<grau_instrucao_id>', methods=['GET'])
@jwt_required
@resource('grauInstrucao-view')
def grauInstrucaoView(grau_instrucao_id):
    grauInstrucao = GrauInstrucao.query.get(grau_instrucao_id)

    if not grauInstrucao:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(grau_instrucao_id), 'error': True})

    data = {'error': False}
    data['id'] = grauInstrucao.id
    data['nome'] = grauInstrucao.nome

    return jsonify(data)


# --------------------------------------------------------------------------------------------------#

@app.route('/grau-instrucao/add', methods=['POST'])
@jwt_required
@resource('grauInstrucao-add')
def grauInstrucaoAdd():
    data = request.get_json()
    validator = GrauInstrucaoValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    grauInstrucao = GrauInstrucao(
        nome=data['nome']
    )

    db.session.add(grauInstrucao)

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_CREATED.format("Grau Instrução"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})


# --------------------------------------------------------------------------------------------------#

@app.route('/grau-instrucao/edit/<grau_instrucao_id>', methods=['PUT'])
@jwt_required
@resource('grauInstrucao-edit')
def grauInstrucaoEdit(grau_instrucao_id):
    grauInstrucao = GrauInstrucao.query.get(grau_instrucao_id)

    if not grauInstrucao:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(grau_instrucao_id), 'error': True})

    data = request.get_json()
    validator = GrauInstrucaoValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    grauInstrucao.nome = data['nome']

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_UPDATED.format("Grau Instrução"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})


# --------------------------------------------------------------------------------------------------#

@app.route('/grau-instrucao/delete/<grau_instrucao_id>', methods=['DELETE'])
@jwt_required
@resource('grauInstrucao-delete')
def grauInstrucaoDelete(grau_instrucao_id):
    grauInstrucao = GrauInstrucao.query.get(grau_instrucao_id)

    if not grauInstrucao:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(grau_instrucao_id), 'error': True})

    db.session.delete(grauInstrucao)

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_DELETED.format("Grau Instrução"), 'error': False})
    except exc.IntegrityError:
        return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})
