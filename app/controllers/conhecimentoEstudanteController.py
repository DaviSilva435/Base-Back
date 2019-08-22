from app import app, db, Messages
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import exc
from . import resource
from app import ConhecimentoEstudante
from app import ConhecimentoEstudanteValidator
from app import fieldsFormatter


# --------------------------------------------------------------------------------------------------#

@app.route('/conhecimento-estudante/all', methods=['GET'])
@jwt_required
@resource('conhecimentoEstudante-all')
def conhecimentoEstudanteAll():
    page = request.args.get('page', 1, type=int)
    conhecimentoIdFilter = request.args.get('conhecimento_id', None)
    estudanteIdFilter = request.args.get('estudante_id', None)
    valorFilter = request.args.get('valor', None)
    rowsPerPage = app.config['ROWS_PER_PAGE']

    query = ConhecimentoEstudante.query.order_by(ConhecimentoEstudante.estudante_id)

    if (conhecimentoIdFilter != None):
        query = query.filter( \
            ConhecimentoEstudante.conhecimento_id == conhecimentoIdFilter \
            )

    if (estudanteIdFilter != None):
        query = query.filter( \
            ConhecimentoEstudante.estudante_id == estudanteIdFilter \
            )
    if (valorFilter != None):
        query = query.filter( \
            ConhecimentoEstudante.valor == valorFilter \
            )


    pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
    conhecimentoEstudantes = pagination.items
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

    for conhecimentoEstudante in conhecimentoEstudantes:
        data = {}
        data['estudante_id'] = conhecimentoEstudante.estudante_id
        data['conhecimento_id'] = conhecimentoEstudante.conhecimento_id
        data['valor'] = conhecimentoEstudante.valor

        output['itens'].append(data)

    return jsonify(output)


# --------------------------------------------------------------------------------------------------#

@app.route('/conhecimento-estudante/view/<estudante_id>/<conhecimento_id>', methods=['GET'])
@jwt_required
@resource('conhecimentoEstudante-view')
def conhecimentoEstudanteView(estudante_id, conhecimento_id):
    conhecimentoEstudante = ConhecimentoEstudante.query.filter(ConhecimentoEstudante.conhecimento_id == conhecimento_id, \
                                           ConhecimentoEstudante.estudante_id == estudante_id).first()

    if not conhecimentoEstudante:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(estudante_id + ", " + conhecimento_id), 'error': True})

    data = {'error': False}
    data['valor'] = conhecimentoEstudante.valor
    data['estudante_id'] = conhecimentoEstudante.estudante_id
    data['conhecimento_id'] = conhecimentoEstudante.conhecimento_id

    return jsonify(data)


# --------------------------------------------------------------------------------------------------#

@app.route('/conhecimento-estudante/add', methods=['POST'])
@jwt_required
@resource('conhecimentoEstudante-add')
def conhecimentoEstudanteAdd():
    data = request.get_json()
    validator = ConhecimentoEstudanteValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    conhecimentoEstudante = ConhecimentoEstudante(
        valor=data['valor'],
        estudante_id=data['estudante_id'],
        conhecimento_id=data['conhecimento_id']
    )

    db.session.add(conhecimentoEstudante)

    try:
        db.session.commit()
        return jsonify(
            {'message': Messages.REGISTER_SUCCESS_CREATED.format("Conhecimentos do Estudante"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})


# --------------------------------------------------------------------------------------------------#

@app.route('/conhecimento-estudante/edit/<estudante_id>/<conhecimento_id>', methods=['PUT'])
@jwt_required
@resource('conhecimentoEstudante-edit')
def conhecimentoEstudanteEdit(estudante_id, conhecimento_id):
    conhecimentoEstudante = ConhecimentoEstudante.query.filter(ConhecimentoEstudante.estudante_id == estudante_id, \
                                           ConhecimentoEstudante.conhecimento_id == conhecimento_id).first()

    if not conhecimentoEstudante:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(estudante_id + "/" + conhecimento_id),
                        'error': True})

    data = request.get_json()
    validator = ConhecimentoEstudanteValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    conhecimentoEstudante.valor = data['valor']
    conhecimentoEstudante.estudante_id = data['estudante_id']
    conhecimentoEstudante.conhecimento_id = data['conhecimento_id']

    try:
        db.session.commit()
        return jsonify(
            {'message': Messages.REGISTER_SUCCESS_UPDATED.format("Conhecimentos do Estudante"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})


# --------------------------------------------------------------------------------------------------#

@app.route('/conhecimento-estudante/delete/<estudante_id>/<conhecimento_id>', methods=['DELETE'])
@jwt_required
@resource('conhecimentoEstudante-delete')
def conhecimentoEstudanteDelete(estudante_id, conhecimento_id):
    conhecimentoEstudante = ConhecimentoEstudante.query.filter(ConhecimentoEstudante.estudante_id == estudante_id, \
                                           ConhecimentoEstudante.conhecimento_id == conhecimento_id).first()

    if not conhecimentoEstudante:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(estudante_id + "/" + conhecimento_id),
                        'error': True})

    db.session.delete(conhecimentoEstudante)

    try:
        db.session.commit()
        return jsonify(
            {'message': Messages.REGISTER_SUCCESS_DELETED.format("Conhecimentos do Estudante"), 'error': False})
    except exc.IntegrityError:
        return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})
