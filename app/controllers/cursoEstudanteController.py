from app import app, db, Messages
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import exc
from . import resource
from app import CursoEstudante
from app import CursoEstudanteValidator


# --------------------------------------------------------------------------------------------------#

@app.route('/curso-estudante/all', methods=['GET'])
@jwt_required
@resource('cursoEstudantes-all')
def cursoEstudanteAll():
    page = request.args.get('page', 1, type=int)
    idFilter = request.args.get('id', None)
    nomeFilter = request.args.get('nome', None)
    rowsPerPage = app.config['ROWS_PER_PAGE']

    query = CursoEstudante.query.order_by(CursoEstudante.nome)

    if (idFilter != None):
        query = query.filter_by(id=idFilter)

    if (nomeFilter != None):
        query = query.filter( \
            CursoEstudante.nome.ilike("%%{}%%".format(nomeFilter)) \
            )

    pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
    cursoEstudantes = pagination.items
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

    for cursoEstudante in cursoEstudantes:
        data = {}
        data['id'] = cursoEstudante.id
        data['nome'] = cursoEstudante.nome

        output['itens'].append(data)

    return jsonify(output)


# --------------------------------------------------------------------------------------------------#

@app.route('/curso-estudante/view/<curso_estudante_id>', methods=['GET'])
@jwt_required
@resource('cursoEstudante-view')
def cursoEstudanteView(curso_estudante_id):
    cursoEstudante = CursoEstudante.query.get(curso_estudante_id)

    if not cursoEstudante:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(curso_estudante_id), 'error': True})

    data = {'error': False}
    data['id'] = cursoEstudante.id
    data['nome'] = cursoEstudante.nome

    return jsonify(data)


# --------------------------------------------------------------------------------------------------#

@app.route('/curso-estudante/add', methods=['POST'])
@jwt_required
@resource('cursoEstudante-add')
def cursoEstudanteAdd():
    data = request.get_json()
    validator = CursoEstudanteValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    cursoEstudante = CursoEstudante(
        nome=data['nome']
    )

    db.session.add(cursoEstudante)

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_CREATED.format("CursoEstudante"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})


# --------------------------------------------------------------------------------------------------#

@app.route('/curso-estudante/edit/<curso_estudante_id>', methods=['PUT'])
@jwt_required
@resource('cursoEstudante-edit')
def cursoEstudanteEdit(curso_estudante_id):
    cursoEstudante = CursoEstudante.query.get(curso_estudante_id)

    if not cursoEstudante:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(curso_estudante_id), 'error': True})

    data = request.get_json()
    validator = CursoEstudanteValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    cursoEstudante.nome = data['nome']

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_UPDATED.format("CursoEstudante"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})


# --------------------------------------------------------------------------------------------------#

@app.route('/curso-estudante/delete/<curso_estudante_id>', methods=['DELETE'])
@jwt_required
@resource('cursoEstudante-delete')
def cursoEstudanteDelete(curso_estudante_id):
    cursoEstudante = CursoEstudante.query.get(curso_estudante_id)

    if not cursoEstudante:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(curso_estudante_id), 'error': True})

    db.session.delete(cursoEstudante)

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_DELETED.format("CursoEstudante"), 'error': False})
    except exc.IntegrityError:
        return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})
