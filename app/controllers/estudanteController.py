from app 				import app, db, Messages
from flask 				import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy 		import exc
from . 					import resource
from app import Estudante
from app import EstudanteValidator
from app import fieldsFormatter
from app import ConhecimentoEstudante
from app import CursoAdicionalEstudante
from app import ExperienciaProfissionalEstudante


#--------------------------------------------------------------------------------------------------#

@app.route('/estudante/all', methods=['GET'])
@jwt_required
@resource('estudante-all')
def estudanteAll():

    page = request.args.get('page', 1, type=int)
    nomeFilter = request.args.get('nome', None)
    sexoFilter = request.args.get('sexo', None)
    cepFilter = request.args.get('cep', None)
    enderecoFilter = request.args.get('endereco', None)
    bairroFilter = request.args.get('bairro', None)
    telefoneFilter = request.args.get('telefone', None)
    celularFilter = request.args.get('celular', None)
    emailFilter = request.args.get('email', None)
    data_nascimentoFilter = request.args.get('data_nascimento', None)
    rgFilter = request.args.get('rg', None)
    cpfFilter = request.args.get('cpf', None)
    nome_paiFilter = request.args.get('nome_pai', None)
    nome_maeFilter = request.args.get('nome_mae', None)
    anoFilter = request.args.get('ano', None)
    habilitacaoFilter = request.args.get('habilitacao', None)
    conducao_propriaFilter = request.args.get('conducao_propria', None)
    #FK
    cidade_idFilter = request.args.get('cidade_id', None)
    estado_civil_idFilter = request.args.get('estado_civil_id', None)
    curso_idFilter = request.args.get('curso_id', None)
    escola_idFilter = request.args.get('escola_id', None)
    periodo_curso_idFilter = request.args.get('periodo_curso_id', None)
    grau_instrucao_idFilter = request.args.get('grau_instrucao_id', None)
    categoria_habilitacao_idFilter = request.args.get('categoria_habilitacao_id', None)
    tipo_veiculo_idFilter = request.args.get('tipo_veiculo_id', None)
    centro_estagio_idFilter = request.args.get('centro_estagio_id', None)

    rowsPerPage = app.config['ROWS_PER_PAGE']

    query = Estudante.query.order_by(Estudante.nome)

    #FK
    if (cidade_idFilter != None):
        query = query.filter(
            Estudante.cidade_id == cidade_idFilter
            )
    if (estado_civil_idFilter != None):
        query = query.filter(
            Estudante.estado_civil_id == estado_civil_idFilter
            )
    if (curso_idFilter != None):
        query = query.filter(
            Estudante.curso_id == curso_idFilter
            )
    if (escola_idFilter != None):
        query = query.filter(
            Estudante.escola_id == escola_idFilter
            )
    if (periodo_curso_idFilter != None):
        query = query.filter(
            Estudante.periodo_curso_id == periodo_curso_idFilter
            )
    if (grau_instrucao_idFilter != None):
        query = query.filter(
            Estudante.grau_instrucao_id == grau_instrucao_idFilter
            )
    if (categoria_habilitacao_idFilter != None):
        query = query.filter(
            Estudante.categoria_habilitacao_id == categoria_habilitacao_idFilter
            )
    if (tipo_veiculo_idFilter != None):
        query = query.filter(
            Estudante.tipo_veiculo_id == tipo_veiculo_idFilter
            )
    if (centro_estagio_idFilter != None):
        query = query.filter(
            Estudante.centro_estagio_id == centro_estagio_idFilter
            )


    if (nomeFilter != None):
        query = query.filter( \
            Estudante.nome.ilike("%%{}%%".format(nomeFilter)) \
            )
    if (sexoFilter!= None):
        query = query.filter( \
            Estudante.sexo.ilike("%%{}%%".format(sexoFilter)) \
            )
    if (cepFilter != None):
        query = query.filter( \
            Estudante.cep.ilike("%%{}%%".format(cepFilter)) \
            )
    if (enderecoFilter != None):
        query = query.filter( \
            Estudante.endereco.ilike("%%{}%%".format(enderecoFilter)) \
            )
    if (bairroFilter != None):
        query = query.filter(
            Estudante.bairro.ilike("%{}%".format(bairroFilter))
        )
    if (telefoneFilter != None):
        query = query.filter(
            Estudante.telefone.ilike("%{}%".format(telefoneFilter))
        )
    if (celularFilter != None):
        query = query.filter(
            Estudante.celular.ilike("%{}%".format(celularFilter))
        )
    if (emailFilter != None):
        query = query.filter(
            Estudante.email.ilike("%{}%".format(emailFilter))
        )
    if (data_nascimentoFilter != None):
        query = query.filter(
            Estudante.data_nascimento.ilike("%{}%".format(data_nascimentoFilter))
        )
    if (rgFilter != None):
        query = query.filter(
            Estudante.rg.ilike("%{}%".format(rgFilter))
        )
    if (cpfFilter != None):
        query = query.filter(
            Estudante.cpf.ilike("%{}%".format(cpfFilter))
        )
    if (nome_paiFilter != None):
        query = query.filter(
            Estudante.nome_pai.ilike("%{}%".format(nome_paiFilter))
        )
    if (nome_maeFilter != None):
        query = query.filter(
            Estudante.nome_mae.ilike("%{}%".format(nome_maeFilter))
        )
    if (anoFilter != None):
        query = query.filter(
            Estudante.ano.ilike("%{}%".format(anoFilter))
        )
    if (habilitacaoFilter != None):
        query = query.filter(
            Estudante.habilitacao.ilike("%{}%".format(habilitacaoFilter))
        )
    if (conducao_propriaFilter != None):
        query = query.filter(
            Estudante.conducao_propria.ilike("%{}%".format(conducao_propriaFilter))
        )

    pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
    estudantes = pagination.items
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

    for estudante in estudantes:
        data = {}
        data['id'] = estudante.id
        data['nome'] = estudante.nome
        data['sexo'] = estudante.sexo
        data['cep'] = estudante.cep
        data['endereco'] = estudante.endereco
        data['bairro'] = estudante.bairro
        data['telefone'] = estudante.telefone
        data['celular'] = estudante.celular
        data['email'] = estudante.email
        data['data_nascimento'] = estudante.data_nascimento
        data['rg'] = estudante.rg
        data['cpf'] = estudante.cpf
        data['nome_pai'] = estudante.nome_pai
        data['nome_mae'] = estudante.nome_mae
        data['ano'] = estudante.ano
        data['habilitacao'] = estudante.habilitacao
        data['conducao_propria'] = estudante.conducao_propria
        data['cidade_id'] = estudante.cidade_id

        data['estado_civil_id'] = estudante.estado_civil_id
        data['curso_id'] = estudante.curso_id
        data['escola_id'] = estudante.escola_id
        data['periodo_curso_id'] = estudante.periodo_curso_id
        data['grau_instrucao_id'] = estudante.grau_instrucao_id
        data['categoria_habilitacao_id'] = estudante.categoria_habilitacao_id
        data['tipo_veiculo_id'] = estudante.tipo_veiculo_id
        data['centro_estagio_id'] = estudante.centro_estagio_id

        output['itens'].append(data)

    return jsonify(output)

#--------------------------------------------------------------------------------------------------#

@app.route('/estudante/view/<estudante_id>', methods = ['GET'])
@jwt_required
@resource('estudante-view')
def estudanteView(estudante_id):

    estudante = Estudante.query.get(estudante_id)

    if not estudante:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(estudante_id), 'error': True})

    data = {'error': False}
    data['id'] = estudante.id
    data['nome'] = estudante.nome
    data['sexo'] = estudante.sexo
    data['cep'] = estudante.cep
    data['endereco'] = estudante.endereco
    data['bairro'] = estudante.bairro
    data['telefone'] = estudante.telefone
    data['celular'] = estudante.celular
    data['email'] = estudante.email
    data['data_nascimento'] = estudante.data_nascimento
    data['rg'] = estudante.rg
    data['cpf'] = estudante.cpf
    data['nome_pai'] = estudante.nome_pai
    data['nome_mae'] = estudante.nome_mae
    data['ano'] = estudante.ano
    data['habilitacao'] = estudante.habilitacao
    data['conducao_propria'] = estudante.conducao_propria

    data['cidade_id'] = {}
    data['cidade_id']['id'] = estudante.cidade.id
    data['cidade_id']['cidade'] = estudante.cidade.nome

    data['uf'] = {}
    data['uf']['id'] = estudante.cidade.uf.id
    data['uf']['nome'] = estudante.cidade.uf.nome
    data['uf']['sigla'] = estudante.cidade.uf.sigla

    data['estado_civil_id'] = estudante.estado_civil_id
    data['curso_id'] = estudante.curso_id
    data['escola_id'] = estudante.escola_id
    data['periodo_curso_id'] = estudante.periodo_curso_id
    data['grau_instrucao_id'] = estudante.grau_instrucao_id
    data['categoria_habilitacao_id!'] = estudante.categoria_habilitacao_id
    data['tipo_veiculo_id'] = estudante.tipo_veiculo_id
    data['centro_estagio_id'] = estudante.centro_estagio_id

    return jsonify(data)

#--------------------------------------------------------------------------------------------------#

@app.route('/estudante/add', methods=['POST'])
@jwt_required
@resource('estudante-add')
def estudanteAdd():
    data = request.get_json()

    validator = EstudanteValidator(data)
    errors = validator.validate()

    if(errors['has']):
       return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error':errors['has'], 'errors':errors}), 200

    estudante = Estudante(
        data['nome'],
        data['sexo'],
        fieldsFormatter.CepFormatter().clean(data['cep']),
        data['endereco'],
        data['bairro'],
        data['cidade_id'],
        fieldsFormatter.PhoneFormatter().clean(data['telefone']),
        fieldsFormatter.PhoneFormatter().clean(data['celular']),
        data['email'],
        data['estado_civil_id'],
        data['data_nascimento'],
        data['rg'],
        fieldsFormatter.CpfFormatter().clean(data['cpf']),
        data['nome_pai'],
        data['nome_mae'],
        data['curso_id'],
        data['escola_id'],
        data['periodo_curso_id'],
        data['grau_instrucao_id'],
        data['ano'],
        data['habilitacao'],
        data['categoria_habilitacao_id'],
        data['conducao_propria'],
        data['tipo_veiculo_id'],
        data['centro_estagio_id']
    )
    db.session.add(estudante)

    try:
        db.session.commit()
        return jsonify(
            {'message': Messages.REGISTER_SUCCESS_CREATED.format("Estudamte"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CREATE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#

@app.route('/estudante/edit/<estudante_id>', methods=['PUT'])
@jwt_required
@resource('estudante-edit')
def estudanteEdit(estudante_id):

    estudante = Estudante.query.get(estudante_id)

    if not estudante:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND, 'error': True})

    data = request.get_json()
    validator = EstudanteValidator(data)
    errors = validator.validate()

    if(errors['has']):
        return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

    estudante.nome = data['nome']
    estudante.sexo = data['sexo']
    estudante.cep = fieldsFormatter.CepFormatter().clean(data['cep'])
    estudante.endereco = data['endereco']
    estudante.bairro = data['bairro']
    estudante.telefone = fieldsFormatter.PhoneFormatter().clean(data['telefone'])
    estudante.celular = fieldsFormatter.PhoneFormatter().clean(data['celular'])
    estudante.email = data['email']
    estudante.data_nascimento = data['data_nascimento']
    estudante.rg = data['rg']
    estudante.cpf = fieldsFormatter.CpfFormatter().clean(data['cpf'])
    estudante.nome_pai = data['nome_pai']
    estudante.nome_mae = data['nome_mae']
    estudante.ano = data['ano']
    estudante.habilitacao = data['habilitacao']
    estudante.conducao_propria = data['conducao_propria']

    estudante.cidade_id = data['cidade_id']
    estudante.estado_civil_id = data['estado_civil_id']
    estudante.curso_id = data['curso_id']
    estudante.escola_id = data['escola_id']
    estudante.periodo_curso_id = data['periodo_curso_id']
    estudante.grau_instrucao_id = data['grau_instrucao_id']
    estudante.categoria_habilitacao_id = data['categoria_habilitacao_id']
    estudante.tipo_veiculo_id = data['tipo_veiculo_id']
    estudante.centro_estagio_id = data['centro_estagio_id']

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_UPDATED.format("Estudante"), 'error': False})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': Messages.REGISTER_CHANGE_INTEGRITY_ERROR, 'error': True})

#--------------------------------------------------------------------------------------------------#

@app.route('/estudante/delete/<estudante_id>', methods=['DELETE'])
@jwt_required
@resource('estudante-delete')
def estudanteDelete(estudante_id):

    estudante = Estudante.query.get(estudante_id)

    if not estudante:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format(estudante_id), 'error': True})

    ConhecimentoEstudante.query.filter(ConhecimentoEstudante.estudante_id == estudante_id).delete()
    CursoAdicionalEstudante.query.filter(CursoAdicionalEstudante.estudante_id == estudante_id).delete()
    ExperienciaProfissionalEstudante.query.filter(ExperienciaProfissionalEstudante.estudante_id == estudante_id).delete()

    db.session.delete(estudante)

    try:
        db.session.commit()
        return jsonify({'message': Messages.REGISTER_SUCCESS_DELETED.format(estudante_id), 'error' : False})
    except exc.IntegrityError:
        return jsonify({'message': Messages.REGISTER_DELETE_INTEGRITY_ERROR, 'error': True})
