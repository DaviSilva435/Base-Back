from app import app, db, Messages
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import exc
from . import resource
from app import EstadoCivil
from app import EstadoCivilValidator

# --------------------------------------------------------------------------------------------------#

@app.route('/estado-civil/all', methods=['GET'])
@jwt_required
@resource('estadoCivil-all')
def estadoCivilAll():
    page = request.args.get('page', 1, type=int)
    idFilter = request.args.get('id', None)
    nomeFilter = request.args.get('nome', None)
    rowsPerPage = app.config['ROWS_PER_PAGE']

    query = EstadoCivil.query.order_by(EstadoCivil.nome)

    if (idFilter != None):
        query = query.filter_by(id=idFilter)

    if (nomeFilter != None):
        query = query.filter( \
            EstadoCivil.nome.ilike("%%{}%%".format(nomeFilter)) \
            )

    pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
    estadosCivis = pagination.items
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

    for estadoCivil in estadosCivis:
        data = {}
        data['id'] = estadoCivil.id
        data['nome'] = estadoCivil.nome

        output['itens'].append(data)

    return jsonify(output)


# --------------------------------------------------------------------------------------------------#

@app.route('/estado-civil/view/<estado_civil_id>', methods=['GET'])
@jwt_required
@resource('estadoCivil-view')
def estadoCivilView(estado_civil_id):
    estadoCivil = EstadoCivil.query.get(estado_civil_id)

    if not estadoCivil:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(estado_civil_id), 'error': True})

    data = {'error': False}
    data['id'] = estadoCivil.id
    data['nome'] = estadoCivil.nome

    return jsonify(data)


# --------------------------------------------------------------------------------------------------#

@app.route('/estado-civil/add', methods=['POST'])
@jwt_required
@resource('estadoCivil-add')
def estadoCivilAdd():
    data = request.get_json()
    validator = EstadoCivilValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    estadoCivil = EstadoCivil(
        nome=data['nome']
    )

    db.session.add(estadoCivil)

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_CREATED.format("Estado Civil"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})


# --------------------------------------------------------------------------------------------------#

@app.route('/estado-civil/edit/<estado_civil_id>', methods=['PUT'])
@jwt_required
@resource('estadoCivil-edit')
def estadoCivilEdit(estado_civil_id):
    estadoCivil = EstadoCivil.query.get(estado_civil_id)

    if not estadoCivil:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(estado_civil_id), 'error': True})

    data = request.get_json()
    validator = EstadoCivilValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    estadoCivil.nome = data['nome']

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_UPDATED.format("Estado Civil"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})


# --------------------------------------------------------------------------------------------------#

@app.route('/estado-civil/delete/<estado_civil_id>', methods=['DELETE'])
@jwt_required
@resource('estadoCivil-delete')
def estadoCivilDelete(estado_civil_id):
    estadoCivil = EstadoCivil.query.get(estado_civil_id)

    if not estadoCivil:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(estado_civil_id), 'error': True})

    db.session.delete(estadoCivil)

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_DELETED.format("Estado Civil"), 'error': False})
    except exc.IntegrityError:
        return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})
