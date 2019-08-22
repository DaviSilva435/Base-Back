from app import app, db, Messages
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import exc
from . import resource
from app import TipoConhecimento
from app import TipoConhecimentoValidator


# --------------------------------------------------------------------------------------------------#

@app.route('/tipo-conhecimento/all', methods=['GET'])
@jwt_required
@resource('tipoConhecimento-all')
def tipoConhecimentoAll():
    page = request.args.get('page', 1, type=int)
    idFilter = request.args.get('id', None)
    nomeFilter = request.args.get('nome', None)
    rowsPerPage = app.config['ROWS_PER_PAGE']

    query = TipoConhecimento.query.order_by(TipoConhecimento.nome)

    if (idFilter != None):
        query = query.filter_by(id=idFilter)

    if (nomeFilter != None):
        query = query.filter( \
            TipoConhecimento.nome.ilike("%%{}%%".format(nomeFilter)) \
            )

    pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
    tipoConhecimentos = pagination.items
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

    for tipoConhecimento in tipoConhecimentos:
        data = {}
        data['id'] = tipoConhecimento.id
        data['nome'] = tipoConhecimento.nome

        output['itens'].append(data)

    return jsonify(output)


# --------------------------------------------------------------------------------------------------#

@app.route('/tipo-conhecimento/view/<tipo_conhecimento_id>', methods=['GET'])
@jwt_required
@resource('tipoConhecimento-view')
def tipoConhecimentoView(tipo_conhecimento_id):
    tipoConhecimento = TipoConhecimento.query.get(tipo_conhecimento_id)

    if not tipoConhecimento:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(tipo_conhecimento_id), 'error': True})

    data = {'error': False}
    data['id'] = tipoConhecimento.id
    data['nome'] = tipoConhecimento.nome

    return jsonify(data)


# --------------------------------------------------------------------------------------------------#

@app.route('/tipo-conhecimento/add', methods=['POST'])
@jwt_required
@resource('tipoConhecimento-add')
def tipoConhecimentoAdd():
    data = request.get_json()
    validator = TipoConhecimentoValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    tipoConhecimento = TipoConhecimento(
        nome=data['nome']
    )

    db.session.add(tipoConhecimento)

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_CREATED.format("TipoConhecimento"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})


# --------------------------------------------------------------------------------------------------#

@app.route('/tipo-conhecimento/edit/<tipo_conhecimento_id>', methods=['PUT'])
@jwt_required
@resource('tipoConhecimento-edit')
def tipoConhecimentoEdit(tipo_conhecimento_id):
    tipoConhecimento = TipoConhecimento.query.get(tipo_conhecimento_id)

    if not tipoConhecimento:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(tipo_conhecimento_id), 'error': True})

    data = request.get_json()
    validator = TipoConhecimentoValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    tipoConhecimento.nome = data['nome']

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_UPDATED.format("TipoConhecimento"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})


# --------------------------------------------------------------------------------------------------#

@app.route('/tipo-conhecimento/delete/<tipo_conhecimento_id>', methods=['DELETE'])
@jwt_required
@resource('tipoConhecimento-delete')
def tipoConhecimentoDelete(tipo_conhecimento_id):
    tipoConhecimento = TipoConhecimento.query.get(tipo_conhecimento_id)

    if not tipoConhecimento:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(tipo_conhecimento_id), 'error': True})

    db.session.delete(tipoConhecimento)

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_DELETED.format("TipoConhecimento"), 'error': False})
    except exc.IntegrityError:
        return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})