from app import FormValidator, Messages

class ApoliceEstudanteValidator(FormValidator):

	def __init__(self, formData):
		super().__init__(formData)
		self.addFields()
		
#--------------------------------------------------------------------------------------------------#

	# def addFields(self):
	# 	super().addField("seguradora_id", "Seguradora Id", "integer", required=True)
	# 	super().addField("numero", "Numero", "integer", required=True)
	# 	super().addField("centro_estagio_id", "Centro Estagio Id", "integer", required=True)
	# 	super().addField("mes", "Mes", "date", required=True)
	# 	super().addField("ano", "Ano", "date", required=True)
	# 	super().addField("estudante_id", "Estudante Id", "float", required=True)