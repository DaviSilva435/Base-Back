from app import db

class CursoAdicionalEstudante(db.Model):
	__tablename__ = "curso_adicional_estudante"

	carga_horaria = db.Column(db.Integer, nullable=False)
	curso_id = db.Column(db.Integer, db.ForeignKey('curso_estudante.id'), primary_key=True, nullable=False)
	estudante_id = db.Column(db.Integer, db.ForeignKey('estudante.id'), primary_key=True, nullable=False)

#--------------------------------------------------------------------------------------------------#

	def __init__(self, curso_id, estudante_id, carga_horaria):
		self.curso_id = curso_id
		self.estudante_id = estudante_id
		self.carga_horaria = carga_horaria

#--------------------------------------------------------------------------------------------------#

	def __repr__(self):
		return "<ConhecimentoAdicionalEstudante - {} - {} - {}>".format(self.carga_horaria, self.curso_id, self.estudante_id)