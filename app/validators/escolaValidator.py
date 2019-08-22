from app import FormValidator

class EscolaValidator(FormValidator):

    def __init__(self, formData):
        super().__init__(formData)
        self.addFields()
        self.addConstraints()

#--------------------------------------------------------------------------------------------------#

    def addFields(self):
        super().addField("nome", "Nome", "text", required=True)
        super().addField("cep", "CEP", "text", required=True)
        super().addField("bairro", "Bairro", "text", required=True)
        super().addField("cidade_id", "Cidade", "integer", required=True)
        super().addField("telefone", "Telefone", "text", required=True)
        super().addField("email", "Email", "email", required=True)
        super().addField("cnpj", "CNPJ", "cnpj", required=True)

# --------------------------------------------------------------------------------------------------#

    def addConstraints(self):
        super().addLengthConstraint("nome", 1, 255)
        super().addLengthConstraint("cep", 8, 10)
        super().addLengthConstraint("endereco", 2, 255)
        super().addLengthConstraint("bairro", 2, 255)
        super().addLengthConstraint("telefone", 8, 30)
        super().addLengthConstraint("email", 2, 255)
        super().addLengthConstraint("cnpj", 2 , 20)
