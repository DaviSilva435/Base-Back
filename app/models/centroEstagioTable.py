from app import db

class CentroEstagio(db.Model):
	__tablename__ = "centro_estagio"

	id = db.Column(db.BigInteger, primary_key = True)
	razao_social = db.Column(db.String(255), nullable=False)
	nome_fantasia = db.Column(db.String(255), nullable=False)
	cnpj = db.Column(db.String(20), nullable=False)
	email = db.Column(db.String(255), nullable=False)
	matriz_id  = db.Column(db.Integer, db.ForeignKey('centro_estagio.id'), nullable=True)

	filiais = db.relationship("CentroEstagio", backref=db.backref('matriz', remote_side=[id]))
	usuarios = db.relationship('User', backref='centro_estagio', lazy=True)
	contratos_empresa = db.relationship('ContratoEmpresa', backref='centro_estagio', lazy=True)
	apolices = db.relationship('Apolice', backref='centro_estagio', lazy=True)
	apolicesMesAno = db.relationship('ApoliceMesAno', backref='centro_estagio', lazy=True)
	ApoliceEstudanteConsolidado = db.relationship('ApoliceEstudanteConsolidado', backref='centro_estagio', lazy=True)
	ApoliceEstudante = db.relationship('ApoliceEstudante', backref='centro_estagio', lazy=True)

#--------------------------------------------------------------------------------------------------#

	def __init__(self, razao_social, nome_fantasia, cnpj, email, matriz_id=None):
		self.razao_social = razao_social
		self.nome_fantasia = nome_fantasia
		self.cnpj = cnpj
		self.email = email
		self.matriz_id = matriz_id

#--------------------------------------------------------------------------------------------------#

	def __repr__(self):
		return "<CentroEstagio %r>" % self.id
