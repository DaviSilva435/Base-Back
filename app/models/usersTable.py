from app import db
from sqlalchemy.orm import validates

class User(db.Model):
	__tablename__ = "users"

	id = db.Column(db.BigInteger, primary_key = True)
	username = db.Column(db.String(255), unique=True, nullable=False)
	password = db.Column(db.String(255), nullable=False)
	email	 = db.Column(db.String(255), nullable=True)
	role_id  = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
	empresa_id = db.Column(db.BigInteger, db.ForeignKey('empresa.id'), nullable=True)
	centro_estagio_id = db.Column(db.BigInteger, db.ForeignKey('centro_estagio.id'), nullable=True)

#--------------------------------------------------------------------------------------------------#
	
	def __init__(self, username, password, email, role_id, empresa_id, centro_estagio_id):
		self.username = username
		self.password = password
		self.email = email
		self.role_id = role_id
		self.empresa_id = empresa_id
		self.centro_estagio_id = centro_estagio_id

#--------------------------------------------------------------------------------------------------#

	def __repr__(self):
		return "<User %r>" % self.username