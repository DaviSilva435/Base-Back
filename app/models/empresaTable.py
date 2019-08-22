from app import db

class Empresa(db.Model):
	__tablename__ = "empresa"

	id = db.Column(db.BigInteger, primary_key = True)
	razao_social = db.Column(db.String(255), nullable=False)
	nome_fantasia = db.Column(db.String(255), nullable=False)
	endereco = db.Column(db.String(255), nullable=False)
	bairro = db.Column(db.String(255), nullable=False)
	cep = db.Column(db.String(20), nullable=False)
	fone = db.Column(db.String(20), nullable=False)
	cnpj = db.Column(db.String(20), nullable=False)
	complemento = db.Column(db.String(255), nullable=True)
	cidade_id 	 = db.Column(db.Integer, db.ForeignKey('cidade.id'), nullable=False)

	usuarios = db.relationship('User', backref='empresa', lazy=True)
	contatos = db.relationship('ContatoEmpresa', backref='empresa', lazy=True)
	contratos = db.relationship('ContratoEmpresa', backref='empresa', lazy=True)

#--------------------------------------------------------------------------------------------------#

	def __init__(self, razao_social, nome_fantasia, endereco, bairro, \
				cep, fone, cnpj, complemento, cidade_id):
		self.razao_social = razao_social
		self.nome_fantasia = nome_fantasia
		self.endereco = endereco
		self.bairro = bairro
		self.cep = cep
		self.fone = fone
		self.cnpj = cnpj 
		self.complemento = complemento
		self.cidade_id = cidade_id

#--------------------------------------------------------------------------------------------------#

	def __repr__(self):
		return "<Empresa %r>" % self.id
