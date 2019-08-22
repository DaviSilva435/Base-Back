from app import app, db, Messages
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import exc
from . import resource
from app import BeneficioVaga
from app import BeneficioVagaValidator
from app import fieldsFormatter


# --------------------------------------------------------------------------------------------------#

@app.route('/beneficio-vaga/all', methods=['GET'])
@jwt_required
@resource('beneficioVaga-all')
def beneficioVagaAll():
    page = request.args.get('page', 1, type=int)
    beneficioIdFilter = request.args.get('beneficio_id', None)
    vagaIdFilter = request.args.get('vaga_id', None)
    valorFilter = request.args.get('valor', None)
    rowsPerPage = app.config['ROWS_PER_PAGE']

    query = BeneficioVaga.query.order_by(BeneficioVaga.vaga_id)

    if (beneficioIdFilter != None):
        query = query.filter( \
            BeneficioVaga.beneficio_id == beneficioIdFilter \
            )

    if (vagaIdFilter != None):
        query = query.filter( \
            BeneficioVaga.vaga_id == vagaIdFilter \
            )
    if (valorFilter != None):
        query = query.filter( \
            BeneficioVaga.valor == valorFilter \
            )


    pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
    beneficioVagas = pagination.items
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

    for beneficioVaga in beneficioVagas:
        data = {}
        data['vaga_id'] = beneficioVaga.vaga_id
        data['beneficio_id'] = beneficioVaga.beneficio_id
        data['valor'] = beneficioVaga.valor

        output['itens'].append(data)

    return jsonify(output)


# --------------------------------------------------------------------------------------------------#

@app.route('/beneficio-vaga/view/<vaga_id>/<beneficio_id>', methods=['GET'])
@jwt_required
@resource('beneficioVaga-view')
def beneficioVagaView(vaga_id, beneficio_id):
    beneficioVaga = BeneficioVaga.query.filter(BeneficioVaga.beneficio_id == beneficio_id, \
                                           BeneficioVaga.vaga_id == vaga_id).first()

    if not beneficioVaga:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(vaga_id + ", " + beneficio_id), 'error': True})

    data = {'error': False}
    data['valor'] = beneficioVaga.valor
    data['vaga_id'] = beneficioVaga.vaga_id
    data['beneficio_id'] = beneficioVaga.beneficio_id

    return jsonify(data)


# --------------------------------------------------------------------------------------------------#

@app.route('/beneficio-vaga/add', methods=['POST'])
@jwt_required
@resource('beneficioVaga-add')
def beneficioVagaAdd():
    data = request.get_json()
    validator = BeneficioVagaValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    beneficioVaga = BeneficioVaga(
        valor=data['valor'],
        vaga_id=data['vaga_id'],
        beneficio_id=data['beneficio_id']
    )

    db.session.add(beneficioVaga)

    try:
        db.session.commit()
        return jsonify(
            {'message': Messages.REGISTER_SUCCESS_CREATED.format("Beneficio Vaga"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})


# --------------------------------------------------------------------------------------------------#

@app.route('/beneficio-vaga/edit/<vaga_id>/<beneficio_id>', methods=['PUT'])
@jwt_required
@resource('beneficioVaga-edit')
def beneficioVagaEdit(vaga_id, beneficio_id):
    beneficioVaga = BeneficioVaga.query.filter(BeneficioVaga.vaga_id == vaga_id, \
                                           BeneficioVaga.beneficio_id == beneficio_id).first()

    if not beneficioVaga:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(vaga_id + "/" + beneficio_id),
                        'error': True})

    data = request.get_json()
    validator = BeneficioVagaValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    beneficioVaga.valor = data['valor']
    beneficioVaga.vaga_id = data['vaga_id']
    beneficioVaga.beneficio_id = data['beneficio_id']

    try:
        db.session.commit()
        return jsonify(
            {'message': Messages.REGISTER_SUCCESS_UPDATED.format("Beneficio Vaga"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})


# --------------------------------------------------------------------------------------------------#

@app.route('/beneficio-vaga/delete/<vaga_id>/<beneficio_id>', methods=['DELETE'])
@jwt_required
@resource('beneficioVaga-delete')
def beneficioVagaDelete(vaga_id, beneficio_id):
    beneficioVaga = BeneficioVaga.query.filter(BeneficioVaga.vaga_id == vaga_id, \
                                           BeneficioVaga.beneficio_id == beneficio_id).first()

    if not beneficioVaga:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(vaga_id + "/" + beneficio_id),
                        'error': True})

    db.session.delete(beneficioVaga)

    try:
        db.session.commit()
        return jsonify(
            {'message': Messages.REGISTER_SUCCESS_DELETED.format("Beneficio Vaga"), 'error': False})
    except exc.IntegrityError:
        return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})
