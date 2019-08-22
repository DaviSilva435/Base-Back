from app import db


class CursoEstudante(db.Model):
    __tablename__ = "curso_estudante"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(400), nullable=False)

    CursoAdicionalEstudante = db.relationship('CursoAdicionalEstudante', backref='curso_estudante', lazy=True)
    Estudante = db.relationship('Estudante', backref='curso_estudante', lazy=True)
    Vaga = db.relationship('Vaga', backref='curso_estudante', lazy=True)

    # --------------------------------------------------------------------------------------------------#

    def __init__(self, nome):
        self.nome = nome

    # --------------------------------------------------------------------------------------------------#

    def __repr__(self):
        return "<CursoEstudante - {} - {}>".format(self.id, self.nome)