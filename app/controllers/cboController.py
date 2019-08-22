from app import app, db, Messages
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import exc
from . import resource
from app import Cbo
from app import CboValidator


# --------------------------------------------------------------------------------------------------#

@app.route('/cbo/all', methods=['GET'])
@jwt_required
@resource('cbo-all')
def cboAll():
    page = request.args.get('page', 1, type=int)
    idFilter = request.args.get('id', None)
    nomeFilter = request.args.get('nome', None)
    codigoFilter = request.args.get('codigo', None)
    rowsPerPage = app.config['ROWS_PER_PAGE']

    query = Cbo.query.order_by(Cbo.nome)

    if (idFilter != None):
        query = query.filter_by(id=idFilter)

    if (nomeFilter != None):
        query = query.filter( \
            Cbo.nome.ilike("%%{}%%".format(nomeFilter)) \
            )

    if (codigoFilter != None):
        query = query.filter( \
            Cbo.codigo.ilike("%%{}%%".format(codigoFilter)) \
            )

    pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
    cbos = pagination.items
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

    for cbo in cbos:
        data = {}
        data['id'] = cbo.id
        data['nome'] = cbo.nome
        data['codigo'] = cbo.codigo

        output['itens'].append(data)

    return jsonify(output)


# --------------------------------------------------------------------------------------------------#

@app.route('/cbo/view/<cbo_id>', methods=['GET'])
@jwt_required
@resource('cbo-view')
def cboView(cbo_id):
    cbo = Cbo.query.get(cbo_id)

    if not cbo:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(cbo_id), 'error': True})

    data = {'error': False}
    data['id'] = cbo.id
    data['nome'] = cbo.nome

    return jsonify(data)


# --------------------------------------------------------------------------------------------------#

@app.route('/cbo/add', methods=['POST'])
@jwt_required
@resource('cbo-add')
def cboAdd():
    data = request.get_json()
    validator = CboValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    cbo = Cbo(
        nome=data['nome'],
        codigo=data['codigo']
    )

    db.session.add(cbo)

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_CREATED.format("Cbo"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})


# --------------------------------------------------------------------------------------------------#

@app.route('/cbo/edit/<cbo_id>', methods=['PUT'])
@jwt_required
@resource('cbo-edit')
def cboEdit(cbo_id):
    cbo = Cbo.query.get(cbo_id)

    if not cbo:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(cbo_id), 'error': True})

    data = request.get_json()
    validator = CboValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    cbo.nome = data['nome'],
    cbo.codigo = data['codigo']

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_UPDATED.format("Cbo"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})


# --------------------------------------------------------------------------------------------------#

@app.route('/cbo/delete/<cbo_id>', methods=['DELETE'])
@jwt_required
@resource('cbo-delete')
def cboDelete(cbo_id):
    cbo = Cbo.query.get(cbo_id)

    if not cbo:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(cbo_id), 'error': True})

    db.session.delete(cbo)

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_DELETED.format("Cbo"), 'error': False})
    except exc.IntegrityError:
        return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})
