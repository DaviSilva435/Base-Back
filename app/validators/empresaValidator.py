from app import FormValidator, Messages

class EmpresaValidator(FormValidator):

	def __init__(self, formData):
		super().__init__(formData)
		self.addFields()
		self.addConstraints()
		
#--------------------------------------------------------------------------------------------------#

	def addFields(self):
		super().addField("razao_social", "Razão Social", "text", required=True)
		super().addField("nome_fantasia", "Nome de Fantasia", "text", required=True)
		super().addField("endereco", "Endereço", "text", required=True)
		super().addField("bairro", "Bairro", "text", required=True)
		super().addField("cep", "CEP", "text", required=True)
		super().addField("fone", "Telefone", "text", required=True)
		super().addField("cnpj", "CNPJ", "cnpj", required=True)
		super().addField("cidade_id", "Cidade", "integer", required=True)

#--------------------------------------------------------------------------------------------------#

	def addConstraints(self):
		super().addLengthConstraint("razao_social", 2, 255)
		super().addLengthConstraint("nome_fantasia", 1, 255)
		super().addLengthConstraint("endereco", 2, 255)
		super().addLengthConstraint("bairro", 2, 255)
		