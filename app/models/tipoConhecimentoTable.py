from app import db

class TipoConhecimento(db.Model):
	__tablename__ = "tipo_conhecimento"

	id = db.Column(db.Integer, primary_key = True)
	nome = db.Column(db.String(400), nullable=False)

	conhecimentos = db.relationship('Conhecimento', backref='tipo_conhecimento', lazy=True)

#--------------------------------------------------------------------------------------------------#

	def __init__(self, nome):
		self.nome = nome

#--------------------------------------------------------------------------------------------------#

	def __repr__(self):
		return "<TipoConhecimento - {} - {}>".format(self.id, self.nome)