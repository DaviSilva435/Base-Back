from app import db

class ExperienciaProfissionalEstudante(db.Model):
	__tablename__ = "experiencia_profissional_estudante"

	cbo_id  = db.Column(db.Integer, db.ForeignKey('cbo.id'), primary_key = True, nullable=False)
	estudante_id  = db.Column(db.Integer, db.ForeignKey('estudante.id'), primary_key = True, nullable=False)

	duracao = db.Column(db.Integer, nullable = False)

#--------------------------------------------------------------------------------------------------#

	def __init__(self, cbo_id, estudante_id, duracao ):
		self.cbo_id = cbo_id
		self.estudante_id = estudante_id
		self.duracao = duracao

#--------------------------------------------------------------------------------------------------#

	def __repr__(self):
		return "<ExperienciaProfissionalEstudante - {} - {} - {}>".format(self.cbo_id, self.estudante_id, self.duracao)
