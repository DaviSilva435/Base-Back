from app import FormValidator, Messages

class EstudanteValidator(FormValidator):

    def __init__(self,formData):
        super().__init__(formData)
        self.addFields()
        self.addConstraints()

#----------------------------------------------------------------------------------------------------------------------#

    def addFields(self):
        super().addField("nome","Nome","text", required=True)
        super().addField("sexo", "Sexo", "text", required=True)
        super().addField("cep", "Cep", "text", required=True)
        super().addField("endereco", "Endereco", "text", required=True)
        super().addField("bairro", "Bairro", "text", required=True)
        super().addField("telefone","Telefone", "text", required=True)
        super().addField("celular", "Celular", "text", required=True)
        super().addField("email", "Email", "email", required=True)
        super().addField("data_nascimento", "Data_Nascimento", "date", required=True)
        super().addField("rg", "Rg", "text", required=True)
        super().addField("cpf", "CPF", "cpf", required=True)
        super().addField("nome_pai", "Nome_Pai", "text", required=True)
        super().addField("nome_mae", "Nome_Mae", "text", required=True)
        super().addField("ano", "Ano", "ano", required=True)
        super().addField("habilitacao", "Habilitacao", "boolean", required=True)
        super().addField("conducao_propria", "Conducao_Propria", "boolean", required=True)
        super().addField("cidade_id", "Cidade_id", "integer", required=True)
        super().addField("escola_id", "Escola_id", "integer", required=True)
        super().addField("periodo_curso_id", "Periodo_Curso_Id", "integer", required=True)
        super().addField("grau_instrucao_id", "Grau_Intrucao_Id", "integer", required=True)
        super().addField("categoria_habilitacao_id", "Categoria_Habilitacao_Id", "integer", required=True)
        super().addField("tipo_veiculo_id", "Tipo_Veiculo_Id", "integer", required=True)
        super().addField("centro_estagio_id", "Centro_Estagio_Id", "integer", required=True)

#----------------------------------------------------------------------------------------------------------------------#

    def addConstraints(self):
        super().addLengthConstraint("nome", 2, 255)
        super().addLengthConstraint("sexo", 1, 1)
        super().addLengthConstraint("cep", 8, 10)
        super().addLengthConstraint("endereco", 2, 255)
        super().addLengthConstraint("bairro", 2, 255)
        super().addLengthConstraint("telefone", 2, 30)
        super().addLengthConstraint("celular", 2, 30)
        super().addLengthConstraint("email", 5, 255)
        super().addLengthConstraint("rg", 2, 20)
        super().addLengthConstraint("cpf", 2, 20)
        super().addLengthConstraint("nome_pai", 2, 255)
        super().addLengthConstraint("nome_mae", 2, 255)