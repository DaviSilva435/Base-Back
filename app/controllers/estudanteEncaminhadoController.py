from app import app, db, Messages
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import exc
from . import resource
from app import EstudanteEncaminhado
from app import ConvocacaoVaga
from app import Vaga
from app import EstudanteEncaminhadoValidator
from app import fieldsFormatter


# --------------------------------------------------------------------------------------------------#

@app.route('/estudante-encaminhado/all', methods=['GET'])
@jwt_required
@resource('estudanteEncaminhado-all')
def estudanteEncaminhadoAll():
    page = request.args.get('page', 1, type=int)
    convocacaoIdFilter = request.args.get('convocacao_id', None)
    estudanteIdFilter = request.args.get('estudante_id', None)
    contratadoIdFilter = request.args.get('contratado', None)
    rowsPerPage = app.config['ROWS_PER_PAGE']

    query = EstudanteEncaminhado.query.order_by(EstudanteEncaminhado.estudante_id)

    if (convocacaoIdFilter != None):
        query = query.filter( \
            EstudanteEncaminhado.convocacao_id == convocacaoIdFilter \
            )

    if (estudanteIdFilter != None):
        query = query.filter( \
            EstudanteEncaminhado.estudante_id == estudanteIdFilter \
            )
    if (contratadoIdFilter != None):
        query = query.filter(
            EstudanteEncaminhado.contratado.ilike("%{}%".format(contratadoIdFilter))
        )


    pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
    estudanteEncaminhados = pagination.items
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

    for estudanteEncaminhado in estudanteEncaminhados:
        data = {}
        data['estudante_id'] = estudanteEncaminhado.estudante_id
        data['convocacao_id'] = estudanteEncaminhado.convocacao_id
        data['contratado'] = estudanteEncaminhado.contratado

        output['itens'].append(data)

    return jsonify(output)


# --------------------------------------------------------------------------------------------------#

@app.route('/estudante-encaminhado/view/<estudante_id>/<convocacao_id>', methods=['GET'])
@jwt_required
@resource('estudanteEncaminhado-view')
def estudanteEncaminhadoView(estudante_id, convocacao_id):
    estudanteEncaminhado = EstudanteEncaminhado.query.filter(EstudanteEncaminhado.convocacao_id == convocacao_id, \
                                           EstudanteEncaminhado.estudante_id == estudante_id).first()

    if not estudanteEncaminhado:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(estudante_id + ", " + convocacao_id), 'error': True})

    data = {'error': False}
    data['contratado'] = estudanteEncaminhado.contratado
    data['estudante_id'] = estudanteEncaminhado.estudante_id
    data['convocacao_id'] = estudanteEncaminhado.convocacao_id

    return jsonify(data)


# --------------------------------------------------------------------------------------------------#

@app.route('/estudante-encaminhado/add', methods=['POST'])
@jwt_required
@resource('estudanteEncaminhado-add')
def estudanteEncaminhadoAdd():
    data = request.get_json()
    validator = EstudanteEncaminhadoValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200



    if data['contratado']:
        convocacao = ConvocacaoVaga.query.get(data['convocacao_id'])
        vaga = Vaga.query.get(convocacao.id)
        registrados = EstudanteEncaminhado.query.count()
        if registrados >= vaga.quantidade_vagas:
            return jsonify({'message' : "Quantidade de vagas excedida.", 'error':True})

    estudanteEncaminhado = EstudanteEncaminhado(
        estudante_id=data['estudante_id'],
        convocacao_id=data['convocacao_id'],
        contratado=data['contratado']
    )

    db.session.add(estudanteEncaminhado)

    try:
        db.session.commit()
        return jsonify(
            {'message': Messages.REGISTER_SUCCESS_CREATED.format("Estudante Encaminhado"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})


# --------------------------------------------------------------------------------------------------#

@app.route('/estudante-encaminhado/edit/<estudante_id>/<convocacao_id>', methods=['PUT'])
@jwt_required
@resource('estudanteEncaminhado-edit')
def estudanteEncaminhadoEdit(estudante_id, convocacao_id):
    estudanteEncaminhado = EstudanteEncaminhado.query.filter(EstudanteEncaminhado.estudante_id == estudante_id, \
                                           EstudanteEncaminhado.convocacao_id == convocacao_id).first()

    if not estudanteEncaminhado:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(estudante_id + "/" + convocacao_id),
                        'error': True})

    data = request.get_json()
    validator = EstudanteEncaminhadoValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    if data['contratado']:
        convocacao = ConvocacaoVaga.query.get(data['convocacao_id'])
        vaga = Vaga.query.get(convocacao.id)
        registrados = EstudanteEncaminhado.query.count()
        if registrados >= vaga.quantidade_vagas:
            return jsonify({'message': "Quantidade de vagas excedida.", 'error': True})

    estudanteEncaminhado.contratado = data['contratado']
    estudanteEncaminhado.estudante_id = data['estudante_id']
    estudanteEncaminhado.convocacao_id = data['convocacao_id']

    try:
        db.session.commit()
        return jsonify(
            {'message': Messages.REGISTER_SUCCESS_UPDATED.format("Estudante Encaminhado"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})


# --------------------------------------------------------------------------------------------------#

@app.route('/estudante-encaminhado/delete/<estudante_id>/<convocacao_id>', methods=['DELETE'])
@jwt_required
@resource('estudanteEncaminhado-delete')
def estudanteEncaminhadoDelete(estudante_id, convocacao_id):
    estudanteEncaminhado = EstudanteEncaminhado.query.filter(EstudanteEncaminhado.estudante_id == estudante_id, \
                                           EstudanteEncaminhado.convocacao_id == convocacao_id).first()

    if not estudanteEncaminhado:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(estudante_id + "/" + convocacao_id),
                        'error': True})

    db.session.delete(estudanteEncaminhado)

    try:
        db.session.commit()
        return jsonify(
            {'message': Messages.REGISTER_SUCCESS_DELETED.format("Estudante Encaminhado"), 'error': False})
    except exc.IntegrityError:
        return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})
