from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from werkzeug.security import check_password_hash

app = Flask(__name__)
CORS(app)
app.config.from_object('config')
jwt = JWTManager(app)
db  = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

import Messages
from app.components import fieldsFormatter

#tables
from app.models.rolesTable import Role
from app.models.usersTable import User
from app.models.controllersTable import Controller
from app.models.actionsTable import Action
from app.models.resourcesTable import Resource
from app.models.privilegesTable import Privilege
from app.models.centroEstagioTable import CentroEstagio
from app.models.empresaTable import Empresa
from app.models.cidadeTable import Cidade
from app.models.ufTable import Uf
from app.models.tipoEstudanteTable import TipoEstudante
from app.models.taxasTipoEstudanteTable import TaxasTipoEstudante
from app.models.seguradoraTable import Seguradora
from app.models.contratoEmpresaTable import ContratoEmpresa
from app.models.contatoEmpresaTable import ContatoEmpresa
from app.models.apoliceTable import Apolice
from app.models.apoliceMesAnoTable import ApoliceMesAno
from app.models.apoliceEstudanteTable import ApoliceEstudante
from app.models.apoliceEstudanteConsolidadoTable import ApoliceEstudanteConsolidado
#estudante
from app.models.cboTable import Cbo
from app.models.estadoCivilTable import EstadoCivil
from app.models.tipoConhecimentoTable import TipoConhecimento
from app.models.cursoEstudanteTable import CursoEstudante
from app.models.periodoCursoTable import PeriodoCurso
from app.models.grauInstrucaoTable import GrauInstrucao
from app.models.categoriaHabilitacaoTable import CategoriaHabilitacao
from app.models.tipoVeiculoTable import TipoVeiculo
from app.models.estudanteTable import Estudante
from app.models.escolaTable import Escola
from app.models.conhecimentoTable import Conhecimento
from app.models.experienciaProfissionalEstudanteTable import ExperienciaProfissionalEstudante
from app.models.conhecimentoEstudanteTable import ConhecimentoEstudante
from app.models.cursoAdicionalEstudanteTable import CursoAdicionalEstudante
#selecao_estudante
from app.models.beneficioTable import Beneficio
from app.models.beneficioVagaTable import BeneficioVaga
from app.models.convocacaoVagaTable import ConvocacaoVaga
from app.models.diasVagaTable import DiasVaga
from app.models.estudanteEncaminhadoTable import EstudanteEncaminhado
from app.models.vagaTable import Vaga

#validators
from app.validators.formValidator import FormValidator
from app.validators.authValidator import AuthValidator
from app.validators.userValidator import UserValidator
from app.validators.centroEstagioValidator import CentroEstagioValidator
from app.validators.tipoEstudanteValidator import TipoEstudanteValidator
from app.validators.seguradoraValidator import SeguradoraValidator
from app.validators.empresaValidator import EmpresaValidator
from app.validators.contatoEmpresaValidator import ContatoEmpresaValidator
from app.validators.contratoEmpresaValidator import ContratoEmpresaValidator
from app.validators.taxasTipoEstudanteValidator import TaxasTipoEstudanteValidator
from app.validators.cidadeValidator import CidadeValidator
from app.validators.ufValidator import UfValidator
from app.validators.apoliceEstudanteValidator import ApoliceEstudanteValidator
from app.validators.apoliceValidator import ApoliceValidator
#estudante
from app.validators.escolaValidator import EscolaValidator
from app.validators.estudanteValidator import EstudanteValidator
from app.validators.tipoConhecimentoValidator import TipoConhecimentoValidator
from app.validators.conhecimentoValidator import ConhecimentoValidator
from app.validators.conhecimentoEstudanteValidator import ConhecimentoEstudanteValidator
from app.validators.cursoAdicionalEstudanteValidator import CursoAdicionalEstudanteValidator
from app.validators.cboValidator import CboValidator
from app.validators.experienciaProfissionalEstudanteValidator import ExperienciaProfissionalEstudanteValidator
from app.validators.estadoCivilValidator import EstadoCivilValidator
from app.validators.periodoCursoValidator import PeriodoCursoValidator
from app.validators.grauInstrucaoValidator import GrauInstrucaoValidator
from app.validators.categoriaHabilitacaoValidator import CategoriaHabilitacaoValidator
from app.validators.tipoVeiculoValidator import TipoVeiculoValidator
from app.validators.cursoEstudanteValidator import CursoEstudanteValidator
#selecaoEstudante
from app.validators.diasVagaValidator import DiasVagaValidator
from app.validators.beneficioValidator import BeneficioValidator
from app.validators.beneficioVagaValidator import BeneficioVagaValidator
from app.validators.vagaValidator import VagaValidator
from app.validators.convocacaoVagaValidator import ConvocacaoVagaValidator
from app.validators.estudanteEncaminhadoValidator import EstudanteEncaminhadoValidator
from app.validators.rolesValidator import RolesValidator

#controllers
from app.controllers import usersController
from app.controllers import authController
from app.controllers import centroEstagioController
from app.controllers import tipoEstudanteController
from app.controllers import seguradoraController
from app.controllers import empresaController
from app.controllers import contatoEmpresaController
from app.controllers import contratoEmpresaController
from app.controllers import taxasTipoEstudanteController
from app.controllers import cidadeController
from app.controllers import ufController
from app.controllers import apoliceMesAnoController
from app.controllers import apoliceEstudanteController
from app.controllers import apoliceController
#estudante
from app.controllers import escolaController
from app.controllers import estudanteController
from app.controllers import tipoConhecimentoController
from app.controllers import conhecimentoController
from app.controllers import conhecimentoEstudanteController
from app.controllers import cursoAdicionalEstudanteController
from app.controllers import cboController
from app.controllers import experienciaProfissionalEstudanteController
from app.controllers import estadoCivilController
from app.controllers import periodoCursoController
from app.controllers import grauInstrucaoController
from app.controllers import categoriaHabilitacaoController
from app.controllers import tipoVeiculoController
from app.controllers import cursoEstudanteController
#selecaoEstudante
from app.controllers import diasVagaController
from app.controllers import beneficioController
from app.controllers import beneficioVagaController
from app.controllers import vagaController
from app.controllers import convocacaoVagaController
from app.controllers import estudanteEncaminhadoController
from app.controllers import rolesController