from app import db

class Apolice(db.Model):
	__tablename__ = "apolice"

	seguradora_id = db.Column(db.Integer, db.ForeignKey('seguradora.id'), nullable=False, primary_key=True)
	numero = db.Column(db.BigInteger, nullable=False, primary_key=True)
	centro_estagio_id = db.Column(db.BigInteger, db.ForeignKey('centro_estagio.id'), nullable=False, primary_key=True)
	inicio = db.Column(db.Date, nullable=False)
	fim = db.Column(db.Date, nullable=False)
	valor = db.Column(db.Float, nullable=False)
	quantidade = db.Column(db.BigInteger, nullable=False)

#--------------------------------------------------------------------------------------------------#

	def __init__(self, seguradora_id, numero, centro_estagio_id, inicio, fim, valor, quantidade):
		self.seguradora_id = seguradora_id
		self.numero = numero
		self.centro_estagio_id = centro_estagio_id
		self.inicio = inicio
		self.fim = fim
		self.valor = valor
		self.quantidade = quantidade

#--------------------------------------------------------------------------------------------------#

	def __repr__(self):
		return "<Apolice %r>" % self.numero
