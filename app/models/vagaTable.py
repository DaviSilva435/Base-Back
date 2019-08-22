from app import db
from sqlalchemy.orm import validates

class Vaga(db.Model):
    __tablename__ = "vaga"

    id = db.Column(db.BigInteger, primary_key = True)
    contrato_empresa_id = db.Column(db.BigInteger, db.ForeignKey('contrato_empresa.id'))
    quantidade_vagas = db.Column(db.Integer, nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('curso_estudante.id'))
    ano = db.Column(db.Integer, nullable=False)
    semestre = db.Column(db.Integer, nullable=False)
    sexo_preferencial = db.Column(db.String(1), nullable=False)
    conhecimento_especifico = db.Column(db.Text, nullable=True)
    atividades_desenvolvidas = db.Column(db.Text, nullable=False)
    responsavel_estagiario = db.Column(db.String(255), nullable=False)
    email_responsavel = db.Column(db.String(255), nullable=False)
    endereco_estagiario = db.Column(db.String(255), nullable=False)
    valor_bolsa = db.Column(db.Float, nullable=False)
    observacao = db.Column(db.Text, nullable=True)


    BeneficioVaga = db.relationship('BeneficioVaga', backref='vaga', lazy=True)
    DiasVaga = db.relationship('DiasVaga', backref='vaga', lazy =True)
    ConvocacaoVaga = db.relationship('ConvocacaoVaga', backref='vaga', lazy=True)

#--------------------------------------------------------------------------------------------------#

    def __init__(self, contrato_empresa_id, quantidade_vagas, curso_id, ano, semestre, sexo_preferencial,\
                 conhecimento_especifico, atividades_desenvolvidas, responsavel_estagiario, email_responsavel, endereco_estagiario,\
                 valor_bolsa, observacao):
        self.contrato_empresa_id = contrato_empresa_id
        self.quantidade_vagas = quantidade_vagas
        self.curso_id = curso_id
        self.ano = ano
        self.semestre = semestre
        self.sexo_preferencial = sexo_preferencial
        self.conhecimento_especifico = conhecimento_especifico
        self.atividades_desenvolvidas =atividades_desenvolvidas
        self.responsavel_estagiario = responsavel_estagiario
        self.email_responsavel = email_responsavel
        self.endereco_estagiario = endereco_estagiario
        self.valor_bolsa = valor_bolsa
        self.observacao = observacao

#--------------------------------------------------------------------------------------------------#

    def __repr__(self):
        return "<Vaga %r>" % self.contrato_empresa_id