from app import db

class TaxasTipoEstudante(db.Model):
	__tablename__ = "taxas_tipo_estudante"

	tipo_estudante_id = db.Column(db.Integer, db.ForeignKey('tipo_estudante.id'), primary_key=True)
	contrato_empresa_id = db.Column(db.BigInteger, db.ForeignKey('contrato_empresa.id'), primary_key=True)
	valor = db.Column(db.Float, nullable=False)

#--------------------------------------------------------------------------------------------------#

	def __init__(self, tipo_estudante_id, contrato_empresa_id, valor):
		self.tipo_estudante_id = tipo_estudante_id
		self.contrato_empresa_id = contrato_empresa_id
		self.valor = valor

#--------------------------------------------------------------------------------------------------#

	def __repr__(self):
		return "<TaxasTipoEstudante - estudante:{}/empresa:{}>".format(self.tipo_estudante_id, self.contrato_empresa_id)
