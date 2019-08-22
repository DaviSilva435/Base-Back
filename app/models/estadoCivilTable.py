from app import db

class EstadoCivil(db.Model):
	__tablename__ = "estado_civil"

	id = db.Column(db.Integer, primary_key = True)
	nome = db.Column(db.String(255), nullable=False)

	estudantes = db.relationship('Estudante', backref='estado_civil', lazy=True)

#--------------------------------------------------------------------------------------------------#

	def __init__(self, nome):
		self.nome = nome

#--------------------------------------------------------------------------------------------------#

	def __repr__(self):
		return "<EstadoCivil - {} - {}>".format(self.id, self.nome)