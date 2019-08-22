from app import db
from sqlalchemy.orm import validates

class Beneficio(db.Model):
    __tablename__ = "beneficio"

    id = db.Column(db.BigInteger, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)

    BeneficioVaga = db.relationship('BeneficioVaga', backref='beneficio', lazy=True)

    #--------------------------------------------------------------------------------------------------#

    def __init__(self, nome):
        self.nome = nome

#--------------------------------------------------------------------------------------------------#

    def __repr__(self):
        return "<Vaga %r>" % self.nome