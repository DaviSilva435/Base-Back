from app import db

class Cbo(db.Model):
	__tablename__ = "cbo"

	id = db.Column(db.Integer, primary_key = True)
	nome = db.Column(db.String(400), nullable=False)
	codigo = db.Column(db.String(255), nullable=False)

	experiencias = db.relationship('ExperienciaProfissionalEstudante', backref = 'cbo', lazy=True)

#--------------------------------------------------------------------------------------------------#

	def __init__(self, nome, codigo):
		self.nome = nome
		self.codigo = codigo

#--------------------------------------------------------------------------------------------------#

	def __repr__(self):
		return "<CBO - {} - {} - {}>".format(self.id, self.nome, self.codigo)
