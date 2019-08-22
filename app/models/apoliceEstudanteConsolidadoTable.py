from app import db

class ApoliceEstudanteConsolidado(db.Model):
	__tablename__ = "apolice_estudante_consolidado"

	seguradora_id = db.Column(db.Integer, db.ForeignKey('seguradora.id'), nullable=False, primary_key=True)
	numero = db.Column(db.BigInteger, nullable=False, primary_key=True)
	centro_estagio_id = db.Column(db.BigInteger, db.ForeignKey('centro_estagio.id'), nullable=False, primary_key=True)
	mes = db.Column(db.Integer, nullable=False, primary_key=True)
	ano = db.Column(db.Integer, nullable=False, primary_key=True)
	registro = db.Column(db.LargeBinary, nullable=False)

#--------------------------------------------------------------------------------------------------#

	def __init__(self, seguradora_id, numero, centro_estagio_id, mes, ano, registro):
		self.seguradora_id = seguradora_id
		self.numero = numero
		self.centro_estagio_id = centro_estagio_id
		self.mes = mes
		self.ano = ano
		self.registro = registro

#--------------------------------------------------------------------------------------------------#

	def __repr__(self):
		return "<ApoliceEstudanteConsolidado %r>" % self.numero
	