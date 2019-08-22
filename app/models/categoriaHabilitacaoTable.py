from app import db

class CategoriaHabilitacao(db.Model):
	__tablename__ = "categoria_habilitacao"

	id = db.Column(db.Integer, primary_key = True)
	nome = db.Column(db.String(255), nullable=False)

	Estudante = db.relationship('Estudante', backref='categoria_habilitacao', lazy=True)

#--------------------------------------------------------------------------------------------------#

	def __init__(self, nome):
		self.nome = nome

#--------------------------------------------------------------------------------------------------#

	def __repr__(self):
		return "<CategoriaHabilitação - {} - {}>".format(self.id, self.nome)