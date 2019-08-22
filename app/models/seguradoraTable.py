from app import db

class Seguradora(db.Model):
	__tablename__ = "seguradora"

	id = db.Column(db.Integer, primary_key = True)
	nome = db.Column(db.String(255), nullable=False)
	
	apolices = db.relationship('Apolice', backref='seguradora', lazy=True)
	apolicesMesAno = db.relationship('ApoliceMesAno', backref='seguradora', lazy=True)
	ApoliceEstudanteConsolidado = db.relationship('ApoliceEstudanteConsolidado', backref='seguradora', lazy=True)
	ApoliceEstudante = db.relationship('ApoliceEstudante', backref='seguradora', lazy=True)

#--------------------------------------------------------------------------------------------------#

	def __init__(self, nome):
		self.nome = nome

#--------------------------------------------------------------------------------------------------#
		
	def __repr__(self):
		return "<Seguradora %r>" % self.id
