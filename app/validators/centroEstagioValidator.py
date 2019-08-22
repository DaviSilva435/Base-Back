from app import FormValidator, Messages

class CentroEstagioValidator(FormValidator):

	def __init__(self, formData):
		super().__init__(formData)
		self.addFields()
		self.addConstraints()
		
#--------------------------------------------------------------------------------------------------#

	def addFields(self):
		super().addField("razao_social", "Razão Social", "text", required=True)
		super().addField("nome_fantasia", "Nome de Fantasia", "text", required=True)
		super().addField("cnpj", "CNPJ", "cnpj", required=True)
		super().addField("email", "Email", "email", required=True)

#--------------------------------------------------------------------------------------------------#

	def addConstraints(self):
		super().addLengthConstraint("razao_social", 2, 255)
		super().addLengthConstraint("nome_fantasia", 1, 255)
		super().addLengthConstraint("email", 5, 255)
