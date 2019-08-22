from app import FormValidator, Messages


class ExperienciaProfissionalEstudanteValidator(FormValidator):

    def __init__(self, formData):
        super().__init__(formData)
        self.addFields()

    # --------------------------------------------------------------------------------------------------#

    def addFields(self):
        super().addField("estudante_id", "Estudante", "integer", required=True)
        super().addField("cbo_id", "CBO", "integer", required=True)
        super().addField("duracao", "Duração", "integer", required=True)