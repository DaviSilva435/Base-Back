from app import db

class ConvocacaoVaga(db.Model):
    __tablename__ = "convocacao_vaga"

    id = db.Column(db.BigInteger, primary_key=True)
    vaga_id = db.Column(db.BigInteger, db.ForeignKey('vaga.id'))
    contrato_empresa_id = db.Column(db.BigInteger, db.ForeignKey('contrato_empresa.id'))
    data_convocacao = db.Column(db.Date)
    nome_solicitante = db.Column(db.String(255), nullable=False)
    contato_solicitante = db.Column(db.String(255), nullable = False)
    data_entrevista = db.Column(db.DateTime)

    EstudanteEncaminhado = db.relationship('EstudanteEncaminhado', backref='convocacao_vaga', lazy=True)

#---------------------------------------------------------------------------------#

    def __init__(self, vaga_id, contrato_empresa_id, data_convocacao,\
                 nome_solicitante, contato_solicitante,data_entrevista):
        self.vaga_id = vaga_id
        self.contrato_empresa_id = contrato_empresa_id
        self.data_convocacao = data_convocacao
        self.nome_solicitante = nome_solicitante
        self.contato_solicitante = contato_solicitante
        self.data_entrevista = data_entrevista

#---------------------------------------------------------------------------------#

    def __repr__(self):
        return "<Convocacao Vaga - {} - {} - {} - {} - {} - {} - {}>".format(self.id, self.vaga_id, self.contrato_empresa_id, self.data_convocacao, self.nome_solicitante, self.contato_solicitante, self.data_entrevista)