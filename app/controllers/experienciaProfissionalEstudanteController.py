from app import app, db, Messages
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import exc
from . import resource
from app import ExperienciaProfissionalEstudante
from app import ExperienciaProfissionalEstudanteValidator
from app import fieldsFormatter


# --------------------------------------------------------------------------------------------------#

@app.route('/experiencia-profissional-estudante/all', methods=['GET'])
@jwt_required
@resource('experienciaProfissionalEstudante-all')
def experienciaProfissionalEstudanteAll():
    page = request.args.get('page', 1, type=int)
    cboIdFilter = request.args.get('cbo_id', None)
    estudanteIdFilter = request.args.get('estudante_id', None)
    duracaoFilter = request.args.get('duracao', None)
    rowsPerPage = app.config['ROWS_PER_PAGE']

    query = ExperienciaProfissionalEstudante.query.order_by(ExperienciaProfissionalEstudante.estudante_id)

    if (cboIdFilter != None):
        query = query.filter( \
            ExperienciaProfissionalEstudante.cbo_id == cboIdFilter \
            )

    if (estudanteIdFilter != None):
        query = query.filter( \
            ExperienciaProfissionalEstudante.estudante_id == estudanteIdFilter \
            )
    if (duracaoFilter != None):
        query = query.filter( \
            ExperienciaProfissionalEstudante.duracao == duracaoFilter \
            )


    pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
    experienciaProfissionalEstudantes = pagination.items
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

    for experienciaProfissionalEstudante in experienciaProfissionalEstudantes:
        data = {}
        data['estudante_id'] = experienciaProfissionalEstudante.estudante_id
        data['cbo_id'] = experienciaProfissionalEstudante.cbo_id
        data['duracao'] = experienciaProfissionalEstudante.duracao

        output['itens'].append(data)

    return jsonify(output)


# --------------------------------------------------------------------------------------------------#

@app.route('/experiencia-profissional-estudante/view/<estudante_id>/<cbo_id>', methods=['GET'])
@jwt_required
@resource('experienciaProfissionalEstudante-view')
def experienciaProfissionalEstudanteView(estudante_id, cbo_id):
    experienciaProfissionalEstudante = ExperienciaProfissionalEstudante.query.filter(ExperienciaProfissionalEstudante.cbo_id == cbo_id, \
                                           ExperienciaProfissionalEstudante.estudante_id == estudante_id).first()

    if not experienciaProfissionalEstudante:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(estudante_id + ", " + cbo_id), 'error': True})

    data = {'error': False}
    data['duracao'] = experienciaProfissionalEstudante.duracao
    data['estudante_id'] = experienciaProfissionalEstudante.estudante_id
    data['cbo_id'] = experienciaProfissionalEstudante.cbo_id

    return jsonify(data)


# --------------------------------------------------------------------------------------------------#

@app.route('/experiencia-profissional-estudante/add', methods=['POST'])
@jwt_required
@resource('experienciaProfissionalEstudante-add')
def experienciaProfissionalEstudanteAdd():
    data = request.get_json()
    validator = ExperienciaProfissionalEstudanteValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    experienciaProfissionalEstudante = ExperienciaProfissionalEstudante(
        duracao=data['duracao'],
        estudante_id=data['estudante_id'],
        cbo_id=data['cbo_id']
    )

    db.session.add(experienciaProfissionalEstudante)

    try:
        db.session.commit()
        return jsonify(
            {'message': Messages.REGISTER_SUCCESS_CREATED.format("Experiencia Profissional de Estudante"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})


# --------------------------------------------------------------------------------------------------#

@app.route('/experiencia-profissional-estudante/edit/<estudante_id>/<cbo_id>', methods=['PUT'])
@jwt_required
@resource('experienciaProfissionalEstudante-edit')
def experienciaProfissionalEstudanteEdit(estudante_id, cbo_id):
    experienciaProfissionalEstudante = ExperienciaProfissionalEstudante.query.filter(ExperienciaProfissionalEstudante.estudante_id == estudante_id, \
                                           ExperienciaProfissionalEstudante.cbo_id == cbo_id).first()

    if not experienciaProfissionalEstudante:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(estudante_id + "/" + cbo_id),
                        'error': True})

    data = request.get_json()
    validator = ExperienciaProfissionalEstudanteValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    experienciaProfissionalEstudante.duracao = data['duracao'],
    experienciaProfissionalEstudante.estudante_id = data['estudante_id'],
    experienciaProfissionalEstudante.cbo_id = data['cbo_id']

    try:
        db.session.commit()
        return jsonify(
            {'message': Messages.REGISTER_SUCCESS_UPDATED.format("Experiencia Profissional de Estudante"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})


# --------------------------------------------------------------------------------------------------#

@app.route('/experiencia-profissional-estudante/delete/<estudante_id>/<cbo_id>', methods=['DELETE'])
@jwt_required
@resource('experienciaProfissionalEstudante-delete')
def experienciaProfissionalEstudanteDelete(estudante_id, cbo_id):
    experienciaProfissionalEstudante = ExperienciaProfissionalEstudante.query.filter(ExperienciaProfissionalEstudante.estudante_id == estudante_id, \
                                           ExperienciaProfissionalEstudante.cbo_id == cbo_id).first()

    if not experienciaProfissionalEstudante:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(estudante_id + "/" + cbo_id),
                        'error': True})

    db.session.delete(experienciaProfissionalEstudante)

    try:
        db.session.commit()
        return jsonify(
            {'message': Messages.REGISTER_SUCCESS_DELETED.format("Experiencia Profissional de Estudante"), 'error': False})
    except exc.IntegrityError:
        return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})
