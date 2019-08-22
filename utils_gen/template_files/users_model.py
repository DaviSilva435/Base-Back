from app import db

class User(db.Model):
	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String, unique=True, nullable=False)
	password = db.Column(db.String, nullable=False)
	role_id  = db.Column(db.Integer, db.ForeignKey('roles.id'),
        nullable=False)

	
	
	def __init__(self, username, password, role_id):
		self.username 	= username
		self.password 	= password
		self.role_id 	= role_id

	def __repr__(self):
		return "<User %r>" % self.username
