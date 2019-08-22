from app import app, db, Messages
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import exc
from . import resource
from app import CursoAdicionalEstudante
from app import CursoAdicionalEstudanteValidator
from app import fieldsFormatter


# --------------------------------------------------------------------------------------------------#

@app.route('/curso-adicional-estudante/all', methods=['GET'])
@jwt_required
@resource('cursoAdicionalEstudante-all')
def cursoAdicionalEstudanteAll():
    page = request.args.get('page', 1, type=int)
    cursoIdFilter = request.args.get('curso_id', None)
    estudanteIdFilter = request.args.get('estudante_id', None)
    cargaHorariaFilter = request.args.get('carga_horaria', None)
    rowsPerPage = app.config['ROWS_PER_PAGE']

    query = CursoAdicionalEstudante.query.order_by(CursoAdicionalEstudante.estudante_id)

    if (cursoIdFilter != None):
        query = query.filter( \
            CursoAdicionalEstudante.curso_id == cursoIdFilter \
            )
    if (estudanteIdFilter != None):
        query = query.filter( \
            CursoAdicionalEstudante.estudante_id == estudanteIdFilter \
            )
    if (cargaHorariaFilter != None):
        query = query.filter( \
            CursoAdicionalEstudante.carga_horaria == cargaHorariaFilter \
            )

    pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
    cursoAdicionalEstudantes = pagination.items
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

    for cursoAdicionalEstudante in cursoAdicionalEstudantes:
        data = {}
        data['carga_horaria'] = cursoAdicionalEstudante.carga_horaria
        data['curso_id'] = cursoAdicionalEstudante.curso_id
        data['estudante_id'] = cursoAdicionalEstudante.estudante_id

        output['itens'].append(data)

    return jsonify(output)


# --------------------------------------------------------------------------------------------------#

@app.route('/curso-adicional-estudante/view/<curso_id>/<estudante_id>', methods=['GET'])
@jwt_required
@resource('cursoAdicionalEstudante-view')
def cursoAdicionalEstudanteView(curso_id, estudante_id):
    cursoAdicionalEstudante = CursoAdicionalEstudante.query.filter(CursoAdicionalEstudante.curso_id == curso_id, \
                                           CursoAdicionalEstudante.estudante_id == estudante_id).first()

    if not cursoAdicionalEstudante:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(estudante_id), 'error': True})

    data = {'error': False}
    data['carga_horaria'] = cursoAdicionalEstudante.carga_horaria
    data['curso_id'] = cursoAdicionalEstudante.curso_id
    data['estudante_id'] = cursoAdicionalEstudante.estudante_id

    return jsonify(data)


# --------------------------------------------------------------------------------------------------#

@app.route('/curso-adicional-estudante/add', methods=['POST'])
@jwt_required
@resource('cursoAdicionalEstudante-add')
def cursoAdicionalEstudanteAdd():
    data = request.get_json()
    validator = CursoAdicionalEstudanteValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    cursoAdicionalEstudante = CursoAdicionalEstudante(
        curso_id=data['curso_id'],
        estudante_id=data['estudante_id'],
        carga_horaria=data['carga_horaria']
    )

    db.session.add(cursoAdicionalEstudante)

    try:
        db.session.commit()
        return jsonify(
            {'message': Messages.REGISTER_SUCCESS_CREATED.format("Curso Adicional do Estudante"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})


# --------------------------------------------------------------------------------------------------#

@app.route('/curso-adicional-estudante/edit/<curso_id>/<estudante_id>', methods=['PUT'])
@jwt_required
@resource('cursoAdicionalEstudante-edit')
def cursoAdicionalEstudanteEdit(curso_id, estudante_id):
    cursoAdicionalEstudante = CursoAdicionalEstudante.query.filter(CursoAdicionalEstudante.curso_id == curso_id, \
                                           CursoAdicionalEstudante.estudante_id == estudante_id).first()

    if not cursoAdicionalEstudante:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(curso_id + "/" + estudante_id),
                        'error': True})

    data = request.get_json()
    validator = CursoAdicionalEstudanteValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    cursoAdicionalEstudante.carga_horaria = data['carga_horaria']
    cursoAdicionalEstudante.curso_id = data['curso_id']
    cursoAdicionalEstudante.estudante_id = data['estudante_id']

    try:
        db.session.commit()
        return jsonify(
            {'message': Messages.REGISTER_SUCCESS_UPDATED.format("Curso Adicional do Estudante"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})


# --------------------------------------------------------------------------------------------------#

@app.route('/curso-adicional-estudante/delete/<curso_id>/<estudante_id>', methods=['DELETE'])
@jwt_required
@resource('cursoAdicionalEstudante-delete')
def cursoAdicionalEstudanteDelete(curso_id, estudante_id):
    cursoAdicionalEstudante = CursoAdicionalEstudante.query.filter(CursoAdicionalEstudante.curso_id == curso_id, \
                                           CursoAdicionalEstudante.estudante_id == estudante_id).first()

    if not cursoAdicionalEstudante:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(curso_id + "/" + estudante_id),
                        'error': True})

    db.session.delete(cursoAdicionalEstudante)

    try:
        db.session.commit()
        return jsonify(
            {'message': Messages.REGISTER_SUCCESS_DELETED.format("Curso Adicional do Estudante"), 'error': False})
    except exc.IntegrityError:
        return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})
