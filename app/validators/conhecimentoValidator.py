from app import FormValidator, Messages


class ConhecimentoValidator(FormValidator):

    def __init__(self, formData):
        super().__init__(formData)
        self.addFields()
        self.addConstraints()

    # --------------------------------------------------------------------------------------------------#

    def addFields(self):
        super().addField("nome", "Nome", "text", required=True)
        super().addField("tipo_conhecimento_id", "Tipo de Conhecimento", "integer", required=True)

    # --------------------------------------------------------------------------------------------------#

    def addConstraints(self):
        super().addLengthConstraint("nome", 1, 255)