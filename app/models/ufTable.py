from app import db

class Uf(db.Model):
	__tablename__ = "uf"

	id = db.Column(db.Integer, primary_key = True)
	nome = db.Column(db.String(255), nullable=False)
	sigla = db.Column(db.String(2), nullable=False, unique=True)

	cidades = db.relationship('Cidade', backref='uf', lazy=True)

#--------------------------------------------------------------------------------------------------#
	
	def __init__(self, nome, sigla):
		self.nome 		= nome
		self.sigla 		= sigla

#--------------------------------------------------------------------------------------------------#
		
	def __repr__(self):
		return "<Uf {} - {} - {}>".format(self.id, self.nome, self.sigla)
