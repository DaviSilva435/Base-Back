
from app import FormValidator, Messages


class BeneficioVagaValidator(FormValidator):

    def __init__(self, formData):
        super().__init__(formData)
        self.addFields()

    # --------------------------------------------------------------------------------------------------#

    def addFields(self):
        super().addField("valor", "Valor", "float", required=True)
        super().addField("vaga_id", "Vaga", "integer", required=True)
        super().addField("beneficio_id", "Beneficio", "integer", required=True)

    # --------------------------------------------------------------------------------------------------#
