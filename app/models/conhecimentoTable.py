from app import db

class Conhecimento(db.Model):
	__tablename__ = "conhecimento"

	id = db.Column(db.Integer, primary_key = True)
	nome = db.Column(db.String(400), nullable=False)

	tipo_conhecimento_id = db.Column(db.Integer, db.ForeignKey('tipo_conhecimento.id'), nullable=False)

	conhecimento_estudante = db.relationship('ConhecimentoEstudante', backref='conhecimento', lazy=True)

#--------------------------------------------------------------------------------------------------#

	def __init__(self, nome, tipo_conhecimento_id):
		self.nome = nome
		self.tipo_conhecimento_id = tipo_conhecimento_id

#--------------------------------------------------------------------------------------------------#

	def __repr__(self):
		return "<Conhecimento - {} - {} - {}>".format(self.id, self.nome, self.tipo_conhecimento_id)
