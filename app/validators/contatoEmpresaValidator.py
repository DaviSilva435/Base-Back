from app import FormValidator, Messages

class ContatoEmpresaValidator(FormValidator):

	def __init__(self, formData):
		super().__init__(formData)
		self.addFields()
		self.addConstraints()
		
#--------------------------------------------------------------------------------------------------#

	def addFields(self):
		super().addField("email", "Email", "email", required=True)
		super().addField("nome", "Nome", "text", required=True)
		super().addField("cargo", "Cargo", "text", required=True)
		super().addField("empresa_id", "Empresa", "integer", required=True)
		super().addField("principal", "Principal", "boolean", required=True)

#--------------------------------------------------------------------------------------------------#

	def addConstraints(self):
		super().addLengthConstraint("email", 5, 255)
		super().addLengthConstraint("nome", 2, 255)
		super().addLengthConstraint("cargo", 2, 255)
		