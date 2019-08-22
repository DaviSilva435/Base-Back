from app import db

class ContratoEmpresa(db.Model):
	__tablename__ = "contrato_empresa"

	id = db.Column(db.BigInteger, primary_key = True)
	inicio = db.Column(db.Date, nullable = False)
	fim = db.Column(db.Date, nullable = False)
	empresa_id = db.Column(db.BigInteger, db.ForeignKey('empresa.id'), nullable=False)
	centro_estagio_id = db.Column(db.BigInteger, db.ForeignKey('centro_estagio.id'), nullable=False)

	taxas = db.relationship('TaxasTipoEstudante', backref='contrato_empresa', lazy=True)
	Vaga = db.relationship('Vaga', backref='contrato_empresa', lazy=True)
	convocacao_vaga = db.relationship('ConvocacaoVaga', backref='contrato_empresa', lazy=True)

#--------------------------------------------------------------------------------------------------#

	def __init__(self, inicio, fim, empresa_id, centro_estagio_id):
		self.inicio = inicio
		self.fim = fim
		self.empresa_id = empresa_id
		self.centro_estagio_id = centro_estagio_id

#--------------------------------------------------------------------------------------------------#

	def __repr__(self):
		return "<ContratoEmpresa %r>" % self.id
