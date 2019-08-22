from app import app, db, Messages
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import exc
from . import resource
from app import CategoriaHabilitacao
from app import CategoriaHabilitacaoValidator


# --------------------------------------------------------------------------------------------------#

@app.route('/categoria-habilitacao/all', methods=['GET'])
@jwt_required
@resource('categoriaHabilitacao-all')
def categoriaHabilitacaoAll():
    page = request.args.get('page', 1, type=int)
    idFilter = request.args.get('id', None)
    nomeFilter = request.args.get('nome', None)
    rowsPerPage = app.config['ROWS_PER_PAGE']

    query = CategoriaHabilitacao.query.order_by(CategoriaHabilitacao.nome)

    if (idFilter != None):
        query = query.filter_by(id=idFilter)

    if (nomeFilter != None):
        query = query.filter( \
            CategoriaHabilitacao.nome.ilike("%%{}%%".format(nomeFilter)) \
            )

    pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
    categoriaHabilitacoes = pagination.items
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

    for categoriaHabilitacao in categoriaHabilitacoes:
        data = {}
        data['id'] = categoriaHabilitacao.id
        data['nome'] = categoriaHabilitacao.nome

        output['itens'].append(data)

    return jsonify(output)


# --------------------------------------------------------------------------------------------------#

@app.route('/categoria-habilitacao/view/<categoria_habilitacao_id>', methods=['GET'])
@jwt_required
@resource('categoriaHabilitacao-view')
def categoriaHabilitacaoView(categoria_habilitacao_id):
    categoriaHabilitacao = CategoriaHabilitacao.query.get(categoria_habilitacao_id)

    if not categoriaHabilitacao:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(categoria_habilitacao_id), 'error': True})

    data = {'error': False}
    data['id'] = categoriaHabilitacao.id
    data['nome'] = categoriaHabilitacao.nome

    return jsonify(data)


# --------------------------------------------------------------------------------------------------#

@app.route('/categoria-habilitacao/add', methods=['POST'])
@jwt_required
@resource('categoriaHabilitacao-add')
def categoriaHabilitacaoAdd():
    data = request.get_json()
    validator = CategoriaHabilitacaoValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    categoriaHabilitacao = CategoriaHabilitacao(
        nome=data['nome']
    )

    db.session.add(categoriaHabilitacao)

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_CREATED.format("Categoria Habilitação"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})


# --------------------------------------------------------------------------------------------------#

@app.route('/categoria-habilitacao/edit/<categoria_habilitacao_id>', methods=['PUT'])
@jwt_required
@resource('categoriaHabilitacao-edit')
def categoriaHabilitacaoEdit(categoria_habilitacao_id):
    categoriaHabilitacao = CategoriaHabilitacao.query.get(categoria_habilitacao_id)

    if not categoriaHabilitacao:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(categoria_habilitacao_id), 'error': True})

    data = request.get_json()
    validator = CategoriaHabilitacaoValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    categoriaHabilitacao.nome = data['nome']

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_UPDATED.format("Categoria Habilitação"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})


# --------------------------------------------------------------------------------------------------#

@app.route('/categoria-habilitacao/delete/<categoria_habilitacao_id>', methods=['DELETE'])
@jwt_required
@resource('categoriaHabilitacao-delete')
def categoriaHabilitacaoDelete(categoria_habilitacao_id):
    categoriaHabilitacao = CategoriaHabilitacao.query.get(categoria_habilitacao_id)

    if not categoriaHabilitacao:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(categoria_habilitacao_id), 'error': True})

    db.session.delete(categoriaHabilitacao)

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_DELETED.format("Categoria Habilitação"), 'error': False})
    except exc.IntegrityError:
        return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})
