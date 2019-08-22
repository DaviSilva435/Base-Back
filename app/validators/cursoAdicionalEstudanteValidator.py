from app import FormValidator, Messages


class CursoAdicionalEstudanteValidator(FormValidator):

    def __init__(self, formData):
        super().__init__(formData)
        self.addFields()

    # --------------------------------------------------------------------------------------------------#

    def addFields(self):
        super().addField("curso_id", "Curso ID", "integer", required=True)
        super().addField("estudante_id", "Estudante ID", "integer", required=True)
        super().addField("carga_horaria", "Carga Horária", "integer", required=True)

    # --------------------------------------------------------------------------------------------------#
