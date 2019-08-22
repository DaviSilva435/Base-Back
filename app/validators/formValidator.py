import re
import datetime
from app import Messages

class FormValidator():

	def __init__(self, formData):
		self.formData 				= formData
		self.fields 				= []
		self.inConstraints 			= {}
		self.lengthConstraints 		= {}

#------------------------------	--------------------------------------------------------------------#

	def addInConstraint(self, fieldName, values):
		self.inConstraints[fieldName] = values

#--------------------------------------------------------------------------------------------------#

	def addLengthConstraint(self, fieldName, minLength, maxLength):
		self.lengthConstraints[fieldName] = {"min": minLength, "max": maxLength}

#--------------------------------------------------------------------------------------------------#

	def addField(self, fieldName, fieldLabel, fieldType, required=False):	
		fld = {
			"type": fieldType,
			"name": fieldName,
			"label": fieldLabel,
			"required": required
		}

		self.fields.append(fld)

#--------------------------------------------------------------------------------------------------#

	def validate(self):
		
		errors = {
			"fields": {},
			"form": [],
			"has" : False
		}
		
		for field in self.fields:

			if not field['name'] in errors['fields']:

				if field['required']:

					if not self.hasValue(field['name']):
						errors['fields'][field['name']] = {
							"message": Messages.FORM_REQUIRED_ERROR
						}
						errors['has'] = True
						continue
				
				if field['name'] in self.lengthConstraints:
					lengthField = len(self.formData[field['name']])
					minConstr	= self.lengthConstraints[field['name']]['min']
					maxConstr	= self.lengthConstraints[field['name']]['max']

					if lengthField < minConstr or lengthField > maxConstr:
						errors['fields'][field['name']] = {
							"message": Messages.FORM_LENGTH_ERROR.format(field['label'], minConstr, maxConstr)
						}
						errors['has'] = True

				if field['name'] in self.inConstraints:
					
					if not self.formData[field['name']] in self.inConstraints:
						strValues = "("
						
						for key in self.inConstraints[field['name']]:
							strValues += "{} - {}, ".format(key, self.inConstraints[field['name']][key])
						
						strValues = strValues[:-2] + ")"
						errors['fields'][field['name']] = {
							"message": Messages.FORM_IN_ERROR.format(field['label'], strValues)
						}
						errors['has'] = True					

				if field['type'] == 'email':

					if not self.emailValidate(self.formData[field['name']]):
						errors['fields'][field['name']] = {
							"message": Messages.FORM_EMAIL_ERROR
						}
						errors['has'] = True

				if field['type'] == 'cpf':

					if not self.cpfValidate(self.formData[field['name']]):
						errors['fields'][field['name']] = {
							"message": Messages.FORM_CPF_ERROR
						}
						errors['has'] = True

				if field['type'] == 'cnpj':

					if not self.cnpjValidate(self.formData[field['name']]):
						errors['fields'][field['name']] = {
							"message": Messages.FORM_CNPJ_ERROR
						}
						errors['has'] = True

				if field['type'] == 'boolean':

					if not self.booleanValidate(self.formData[field['name']]):
						errors['fields'][field['name']] = {
							"message": Messages.FORM_BOOLEAN_ERROR
						}
						errors['has'] = True

				if field['type'] == 'date':

					if not self.dateValidate(self.formData[field['name']]):
						errors['fields'][field['name']] = {
							"message": Messages.FORM_DATE_ERROR
						}
						errors['has'] = True

				if field['type'] == 'year':
					date = self.formData[field['name']] + "-01-01"

					if not self.dateValidate(date):
						errors['fields'][field['name']] = {
							"message": Messages.FORM_DATE_ERROR
						}
						errors['has'] = True

				if field['type'] == 'month':
					date = "2010-" + self.formData[field['name']] + "-01"

					if not self.dateValidate(date):
						errors['fields'][field['name']] = {
							"message": Messages.FORM_DATE_ERROR
						}
						errors['has'] = True

				if field['type'] == 'time':
					if not self.timeValidate(self.formData[field['name']]):
						errors['fields'][field['name']] = {
							"message": Messages.FORM_TIME_ERROR
						}
						errors['has'] = True

				if field['type'] == 'timestamp':
					timestamp = str(self.formData[field['name']])
					timestamp = timestamp.split(' ')
					print(timestamp[0])
					print(timestamp[1])
					if not self.dateValidate(timestamp[0]):
						errors['fields'][field['name']] = {
							"message": Messages.FORM_DATE_ERROR
						}
						errors['has'] = True
					if not self.timeValidate(timestamp[1]):
						errors['fields'][field['name']] = {
                            "message": Messages.FORM_TIME_ERROR
                        }
						errors['has'] = True
		return errors

#--------------------------------------------------------------------------------------------------#

	def hasValue(self, fieldName):
		return \
			fieldName in self.formData and \
			self.formData[fieldName] != None and \
			self.formData[fieldName] != ""

#--------------------------------------------------------------------------------------------------#

	def emailValidate(self, email):
		if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email) != None:
			return True
		return False

#--------------------------------------------------------------------------------------------------#

	def dateValidate(self, date):
		try:
			datetime.datetime.strptime(date, '%Y-%m-%d')
			return True
		except ValueError:
			return False

	#--------------------------------------------------------------------------------------------------#

	def booleanValidate(self, boolean):
		return boolean == True or boolean == False

#--------------------------------------------------------------------------------------------------#

	def timeValidate(self, time):
		try:
			datetime.datetime.strptime(time, "%H:%M:%S")
			return True
		except ValueError:
			return False


# --------------------------------------------------------------------------------------------------#

	def cnpjValidate(self, cnpj):
		lista_validacao_um = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4 , 3, 2]
		lista_validacao_dois = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

		cnpj = cnpj.replace( "-", "" )
		cnpj = cnpj.replace( ".", "" )
		cnpj = cnpj.replace( "/", "" )

		verificadores = cnpj[-2:]
    	
		if len( cnpj ) != 14:
			return False
        
		soma 	= 0
		id 		= 0
        
		for numero in cnpj:
        
			try:
				lista_validacao_um[id]
			except:
				break

			soma += int( numero ) * int( lista_validacao_um[id] )
			id += 1

		soma = soma % 11

		if soma < 2:
			digito_um = 0
		else:
			digito_um = 11 - soma

		digito_um 	= str( digito_um )
		soma 		= 0
		id 			= 0

		for numero in cnpj:

			try:
				lista_validacao_dois[id]
			except:
				break
            
			soma += int( numero ) * int( lista_validacao_dois[id] )
			id += 1

		soma = soma % 11

		if soma < 2:
			digito_dois = 0
		else:
			digito_dois = 11 - soma

		digito_dois = str( digito_dois )
		return bool( verificadores == digito_um + digito_dois )

#--------------------------------------------------------------------------------------------------#

	def cpfValidate( self, cpf ):
		cpf_invalidos = [11*str(i) for i in range(10)]
		
		if cpf in cpf_invalidos:
			return False

		if not cpf.isdigit():
			cpf = cpf.replace( ".", "" )
			cpf = cpf.replace( "-", "" )

		if len( cpf ) < 11:
			return False

		if len( cpf ) > 11:
			return False

		selfcpf = [int( x ) for x in cpf]
		cpf 	= selfcpf[:9]

		while len( cpf ) < 11:
			r =  sum( [( len( cpf )+1-i )*v for i, v in [( x, cpf[x] ) for x in range( len( cpf ) )]] ) % 11

			if r > 1:
				f = 11 - r
			else:
				f = 0

			cpf.append( f )

		return bool( cpf == selfcpf )
