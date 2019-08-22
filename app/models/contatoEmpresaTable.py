from app import db

class ContatoEmpresa(db.Model):
	__tablename__ = "contato_empresa"

	id = db.Column(db.BigInteger, primary_key = True)
	email = db.Column(db.String(255), nullable=False)
	nome = db.Column(db.String(255), nullable=False)
	cargo = db.Column(db.String(255), nullable=False)
	telefone = db.Column(db.String(20), nullable=True)
	celular = db.Column(db.String(20), nullable=True)
	principal = db.Column(db.Boolean, nullable=False)
	empresa_id = db.Column(db.BigInteger, db.ForeignKey('empresa.id'), nullable=False)
	
#--------------------------------------------------------------------------------------------------#

	def __init__(self, email, nome, cargo, telefone, celular, empresa_id, principal=False):
		self.email = email
		self.nome = nome
		self.cargo = cargo
		self.telefone = telefone
		self.celular = celular
		self.principal = principal
		self.empresa_id = empresa_id

#--------------------------------------------------------------------------------------------------#

	def __repr__(self):
		return "<ContatoEmpresa %r>" % self.nome
