from app 				import app, db, Messages
from flask 				import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy 		import exc
from . 					import resource
from app import Vaga
from app import VagaValidator
from app import fieldsFormatter

#--------------------------------------------------------------------------------------------------#

@app.route('/vaga/all', methods=['GET'])
@jwt_required
@resource('vaga-all')
def vagaAll():

    page = request.args.get('page', 1, type=int)
    quantidadeVagasIdFilter = request.args.get('quantidade_vagas', None)
    anoFilter = request.args.get('ano', None)
    semestreFilter = request.args.get('semestre', None)
    sexoPreferencialFilter = request.args.get('sexo_preferencial', None)
    conhecimentoEspecificoFilter = request.args.get('conhecimento_especifico', None)
    atividadesDesenvolvidasFilter = request.args.get('atividades_desenvolvidas', None)
    responsavelEstagiarioFilter = request.args.get('responsavel_estagiario', None)
    emailResponsavelFilter = request.args.get('email_responsavel', None)
    enderecoEstagiarioFilter = request.args.get('endereco_estagiario', None)
    valorBolsaFilter = request.args.get('valor_bolsa', None)
    observacaoFilter = request.args.get('observacao', None)

    contratoEmpresaIdFilter = request.args.get('contrato_empresa_id', None)
    cursoIdFilter = request.args.get('curso_id', None)

    rowsPerPage = app.config['ROWS_PER_PAGE']

    query = Vaga.query.order_by(Vaga.contrato_empresa_id)


    if (contratoEmpresaIdFilter != None):
        query = query.filter(
            Vaga.contrato_empresa_id == contratoEmpresaIdFilter
            )
    if (cursoIdFilter != None):
        query = query.filter(
            Vaga.curso_id == cursoIdFilter
            )

    if (quantidadeVagasIdFilter != None):
        query = query.filter(
            Vaga.quantidade_vagas == quantidadeVagasIdFilter
            )
    if (anoFilter != None):
        query = query.filter(
            Vaga.ano == anoFilter
            )
    if (semestreFilter != None):
        query = query.filter(
            Vaga.semestre == semestreFilter
            )
    if (sexoPreferencialFilter != None):
        query = query.filter( \
            Vaga.sexo_preferencial.ilike("%%{}%%".format(sexoPreferencialFilter)) \
            )
    if (conhecimentoEspecificoFilter != None):
        query = query.filter( \
            Vaga.conhecimento_especifico.ilike("%%{}%%".format(conhecimentoEspecificoFilter)) \
            )
    if (atividadesDesenvolvidasFilter != None):
        query = query.filter( \
            Vaga.atividades_desenvolvidas.ilike("%%{}%%".format(atividadesDesenvolvidasFilter)) \
            )
    if (responsavelEstagiarioFilter != None):
        query = query.filter( \
            Vaga.responsavel_estagiario.ilike("%%{}%%".format(responsavelEstagiarioFilter)) \
            )
    if (emailResponsavelFilter != None):
        query = query.filter( \
            Vaga.email_responsavel.ilike("%%{}%%".format(emailResponsavelFilter)) \
            )
    if (enderecoEstagiarioFilter != None):
        query = query.filter( \
            Vaga.endereco_estagiario.ilike("%%{}%%".format(enderecoEstagiarioFilter)) \
            )
    if (valorBolsaFilter != None):
        query = query.filter(
            Vaga.valor_bolsa == valorBolsaFilter
            )
    if (observacaoFilter != None):
        query = query.filter( \
            Vaga.observacao.ilike("%%{}%%".format(observacaoFilter)) \
            )

    pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
    vagas = pagination.items
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

    for vaga in vagas:
        data = {}
        data['id'] = vaga.id
        data['contrato_empresa_id'] = vaga.contrato_empresa_id
        data['quantidade_vagas'] = vaga.quantidade_vagas
        data['curso_id'] = vaga.curso_id
        data['ano'] = vaga.ano
        data['semestre'] = vaga.semestre
        data['sexo_preferencial'] = vaga.sexo_preferencial
        data['conhecimento_especifico'] = vaga.conhecimento_especifico
        data['atividades_desenvolvidas'] = vaga.atividades_desenvolvidas
        data['responsavel_estagiario'] = vaga.responsavel_estagiario
        data['email_responsavel'] = vaga.email_responsavel
        data['endereco_estagiario'] = vaga.endereco_estagiario
        data['valor_bolsa'] = vaga.valor_bolsa
        data['observacao'] = vaga.observacao

        output['itens'].append(data)

    return jsonify(output)

#--------------------------------------------------------------------------------------------------#

@app.route('/vaga/view/<vaga_id>', methods = ['GET'])
@jwt_required
@resource('vaga-view')
def vagaView(vaga_id):

    vaga = Vaga.query.get(vaga_id)

    if not vaga:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(vaga_id), 'error': True})

    data = {'error': False}
    data['id'] = vaga.id
    data['quantidade_vagas'] = vaga.quantidade_vagas
    data['ano'] = vaga.ano
    data['semestre'] = vaga.semestre
    data['sexo_preferencial'] = vaga.sexo_preferencial
    data['conhecimento_especifico'] = vaga.conhecimento_especifico
    data['atividades_desenvolvidas'] = vaga.atividades_desenvolvidas
    data['responsavel_estagiario'] = vaga.responsavel_estagiario
    data['email_responsavel'] = vaga.email_responsavel
    data['endereco_estagiario'] = vaga.endereco_estagiario
    data['valor_bolsa'] = vaga.valor_bolsa
    data['observacao'] = vaga.observacao

    data['contrato_empresa_id'] = vaga.contrato_empresa_id

    data['curso_id'] = vaga.curso_id


    return jsonify(data)

#--------------------------------------------------------------------------------------------------#

@app.route('/vaga/add', methods=['POST'])
@jwt_required
@resource('vaga-add')
def vagaAdd():
    data = request.get_json()

    validator = VagaValidator(data)
    errors = validator.validate()

    if(errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error':errors['has'], 'errors':errors}), 200

    vaga = Vaga(
        data['contrato_empresa_id'],
        data['quantidade_vagas'],
        data['curso_id'],
        data['ano'],
        data['semestre'],
        data['sexo_preferencial'],
        data['conhecimento_especifico'],
        data['atividades_desenvolvidas'],
        data['responsavel_estagiario'],
        data['email_responsavel'],
        data['endereco_estagiario'],
        data['valor_bolsa'],
        data['observacao']
    )
    db.session.add(vaga)

    try:
        db.session.commit()
        return jsonify(
            {'message': Messages.REGISTER_SUCCESS_CREATED.format("Vaga"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#

@app.route('/vaga/edit/<vaga_id>', methods=['PUT'])
@jwt_required
@resource('vaga-edit')
def vagaEdit(vaga_id):

    vaga = Vaga.query.get(vaga_id)

    if not vaga:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND, 'error': True})

    data = request.get_json()
    validator = VagaValidator(data)
    errors = validator.validate()

    if(errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    vaga.nome = data['contrato_empresa_id']
    vaga.quantidade_vagas = data['quantidade_vagas']
    vaga.curso_id = data['curso_id']
    vaga.ano = data['ano']
    vaga.semestre = data['semestre']
    vaga.sexo_preferencial = data['sexo_preferencial']
    vaga.conhecimento_especifico = data['conhecimento_especifico']
    vaga.atividades_desenvolvidas = data['atividades_desenvolvidas']
    vaga.responsavel_estagiario = data['responsavel_estagiario']
    vaga.email_responsavel = data['email_responsavel']
    vaga.endereco_estagiario = data['endereco_estagiario']
    vaga.valor_bolsa = data['valor_bolsa']
    vaga.observacao = data['observacao']

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_UPDATED.format("Vaga"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#


@app.route('/vaga/delete/<vaga_id>', methods=['DELETE'])
@jwt_required
@resource('vaga-delete')
def vagaDelete(vaga_id):

    vaga = Vaga.query.get(vaga_id)

    if not vaga:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(vaga_id), 'error': True})

    db.session.delete(vaga)

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_DELETED.format(vaga_id), 'error' : False})
    except exc.IntegrityError:
        return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})
