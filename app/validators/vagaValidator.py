from app import FormValidator, Messages


class VagaValidator(FormValidator):

    def __init__(self, formData):
        super().__init__(formData)
        self.addFields()
        self.addConstraints()

    # --------------------------------------------------------------------------------------------------#

    def addFields(self):
        super().addField("contrato_empresa_id", "Contrato Empresa", "integer", required=True)
        super().addField("quantidade_vagas", "Quantidade Vagas", "integer", required=True)
        super().addField("ano", "Ano", "year", required=True)
        super().addField("semestre", "Semestre", "integer", required=True)
        super().addField("sexo_preferencial", "Sexo", "text", required=True)
        super().addField("conhecimento_especifico", "Conhecimento Especifico", "text", required=False)
        super().addField("atividades_desenvolvidas", "Atividades Desenvolvidas", "text", required=True)
        super().addField("responsavel_estagiario", "Responsavel Estagiario", "text", required=True)
        super().addField("email_responsavel", "Email Responsavel", "email", required=True)
        super().addField("endereco_estagiario", "Endereco Estagiario", "text", required=True)
        super().addField("valor_bolsa", "Valor Bolsa", "float", required=True)
        super().addField("observacao", "Observacao", "text", required=False)

    # --------------------------------------------------------------------------------------------------#

    def addConstraints(self):
        super().addLengthConstraint("sexo_preferencial", 1, 1)
        super().addLengthConstraint("conhecimento_especifico", 1, 50000)
        super().addLengthConstraint("atividades_desenvolvidas", 1, 50000)
        super().addLengthConstraint("responsavel_estagiario", 1, 255)
        super().addLengthConstraint("email_responsavel", 1, 255)
        super().addLengthConstraint("endereco_estagiario", 1, 255)
        super().addLengthConstraint("observacao", 0, 50000)
