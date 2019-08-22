from app import FormValidator, Messages

class ApoliceValidator(FormValidator):

	def __init__(self, formData):
		super().__init__(formData)
		self.addFields()
		
#--------------------------------------------------------------------------------------------------#

	def addFields(self):
		super().addField("seguradora_id", "Seguradora Id", "integer", required=True)
		super().addField("numero", "Numero", "integer", required=True)
		super().addField("centro_estagio_id", "Centro Estagio Id", "integer", required=True)
		super().addField("inicio", "Inicio", "date", required=True)
		super().addField("fim", "Fim", "date", required=True)
		super().addField("valor", "Centro Estagio Id", "float", required=True)
		super().addField("quantidade", "Centro Estagio Id", "integer", required=True)


	#PARTE ApoliceTable
	#seguradora_id = db.Column(db.Integer, db.ForeignKey('seguradora.id'), nullable=False, primary_key=True)
	#numero = db.Column(db.BigInteger, nullable=False, primary_key=True)
	#centro_estagio_id = db.Column(db.BigInteger, db.ForeignKey('centro_estagio.id'), nullable=False, primary_key=True)
	#inicio = db.Column(db.Date, nullable=False)
	#fim = db.Column(db.Date, nullable=False)
	#valor = db.Column(db.Float, nullable=False)
	#quantidade = db.Column(db.BigInteger, nullable=False)
