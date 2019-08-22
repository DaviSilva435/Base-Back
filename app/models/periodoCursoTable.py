from app import db

class PeriodoCurso(db.Model):
	__tablename__ = "periodo_curso"

	id = db.Column(db.Integer, primary_key = True)
	nome = db.Column(db.String(255), nullable=False)

	Estudante = db.relationship('Estudante', backref='periodo_curso', lazy=True)

#--------------------------------------------------------------------------------------------------#

	def __init__(self, nome):
		self.nome = nome

#--------------------------------------------------------------------------------------------------#

	def __repr__(self):
		return "<PeriodoCurso - {} - {}>".format(self.id, self.nome)
