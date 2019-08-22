from app import FormValidator, Messages

class CidadeValidator(FormValidator):

    def __init__(self, formData):
        super().__init__(formData)
        self.addFields()
        self.addConstraints()

    # --------------------------------------------------------------------------------------------------#

    def addFields(self):
        super().addField("nome", "Nome", "text", required=True)
        super().addField("ibge", "IBGE", "text", required=True)
        super().addField("uf_id", "UF", "integer", required=True)

    # --------------------------------------------------------------------------------------------------#

    def addConstraints(self):
        super().addLengthConstraint("nome", 1, 255)
        super().addLengthConstraint("ibge", 1, 20)

