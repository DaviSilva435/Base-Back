from app import db

class TipoVeiculo(db.Model):
	__tablename__ = "tipo_veiculo"

	id = db.Column(db.Integer, primary_key = True)
	nome = db.Column(db.String(255), nullable=False)

	Estudante = db.relationship('Estudante', backref='tipo_veiculo', lazy=True)

#--------------------------------------------------------------------------------------------------#

	def __init__(self, nome):
		self.nome = nome

#--------------------------------------------------------------------------------------------------#

	def __repr__(self):
		return "<TipoVeiculo - {} - {}>".format(self.id, self.nome)
