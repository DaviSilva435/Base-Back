from app import app, db, Messages
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import exc
from . import resource
from app import Beneficio
from app import BeneficioValidator

# --------------------------------------------------------------------------------------------------#

@app.route('/beneficio/all', methods=['GET'])
@jwt_required
@resource('beneficios-all')
def beneficioAll():
    page = request.args.get('page', 1, type=int)
    idFilter = request.args.get('id', None)
    nomeFilter = request.args.get('nome', None)
    rowsPerPage = app.config['ROWS_PER_PAGE']

    query = Beneficio.query.order_by(Beneficio.nome)

    if (idFilter != None):
        query = query.filter_by(id=idFilter)

    if (nomeFilter != None):
        query = query.filter( \
            Beneficio.nome.ilike("%%{}%%".format(nomeFilter)) \
            )

    pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
    beneficios = pagination.items
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

    for beneficio in beneficios:
        data = {}
        data['id'] = beneficio.id
        data['nome'] = beneficio.nome

        output['itens'].append(data)

    return jsonify(output)


# --------------------------------------------------------------------------------------------------#

@app.route('/beneficio/view/<beneficio_id>', methods=['GET'])
@jwt_required
@resource('beneficio-view')
def beneficioView(beneficio_id):
    beneficio = Beneficio.query.get(beneficio_id)

    if not beneficio:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(beneficio_id), 'error': True})

    data = {'error': False}
    data['id'] = beneficio.id
    data['nome'] = beneficio.nome

    return jsonify(data)


# --------------------------------------------------------------------------------------------------#

@app.route('/beneficio/add', methods=['POST'])
@jwt_required
@resource('beneficio-add')
def beneficioAdd():
    data = request.get_json()
    validator = BeneficioValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    beneficio = Beneficio(
        nome=data['nome']
    )

    db.session.add(beneficio)

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_CREATED.format("Beneficio"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})


# --------------------------------------------------------------------------------------------------#

@app.route('/beneficio/edit/<beneficio_id>', methods=['PUT'])
@jwt_required
@resource('beneficio-edit')
def beneficioEdit(beneficio_id):
    beneficio = Beneficio.query.get(beneficio_id)

    if not beneficio:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(beneficio_id), 'error': True})

    data = request.get_json()
    validator = BeneficioValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    beneficio.nome = data['nome']

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_UPDATED.format("Beneficio"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})


# --------------------------------------------------------------------------------------------------#

@app.route('/beneficio/delete/<beneficio_id>', methods=['DELETE'])
@jwt_required
@resource('beneficio-delete')
def beneficioDelete(beneficio_id):
    beneficio = Beneficio.query.get(beneficio_id)

    if not beneficio:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(beneficio_id), 'error': True})

    db.session.delete(beneficio)

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_DELETED.format("Beneficio"), 'error': False})
    except exc.IntegrityError:
        return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})
