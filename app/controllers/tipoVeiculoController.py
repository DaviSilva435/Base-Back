from app import app, db, Messages
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import exc
from . import resource
from app import TipoVeiculo
from app import TipoVeiculoValidator


# --------------------------------------------------------------------------------------------------#

@app.route('/tipo-veiculo/all', methods=['GET'])
@jwt_required
@resource('tipoVeiculo-all')
def tipoVeiculoAll():
    page = request.args.get('page', 1, type=int)
    idFilter = request.args.get('id', None)
    nomeFilter = request.args.get('nome', None)
    rowsPerPage = app.config['ROWS_PER_PAGE']

    query = TipoVeiculo.query.order_by(TipoVeiculo.nome)

    if (idFilter != None):
        query = query.filter_by(id=idFilter)

    if (nomeFilter != None):
        query = query.filter( \
            TipoVeiculo.nome.ilike("%%{}%%".format(nomeFilter)) \
            )

    pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
    tipoVeiculos = pagination.items
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

    for tipoVeiculo in tipoVeiculos:
        data = {}
        data['id'] = tipoVeiculo.id
        data['nome'] = tipoVeiculo.nome

        output['itens'].append(data)

    return jsonify(output)


# --------------------------------------------------------------------------------------------------#

@app.route('/tipo-veiculo/view/<tipo_veiculo_id>', methods=['GET'])
@jwt_required
@resource('tipoVeiculo-view')
def tipoVeiculoView(tipo_veiculo_id):
    tipoVeiculo = TipoVeiculo.query.get(tipo_veiculo_id)

    if not tipoVeiculo:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(tipo_veiculo_id), 'error': True})

    data = {'error': False}
    data['id'] = tipoVeiculo.id
    data['nome'] = tipoVeiculo.nome

    return jsonify(data)


# --------------------------------------------------------------------------------------------------#

@app.route('/tipo-veiculo/add', methods=['POST'])
@jwt_required
@resource('tipoVeiculo-add')
def tipoVeiculoAdd():
    data = request.get_json()
    validator = TipoVeiculoValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    tipoVeiculo = TipoVeiculo(
        nome=data['nome']
    )

    db.session.add(tipoVeiculo)

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_CREATED.format("Tipo Veiculo"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})


# --------------------------------------------------------------------------------------------------#

@app.route('/tipo-veiculo/edit/<tipo_veiculo_id>', methods=['PUT'])
@jwt_required
@resource('tipoVeiculo-edit')
def tipoVeiculoEdit(tipo_veiculo_id):
    tipoVeiculo = TipoVeiculo.query.get(tipo_veiculo_id)

    if not tipoVeiculo:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(tipo_veiculo_id), 'error': True})

    data = request.get_json()
    validator = TipoVeiculoValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    tipoVeiculo.nome = data['nome']

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_UPDATED.format("Tipo Veiculo"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})


# --------------------------------------------------------------------------------------------------#

@app.route('/tipo-veiculo/delete/<tipo_veiculo_id>', methods=['DELETE'])
@jwt_required
@resource('tipoVeiculo-delete')
def tipoVeiculoDelete(tipo_veiculo_id):
    tipoVeiculo = TipoVeiculo.query.get(tipo_veiculo_id)

    if not tipoVeiculo:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(tipo_veiculo_id), 'error': True})

    db.session.delete(tipoVeiculo)

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_DELETED.format("Tipo Veiculo"), 'error': False})
    except exc.IntegrityError:
        return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})
