from app import db

class TipoEstudante(db.Model):
	__tablename__ = "tipo_estudante"

	id = db.Column(db.Integer, primary_key = True)
	nome = db.Column(db.String(255), nullable=False)
	
	taxas = db.relationship('TaxasTipoEstudante', backref='tipo_estudante', lazy=True)

#--------------------------------------------------------------------------------------------------#

	def __init__(self, nome):
		self.nome = nome

#--------------------------------------------------------------------------------------------------#
		
	def __repr__(self):
		return "<TipoEstudante %r>" % self.id
