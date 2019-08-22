from app import db

class Cidade(db.Model):
	__tablename__ = "cidade"

	id = db.Column(db.Integer, primary_key = True)
	nome = db.Column(db.String(255), nullable=False)
	ibge = db.Column(db.String(255), nullable=False, unique=True)
	uf_id = db.Column(db.Integer, db.ForeignKey('uf.id'), nullable=False)
	
	empresas = db.relationship('Empresa', backref='cidade', lazy=True)
	escolas = db.relationship('Escola', backref='cidade', lazy=True)
	estudantes = db.relationship('Estudante', backref='cidade', lazy=True)

#--------------------------------------------------------------------------------------------------#

	def __init__(self, nome, ibge, uf_id):
		self.nome 		= nome
		self.ibge 		= ibge
		self.uf_id 		= uf_id

#--------------------------------------------------------------------------------------------------#

	def __repr__(self):
		return "<Cidade {} - {} - {} - {}>".format(self.id, self.nome, self.ibge, self.uf_id)
