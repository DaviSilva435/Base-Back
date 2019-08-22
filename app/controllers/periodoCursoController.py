from app import app, db, Messages
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import exc
from . import resource
from app import PeriodoCurso
from app import PeriodoCursoValidator


# --------------------------------------------------------------------------------------------------#

@app.route('/periodo-curso/all', methods=['GET'])
@jwt_required
@resource('periodoCursos-all')
def periodoCursoAll():
    page = request.args.get('page', 1, type=int)
    idFilter = request.args.get('id', None)
    nomeFilter = request.args.get('nome', None)
    rowsPerPage = app.config['ROWS_PER_PAGE']

    query = PeriodoCurso.query.order_by(PeriodoCurso.nome)

    if (idFilter != None):
        query = query.filter_by(id=idFilter)

    if (nomeFilter != None):
        query = query.filter( \
            PeriodoCurso.nome.ilike("%%{}%%".format(nomeFilter)) \
            )

    pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
    periodoCursos = pagination.items
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

    for periodoCurso in periodoCursos:
        data = {}
        data['id'] = periodoCurso.id
        data['nome'] = periodoCurso.nome

        output['itens'].append(data)

    return jsonify(output)


# --------------------------------------------------------------------------------------------------#

@app.route('/periodo-curso/view/<periodo_curso_id>', methods=['GET'])
@jwt_required
@resource('periodoCurso-view')
def periodoCursoView(periodo_curso_id):
    periodoCurso = PeriodoCurso.query.get(periodo_curso_id)

    if not periodoCurso:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(periodo_curso_id), 'error': True})

    data = {'error': False}
    data['id'] = periodoCurso.id
    data['nome'] = periodoCurso.nome

    return jsonify(data)


# --------------------------------------------------------------------------------------------------#

@app.route('/periodo-curso/add', methods=['POST'])
@jwt_required
@resource('periodoCurso-add')
def periodoCursoAdd():
    data = request.get_json()
    validator = PeriodoCursoValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    periodoCurso = PeriodoCurso(
        nome=data['nome']
    )

    db.session.add(periodoCurso)

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_CREATED.format("Periodo Curso"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})


# --------------------------------------------------------------------------------------------------#

@app.route('/periodo-curso/edit/<periodo_curso_id>', methods=['PUT'])
@jwt_required
@resource('periodoCurso-edit')
def periodoCursoEdit(periodo_curso_id):
    periodoCurso = PeriodoCurso.query.get(periodo_curso_id)

    if not periodoCurso:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(periodo_curso_id), 'error': True})

    data = request.get_json()
    validator = PeriodoCursoValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    periodoCurso.nome = data['nome']

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_UPDATED.format("Periodo Curso"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})


# --------------------------------------------------------------------------------------------------#

@app.route('/periodo-curso/delete/<periodo_curso_id>', methods=['DELETE'])
@jwt_required
@resource('periodoCurso-delete')
def periodoCursoDelete(periodo_curso_id):
    periodoCurso = PeriodoCurso.query.get(periodo_curso_id)

    if not periodoCurso:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(periodo_curso_id), 'error': True})

    db.session.delete(periodoCurso)

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_DELETED.format("Periodo Curso"), 'error': False})
    except exc.IntegrityError:
        return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})
