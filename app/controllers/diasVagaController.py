from app import app, db, Messages
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import exc
from . import resource
from app import DiasVaga
from app import DiasVagaValidator
from app import fieldsFormatter


# --------------------------------------------------------------------------------------------------#

@app.route('/dias-vaga/all', methods=['GET'])
@jwt_required
@resource('diasVaga-all')
def diasVagaAll():
    page = request.args.get('page', 1, type=int)
    idDiaFilter = request.args.get('id_dia', None)
    estudanteIdFilter = request.args.get('vaga_id', None)
    horaInicioFilter = request.args.get('hora_inicio', None)
    horaFimFilter = request.args.get('hora_fim', None)
    rowsPerPage = app.config['ROWS_PER_PAGE']

    query = DiasVaga.query.order_by(DiasVaga.vaga_id)

    if (idDiaFilter != None):
        query = query.filter( \
            DiasVaga.id_dia == idDiaFilter \
        )

    if (estudanteIdFilter != None):
        query = query.filter( \
            DiasVaga.estudante_id == estudanteIdFilter \
        )

    if (horaInicioFilter != None):
        query = query.filter( \
            DiasVaga.hora_inicio.ilike("%%{}%%".format(horaInicioFilter))\
        )

    if (horaFimFilter != None):
        query = query.filter( \
            DiasVaga.hora_fim.ilike("%%{}%%".format(horaFimFilter)) \
        )


    pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
    diasVagas = pagination.items
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

    for diasVaga in diasVagas:
        data = {}
        data['vaga_id'] = diasVaga.vaga_id
        data['id_dia'] = diasVaga.id_dia
        data['hora_inicio'] = ("{}".format(diasVaga.hora_inicio))
        data['hora_fim'] = ("{}".format(diasVaga.hora_fim))

        output['itens'].append(data)

    return jsonify(output)


# --------------------------------------------------------------------------------------------------#

@app.route('/dias-vaga/view/<vaga_id>/<id_dia>', methods=['GET'])
@jwt_required
@resource('diasVaga-view')
def diasVagaView(vaga_id, id_dia):
    diasVaga = DiasVaga.query.get([vaga_id, id_dia])

    if not diasVaga:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(vaga_id + ", " + id_dia), 'error': True})

    data = {'error': False}
    data['vaga_id'] = diasVaga.vaga_id
    data['id_dia'] = diasVaga.id_dia
    data['hora_inicio'] = ("{}".format(diasVaga.hora_inicio))
    data['hora_fim'] = ("{}".format(diasVaga.hora_fim))

    return jsonify(data)


# --------------------------------------------------------------------------------------------------#

@app.route('/dias-vaga/add', methods=['POST'])
@jwt_required
@resource('diasVaga-add')
def diasVagaAdd():
    data = request.get_json()
    validator = DiasVagaValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    diasVaga = DiasVaga(
        vaga_id=data['vaga_id'],
        id_dia=data['id_dia'],
        hora_inicio=data['hora_inicio'],
        hora_fim=data['hora_fim']
    )

    db.session.add(diasVaga)
    db.session.commit()

    try:
        db.session.commit()
        return jsonify(
            {'message': Messages.REGISTER_SUCCESS_CREATED.format("Dias Vaga"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})


# --------------------------------------------------------------------------------------------------#

@app.route('/dias-vaga/edit/<vaga_id>/<id_dia>', methods=['PUT'])
@jwt_required
@resource('diasVaga-edit')
def diasVagaEdit(vaga_id, id_dia):
    diasVaga = DiasVaga.query.filter(DiasVaga.vaga_id == vaga_id, \
                                           DiasVaga.id_dia == id_dia).first()

    if not diasVaga:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(vaga_id + "/" + id_dia),
                        'error': True})

    data = request.get_json()
    validator = DiasVagaValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    diasVaga.vaga_id = data['vaga_id']
    diasVaga.id_dia = data['id_dia']
    diasVaga.hora_inicio = data['hora_inicio']
    diasVaga.hora_fim = data['hora_fim']

    try:
        db.session.commit()
        return jsonify(
            {'message': Messages.REGISTER_SUCCESS_UPDATED.format("Dias Vaga"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})


# --------------------------------------------------------------------------------------------------#

@app.route('/dias-vaga/delete/<vaga_id>/<id_dia>', methods=['DELETE'])
@jwt_required
@resource('diasVaga-delete')
def diasVagaDelete(vaga_id, id_dia):
    diasVaga = DiasVaga.query.filter(DiasVaga.vaga_id == vaga_id, \
                                           DiasVaga.id_dia == id_dia).first()

    if not diasVaga:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(vaga_id + "/" + id_dia),
                        'error': True})

    db.session.delete(diasVaga)

    try:
        db.session.commit()
        return jsonify(
            {'message': Messages.REGISTER_SUCCESS_DELETED.format("Dias Vaga"), 'error': False})
    except exc.IntegrityError:
        return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})
