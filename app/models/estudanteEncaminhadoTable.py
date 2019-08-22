from app import db

class EstudanteEncaminhado(db.Model):
    __tablename__ = 'estudante_encaminhado'
    estudante_id = db.Column(db.Integer, db.ForeignKey('estudante.id'), primary_key=True)
    convocacao_id = db.Column(db.Integer, db.ForeignKey('convocacao_vaga.id'), primary_key=True)
    contratado = db.Column(db.Boolean, nullable=False)

    Estudante = db.relationship('Estudante', backref='estudante_encaminhado', lazy=True)
    ConvocacaoVaga = db.relationship('ConvocacaoVaga', backref='estudante_encaminhado', lazy=True)

#---------------------------------------------------------------------------------------#

    def __init__(self, estudante_id, convocacao_id, contratado):
        self.estudante_id = estudante_id
        self.convocacao_id = convocacao_id
        self.contratado = contratado

#---------------------------------------------------------------------------------------#

    def __repr__(self):
        return "<Estudante encaminhado - {} - {} - {}>".format(self.estudante_id, self.convocacao_id, self.contratado)
