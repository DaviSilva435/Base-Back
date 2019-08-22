from app 				import app, db, Messages
from flask 				import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy 		import exc
from . 					import resource
from app import ApoliceMesAno
#from app import apoliceMesAnoValidator
from app import fieldsFormatter






@app.route('/apolice-mes-ano/all', methods=['GET'])
@jwt_required
@resource('apoliceMesAno-all')
def apoliceMesAnoAll():

    page = request.args.get('page', 1, type=int)
    seguradora_idFilter = request.args.get('seguradora_id', None)
    numeroFilter = request.args.get('numero', None)
    centro_estagio_idFilter = request.args.get('centro_estagio_id', None)
    mesFilter = request.args.get('mes', None)
    anoFilter = request.args.get('ano', None)
    rowsPerPage = app.config['ROWS_PER_PAGE']

    query = ApoliceMesAno.query.order_by(ApoliceMesAno.numero)

    if (seguradora_idFilter != None):
        query = query.filter( \
            ApoliceMesAno.seguradora_id == seguradora_idFilter
            )

    if (numeroFilter != None):
        query = query.filter( \
            ApoliceMesAno.numero == numeroFilter \
            )

    if (centro_estagio_idFilter != None):
        query = query.filter( \
            ApoliceMesAno.centro_estagio_id == centro_estagio_idFilter \
            )

    if (mesFilter != None):
        query = query.filter( \
            ApoliceMesAno.mes == mesFilter \
            )

    if (anoFilter != None):
        query = query.filter( \
            ApoliceMesAno.ano == anoFilter \
            )

    pagination = query.paginate(page=page, per_page=rowsPerPage, error_out=False)
    apolicesMesAno = pagination.items
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

    for apoliceMesAno in apolicesMesAno:
        data = {}
        data['seguradora_id'] = apoliceMesAno.seguradora_id
        data['numero'] = apoliceMesAno.numero
        data['centro_estagio_id'] = apoliceMesAno.centro_estagio_id
        data['mes'] = apoliceMesAno.mes
        data['ano'] = apoliceMesAno.ano

        output['itens'].append(data)

    return jsonify(output)

# --------------------------------------------------------------------------------------------------#

@app.route('/apolice-mes-ano/view/<seguradora_id>/<numero>/<centro_estagio_id>/<mes>/<ano>', methods=['GET'])
@jwt_required
@resource('apoliceMesAno-view')
def apoliceMesAnoView(seguradora_id,numero,centro_estagio_id,mes,ano):

    apoliceMesAno = ApoliceMesAno.query.get([seguradora_id,numero,centro_estagio_id,mes,ano])

    if not apoliceMesAno:
        return jsonify({'message': Messages.REGISTER_NOT_FOUND.format([seguradora_id,numero,centro_estagio_id,mes,ano]), 'error': True})

    data = {'error': False}
    data['seguradora_id'] = apoliceMesAno.seguradora_id
    data['numero'] = apoliceMesAno.numero
    data['centro_estagio_id'] = apoliceMesAno.centro_estagio_id
    data['mes'] = apoliceMesAno.mes
    data['ano'] = apoliceMesAno.ano

    return jsonify(data)








'''
@app.route('/apolice-mes-ano/edit', methods=['POST'])
# @jwt_required
# resource('apoliceMesAno-edit')
def apoliceMesAnoEdit():


@app.route('/apolice-mes-ano/add', methods=['POST'])
# @jwt_required
# resource('apoliceMesAno-add')
def apoliceMesAnoAdd():


@app.route('/apolice-mes-ano/delete', methods=['DELETE'])
# @jwt_required
# resource('apoliceMesAno-delete')
def apoliceMesAnoDelete():
'''