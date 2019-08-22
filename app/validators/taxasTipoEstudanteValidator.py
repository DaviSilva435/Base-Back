from app import FormValidator, Messages

class TaxasTipoEstudanteValidator(FormValidator):

	def __init__(self, formData):
		super().__init__(formData)
		self.addFields()
		
#--------------------------------------------------------------------------------------------------#

	def addFields(self):
		super().addField("tipo_estudante_id", "Tipo de Estudante", "integer", required=True)
		super().addField("contrato_empresa_id", "Contrato da Empresa", "integer", required=True)
		super().addField("valor", "Valor", "number", required=True)
		
