from app import db

class BeneficioVaga(db.Model):
    __tablename__ = 'beneficio_vaga'
    beneficio_id = db.Column(db.Integer, db.ForeignKey('beneficio.id'), primary_key=True)
    vaga_id = db.Column(db.Integer, db.ForeignKey('vaga.id'), primary_key=True)
    valor = db.Column(db.Float, nullable=False)

#---------------------------------------------------------------------------------------#

    def __init__(self, beneficio_id, vaga_id, valor):
        self.beneficio_id = beneficio_id
        self.vaga_id = vaga_id
        self.valor = valor

#---------------------------------------------------------------------------------------#

    def __repr__(self):
        return "<Beneficio vaga - {} - {} - {}>".format(self.beneficio_id, self.vaga_id, self.valor)
