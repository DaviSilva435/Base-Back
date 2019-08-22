from app import FormValidator, Messages
from app import User

class UserValidator(FormValidator):

	def __init__(self, formData):
		super().__init__(formData)
		self.addFields()
		self.addConstraints()
		
#--------------------------------------------------------------------------------------------------#

	def addFields(self):
		super().addField("username", "Login", "text", required=True)
		super().addField("email", "Email", "email", required=True)

#--------------------------------------------------------------------------------------------------#

	def addConstraints(self):
		super().addLengthConstraint("username", 2, 255)
		super().addLengthConstraint("email", 5, 255)

#--------------------------------------------------------------------------------------------------#
	
	def validate(self):
		errors = super().validate()

		# avoid that both fields centro_estagio_id and empresa_id are set as None

		if 	(super().hasValue('centro_estagio_id') and super().hasValue('empresa_id')) or \
			(not super().hasValue('centro_estagio_id') and not super().hasValue('empresa_id')):
			
			errors['form'].append({
				'message': Messages.FORM_USER_EMP_CDE_ERROR
			})
			errors['has'] = True

		return errors

#--------------------------------------------------------------------------------------------------#

	def addPasswordField(self):
		super().addField("password", "Senha", "password", required=True)
		super().addLengthConstraint("password", 6, 255)

#--------------------------------------------------------------------------------------------------#
	
	def validateUsername(self):
		errors = {
			"fields": {},
			"form": [],
			"has" : False
		}

		if(super().hasValue('username')):
			user = User.query.filter(User.username == self.formData['username']).first()
			if user != None:
				errors['form'].append({
					'message': Messages.FORM_USER_ALREADY_EXISTS
				})
				errors['has'] = True				

		return errors