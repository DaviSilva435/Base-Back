from sqlalchemy import or_, and_
from app import FormValidator, Messages
from app import ContratoEmpresa

class ContratoEmpresaValidator(FormValidator):

	def __init__(self, formData):
		super().__init__(formData)
		self.addFields()
		
#--------------------------------------------------------------------------------------------------#

	def addFields(self):
		super().addField("empresa_id", "Empresa", "integer", required=True)
		super().addField("centro_estagio_id", "Centro de Estágio", "integer", required=True)
		super().addField("inicio", "Início", "date", required=True)
		super().addField("fim", "Fim", "date", required=True)

#--------------------------------------------------------------------------------------------------#

	def validateDuplicationContract(self):
		errors = {
			"fields": {},
			"form": [],
			"has" : False
		}

		# avoid that exists more than one contract between the same employee and center in the same period

		if not errors['has']:
			inicio 				= self.formData['inicio']
			fim    				= self.formData['fim']
			empresa_id 			= self.formData['empresa_id']
			centro_estagio_id 	= self.formData['centro_estagio_id']

			contrato = ContratoEmpresa.query.filter(\
				and_( \
					ContratoEmpresa.empresa_id == empresa_id,
					ContratoEmpresa.centro_estagio_id == centro_estagio_id,
					or_( \
						and_(ContratoEmpresa.inicio <= inicio, ContratoEmpresa.fim >= fim), 	\
						and_(ContratoEmpresa.inicio >= inicio, ContratoEmpresa.fim <= fim), 	\
						and_(ContratoEmpresa.inicio <= inicio, ContratoEmpresa.fim >= inicio), 	\
						and_(ContratoEmpresa.inicio <= fim   , ContratoEmpresa.fim >= fim) 		\
					)
				)
			).first()

			if contrato != None:
				errors['form'].append({
					'message': Messages.FORM_CONTRACT_EMPLOYEE_ALREADY_EXISTS
				})
				errors['has'] = True

		return errors

#--------------------------------------------------------------------------------------------------#

	def validateDuplicationContractSameId(self, contrato_empresa_id):
		errors = {
			"fields": {},
			"form": [],
			"has" : False
		}

		# avoid that exists more than one contract between the same employee and center in the same period

		if not errors['has']:
			inicio 				= self.formData['inicio']
			fim    				= self.formData['fim']
			empresa_id 			= self.formData['empresa_id']
			centro_estagio_id 	= self.formData['centro_estagio_id']

			contrato = ContratoEmpresa.query.filter(\
				and_( \
					ContratoEmpresa.empresa_id == empresa_id,
					ContratoEmpresa.centro_estagio_id == centro_estagio_id,
					or_( \
						and_(ContratoEmpresa.inicio <= inicio, ContratoEmpresa.fim >= fim), 	\
						and_(ContratoEmpresa.inicio >= inicio, ContratoEmpresa.fim <= fim), 	\
						and_(ContratoEmpresa.inicio <= inicio, ContratoEmpresa.fim >= inicio), 	\
						and_(ContratoEmpresa.inicio <= fim   , ContratoEmpresa.fim >= fim) 		\
					),
					ContratoEmpresa.id != contrato_empresa_id
				)
			).first()

			if contrato != None:
				errors['form'].append({
					'message': Messages.FORM_CONTRACT_EMPLOYEE_ALREADY_EXISTS
				})
				errors['has'] = True

		return errors
