from app import FormValidator, Messages


class ConhecimentoEstudanteValidator(FormValidator):

    def __init__(self, formData):
        super().__init__(formData)
        self.addFields()

    # --------------------------------------------------------------------------------------------------#

    def addFields(self):
        super().addField("estudante_id", "Estudante", "integer", required=True)
        super().addField("conhecimento_id", "Conhecimento", "integer", required=True)
        super().addField("valor", "Valor", "boolean", required=True)