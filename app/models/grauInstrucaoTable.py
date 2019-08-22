from app import db

class GrauInstrucao(db.Model):
	__tablename__ = "grau_instrucao"

	id = db.Column(db.Integer, primary_key = True)
	nome = db.Column(db.String(400), nullable=False)

	Estudante = db.relationship('Estudante', backref='grau_instrucao', lazy=True)

#--------------------------------------------------------------------------------------------------#

	def __init__(self, nome):
		self.nome = nome

#--------------------------------------------------------------------------------------------------#

	def __repr__(self):
		return "<GrauInstrução - {} - {}".format(self.id, self.nome)
