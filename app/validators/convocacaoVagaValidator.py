from app import FormValidator, Messages


class ConvocacaoVagaValidator(FormValidator):

    def __init__(self, formData):
        super().__init__(formData)
        self.addFields()
        self.addConstraints()

    # --------------------------------------------------------------------------------------------------#

    def addFields(self):
        super().addField("vaga_id", "Vaga", "integer", required=True)
        super().addField("contrato_empresa_id", "Contrato Empresa", "integer", required=True)
        super().addField("data_convocacao", "Data Convocacao", "date", required=True)
        super().addField("nome_solicitante", "Nome Solicitante", "text", required=True)
        super().addField("contato_solicitante", "Contato Solicitante", "text", required=True)
        super().addField("data_entrevista", "Data Entrevista", "timestamp", required=True)

    # --------------------------------------------------------------------------------------------------#

    def addConstraints(self):
        super().addLengthConstraint("nome_solicitante", 1, 255)
        super().addLengthConstraint("contato_solicitante", 1, 255)