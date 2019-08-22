from app import FormValidator, Messages


class DiasVagaValidator(FormValidator):

    def __init__(self, formData):
        super().__init__(formData)
        self.addFields()
        self.addConstraints()

    # --------------------------------------------------------------------------------------------------#

    def addFields(self):
        super().addField("vaga_id", "Vaga", "integer", required=True)
        super().addField("id_dia", "ID Dia", "integer", required=True)
        super().addField("hora_inicio", "Hora Inicio", "time", required=True)
        super().addField("hora_fim", "Hora Fim", "time", required=True)

    # --------------------------------------------------------------------------------------------------#

    def addConstraints(self):
        super().addLengthConstraint("hora_inicio", 6, 8)
        super().addLengthConstraint("hora_fim", 6, 8)