from app import app, db, Messages
from flask import request, jsonify
from flask_jwt_extended import  jwt_required
from sqlalchemy import exc
from . import resource
from app import Conhecimento
from app import ConhecimentoValidator
from app import fieldsFormatter

#--------------------------------------------------------------------------------------------------------#

@app.route('/conhecimento/all', methods=['GET'])
@jwt_required
@resource('conhecimento-all')
def conhecimentoAll():

    page = request.args.get('page',1,type=int)
    idFilter = request.args.get('id',None)
    nomeFilter = request.args.get('nome',None)
    tipoConhecimentoIdFilter = request.args.get('tipo_conhecimento_id',None)
    rowsPerPage = app.config['ROWS_PER_PAGE']

    query = Conhecimento.query.order_by(Conhecimento.tipo_conhecimento_id)

    if (idFilter != None):
        query = query.filter_by(id=idFilter)

    if (nomeFilter != None):
        query = query.filter( \
            Conhecimento.nome.ilike("%%{}%%".format(nomeFilter)) \
            )

    if(tipoConhecimentoIdFilter != None):
        query = query.filter(\
            Conhecimento.tipo_conhecimento_id == tipoConhecimentoIdFilter \
        )

    pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
    conhecimentos = pagination.items
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

    for conhecimento in conhecimentos:
        data = {}
        data['id'] = conhecimento.id
        data['nome'] = conhecimento.nome
        data['tipo_conhecimento_id'] = conhecimento.tipo_conhecimento_id

        output['itens'].append(data)

    return jsonify(output)


# --------------------------------------------------------------------------------------------------#

@app.route('/conhecimento/view/<conhecimento_id>', methods=['GET'])
@jwt_required
@resource('conhecimento-view')
def conhecimentoView(conhecimento_id):

    conhecimento = Conhecimento.query.get(conhecimento_id)

    if not conhecimento:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(conhecimento_id), 'error': True})

    data = {'error': False}
    data['id'] = conhecimento.id
    data['nome'] = conhecimento.nome
    data['tipo_conhecimento_id'] = conhecimento.tipo_conhecimento_id

    return jsonify(data)


# --------------------------------------------------------------------------------------------------#

@app.route('/conhecimento/add', methods=['POST'])
@jwt_required
@resource('conhecimento-add')
def conhecimentoAdd():
    data = request.get_json()
    validator = ConhecimentoValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    conhecimento = Conhecimento(
        nome=data['nome'],
        tipo_conhecimento_id=data['tipo_conhecimento_id']
    )

    db.session.add(conhecimento)

    try:
        db.session.commit()
        return jsonify(
            {'message': Messages.REGISTER_SUCCESS_CREATED.format("Conhecimento"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})


# --------------------------------------------------------------------------------------------------#

@app.route('/conhecimento/edit/<conhecimento_id>', methods=['PUT'])
@jwt_required
@resource('conhecimento-edit')
def conhecimentoEdit(conhecimento_id):
    conhecimento = Conhecimento.query.get(conhecimento_id)

    if not conhecimento:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(conhecimento_id),
                        'error': True})

    data = request.get_json()
    validator = ConhecimentoValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    conhecimento.nome = data['nome'],
    conhecimento.tipo_conhecimento_id = data['tipo_conhecimento_id']

    try:
        db.session.commit()
        return jsonify(
            {'message': Messages.REGISTER_SUCCESS_UPDATED.format("Conhecimento"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})


# --------------------------------------------------------------------------------------------------#

@app.route('/conhecimento/delete/<conhecimento_id>', methods=['DELETE'])
@jwt_required
@resource('conhecimento-delete')
def conhecimentoDelete(conhecimento_id):
    conhecimento = Conhecimento.query.get(conhecimento_id)

    if not conhecimento:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(conhecimento_id),
                        'error': True})

    db.session.delete(conhecimento)

    try:
        db.session.commit()
        return jsonify(
            {'message': Messages.REGISTER_SUCCESS_DELETED.format("Conhecimento"), 'error': False})
    except exc.IntegrityError:
        return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})
