from app import FormValidator, Messages


class EstudanteEncaminhadoValidator(FormValidator):

    def __init__(self, formData):
        super().__init__(formData)
        self.addFields()

    # --------------------------------------------------------------------------------------------------#

    def addFields(self):
        super().addField("estudante_id", "Estudante", "integer", required=True)
        super().addField("convocacao_id", "Convocacao", "integer", required=True)
        super().addField("contratado", "Contratado", "boolean", required=True)

    # --------------------------------------------------------------------------------------------------#
