from app import app, db, Messages
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import exc
from . import resource
from app import Role
from app import RolesValidator


#--------------------------------------------------------------------------------------------------#

@app.route('/roles/all', methods=['GET'])
@jwt_required
@resource('roles-all')
def rolesAll():

    page = request.args.get('page', 1, type=int)
    nameFilter = request.args.get('nome', None)
    idFilter = request.args.get('id', None)
    rowsPerPage = app.config['ROWS_PER_PAGE']

    query = Role.query.order_by(Role.name)

    if (nameFilter != None):
        query = query.filter( \
            Role.name.ilike("%%{}%%".format(nameFilter)) \
            )

    if (idFilter != None):
        query = query.filter_by(id = idFilter)


    pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
    roles = pagination.items

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

    for role in roles:
        data = {}
        data['id'] = role.id
        data['nome'] = role.name
        output['itens'].append(data)

    return jsonify(output)

#--------------------------------------------------------------------------------------------------#

@app.route('/roles/view/<role_id>', methods=['GET'])
@jwt_required
@resource('roles-view')
def rolesView(role_id):

    role = Role.query.get(role_id)
    if not role:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(role_id), 'error': True})

    data = {'error': False}
    data['id'] = role.id
    data['nome'] = role.name

    return jsonify(data)

#--------------------------------------------------------------------------------------------------#

@app.route('/roles/add', methods=['POST'])
@jwt_required
@resource('roles-add')
def rolesAdd():

    data = request.get_json()
    validator = RolesValidator(data)
    errors = validator.validate()

    if(errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    role = Role(data['nome'])

    db.session.add(role)

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_CREATED.format("Role"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#

@app.route('/roles/edit/<role_id>', methods = ['PUT'])
@jwt_required
@resource('roles-edit')
def roleEdit(role_id):
    role = Role.query.get(role_id)

    if not role:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(role_id), 'error': True})

    data = request.get_json()
    validator = RolesValidator(data)
    errors = validator.validate()

    if (errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    role.name = data['nome']

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_UPDATED.format("Role"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#

@app.route('/roles/delete/<role_id>', methods = ['DELETE'])
@jwt_required
@resource('roles-delete')
def rolesDelete(role_id):
    role = Role.query.get(role_id)

    if not role:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(role_id), 'error': True})

    db.session.delete(role)

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_DELETED.format("Role"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})


