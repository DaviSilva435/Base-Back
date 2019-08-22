from app import FormValidator, Messages
from app import User

from werkzeug.security 	import check_password_hash

class AuthValidator(FormValidator):

	def __init__(self, formData):
		super().__init__(formData)
		self.addFields()
		
#--------------------------------------------------------------------------------------------------#

	def addFields(self):
		super().addField("username", "Login", "text", required=True)
		super().addField("password", "Senha", "text", required=True)

#--------------------------------------------------------------------------------------------------#
	
	def validate(self):
		errors = super().validate()
		
		if super().hasValue('username') and super().hasValue('password'):

			pusername = self.formData['username'];
			ppassword = self.formData['password'];
			
			# verify if the username exists in database
			user = User.query.filter(User.username == pusername).first();

			if not user:
				errors['form'].append({
					'message': Messages.AUTH_USER_NOT_FOUND
				})
				errors['has'] = True
			elif not check_password_hash(user.password, ppassword):
				errors['form'].append({
					'message': Messages.AUTH_USER_PASS_ERROR
				})
				errors['has'] = True

			errors['form'].append({
				'message': Messages.AUTH_USER_NOT_FOUND
			})

			return errors
