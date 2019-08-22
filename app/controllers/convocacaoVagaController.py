from app 				import app, db, Messages
from flask 				import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy 		import exc
from . 					import resource
from app import ConvocacaoVaga
from app import ConvocacaoVagaValidator
from app import fieldsFormatter

#--------------------------------------------------------------------------------------------------#

@app.route('/convocacao-vaga/all', methods=['GET'])
@jwt_required
@resource('convocacaoVaga-all')
def convocacaoVagaAll():

    page = request.args.get('page', 1, type=int)
    dataConvocacaoFilter = request.args.get('data_convocacao', None)
    nomeSolicitanteFilter = request.args.get('nome_solicitante', None)
    contatoSolicitanteFilter = request.args.get('contato_solicitante', None)
    dataEntrevistaFilter = request.args.get('data_entrevista', None)

    vagaIdFilter = request.args.get('vaga_id', None)
    contratoEmpresaIdFilter = request.args.get('contrato_empresa_id', None)

    rowsPerPage = app.config['ROWS_PER_PAGE']

    query = ConvocacaoVaga.query.order_by(ConvocacaoVaga.contrato_empresa_id)


    if (vagaIdFilter != None):
        query = query.filter(
            ConvocacaoVaga.vaga_id == vagaIdFilter
            )
    if (contratoEmpresaIdFilter != None):
        query = query.filter(
            ConvocacaoVaga.contrato_empresa_id == contratoEmpresaIdFilter
            )

    if (dataConvocacaoFilter != None):
        query = query.filter(
            ConvocacaoVaga.data_convocacao == dataConvocacaoFilter
            )
    if (dataEntrevistaFilter != None):
        query = query.filter(
            ConvocacaoVaga.data_entrevista == dataEntrevistaFilter
            )

    if (nomeSolicitanteFilter != None):
        query = query.filter( \
            ConvocacaoVaga.nome_solicitante.ilike("%%{}%%".format(nomeSolicitanteFilter)) \
            )
    if (contatoSolicitanteFilter != None):
        query = query.filter( \
            ConvocacaoVaga.contato_solicitante.ilike("%%{}%%".format(contatoSolicitanteFilter)) \
            )

    pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
    convocacaoVagas = pagination.items
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

    for convocacaoVaga in convocacaoVagas:
        data = {}
        data['id'] = convocacaoVaga.id
        data['vaga_id'] = convocacaoVaga.vaga_id
        data['contrato_empresa_id'] = convocacaoVaga.contrato_empresa_id
        data['data_convocacao'] = convocacaoVaga.data_convocacao
        data['nome_solicitante'] = convocacaoVaga.nome_solicitante
        data['contato_solicitante'] = convocacaoVaga.contato_solicitante
        data['data_entrevista'] = convocacaoVaga.data_entrevista

        output['itens'].append(data)

    return jsonify(output)

#--------------------------------------------------------------------------------------------------#

@app.route('/convocacao-vaga/view/<convocacao_vaga_id>', methods = ['GET'])
@jwt_required
@resource('convocacaoVaga-view')
def convocacaoVagaView(convocacao_vaga_id):

    convocacaoVaga = ConvocacaoVaga.query.get(convocacao_vaga_id)

    if not convocacaoVaga:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(convocacao_vaga_id), 'error': True})

    data = {'error': False}
    data['id'] = convocacaoVaga.id
    data['vaga_id'] = convocacaoVaga.vaga_id
    data['contrato_empresa_id'] = convocacaoVaga.contrato_empresa_id
    data['data_convocacao'] = convocacaoVaga.data_convocacao
    data['nome_solicitante'] = convocacaoVaga.nome_solicitante
    data['contato_solicitante'] = convocacaoVaga.contato_solicitante
    data['data_entrevista'] = convocacaoVaga.data_entrevista

    return jsonify(data)

#--------------------------------------------------------------------------------------------------#

@app.route('/convocacao-vaga/add', methods=['POST'])
@jwt_required
@resource('convocacaoVaga-add')
def convocacaoVagaAdd():
    data = request.get_json()

    validator = ConvocacaoVagaValidator(data)
    errors = validator.validate()

    if(errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error':errors['has'], 'errors':errors}), 200

    convocacaoVaga = ConvocacaoVaga(
        data['vaga_id'],
        data['contrato_empresa_id'],
        data['data_convocacao'],
        data['nome_solicitante'],
        data['contato_solicitante'],
        data['data_entrevista']
    )
    db.session.add(convocacaoVaga)

    try:
        db.session.commit()
        return jsonify(
            {'message': Messages.REGISTER_SUCCESS_CREATED.format("Convocação Vaga"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#

@app.route('/convocacao-vaga/edit/<convocacao_vaga_id>', methods=['PUT'])
@jwt_required
@resource('convocacaoVaga-edit')
def convocacaoVagaEdit(convocacao_vaga_id):

    convocacaoVaga = ConvocacaoVaga.query.get(convocacao_vaga_id)

    if not convocacaoVaga:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND, 'error': True})

    data = request.get_json()
    validator = ConvocacaoVagaValidator(data)
    errors = validator.validate()

    if(errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    convocacaoVaga.vaga_id = data['vaga_id']
    convocacaoVaga.contato_solicitante = data['contato_solicitante']
    convocacaoVaga.contrato_empresa_id = data['contrato_empresa_id']
    convocacaoVaga.nome_solicitante = data['nome_solicitante']
    convocacaoVaga.data_convocacao = data['data_convocacao']
    convocacaoVaga.data_entrevista = data['data_entrevista']

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_UPDATED.format("Convocação Vaga"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#


@app.route('/convocacao-vaga/delete/<convocacao_vaga_id>', methods=['DELETE'])
@jwt_required
@resource('convocacaoVaga-delete')
def convocacaoVagaDelete(convocacao_vaga_id):

    convocacaoVaga = ConvocacaoVaga.query.get(convocacao_vaga_id)

    if not convocacaoVaga:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(convocacao_vaga_id), 'error': True})

    db.session.delete(convocacaoVaga)

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_DELETED.format(convocacao_vaga_id), 'error' : False})
    except exc.IntegrityError:
        return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})
