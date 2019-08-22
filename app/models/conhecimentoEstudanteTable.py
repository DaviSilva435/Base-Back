from app import db

class ConhecimentoEstudante(db.Model):
	__tablename__ = "conhecimento_estudante"

	valor = db.Column(db.Boolean, nullable=False)
	conhecimento_id = db.Column(db.Integer, db.ForeignKey('conhecimento.id'), primary_key=True, nullable=False)
	estudante_id = db.Column(db.Integer, db.ForeignKey('estudante.id'), primary_key=True, nullable=False)


#--------------------------------------------------------------------------------------------------#

	def __init__(self, valor, estudante_id, conhecimento_id):
		self.valor = valor
		self.estudante_id = estudante_id
		self.conhecimento_id = conhecimento_id

#--------------------------------------------------------------------------------------------------#

	def __repr__(self):
		return "<ConhecimentoEstudante - {} - {} - {}>".format(self.valor, self.estudante_id, self.conhecimento_id)
