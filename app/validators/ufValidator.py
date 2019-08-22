from app import FormValidator, Messages

class UfValidator(FormValidator):

	def __init__(self, formData):
		super().__init__(formData)
		self.addFields()
		self.addConstraints()
#--------------------------------------------------------------------------------------------------#

	def addFields(self):
		super().addField("nome", "Nome", "text", required=True)
		super().addField("sigla", "Sigla", "text", required=True)

# --------------------------------------------------------------------------------------------------#

	def addConstraints(self):
		super().addLengthConstraint("nome", 1, 255)
		super().addLengthConstraint("sigla", 2, 2)
