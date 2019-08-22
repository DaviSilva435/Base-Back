from app import db

class DiasVaga(db.Model):
    __tablename__= 'dias_vaga'
    vaga_id = db.Column(db.BigInteger, db.ForeignKey('vaga.id'), primary_key=True)
    id_dia = db.Column(db.Integer, primary_key=True)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fim = db.Column(db.Time, nullable=False)

#---------------------------------------------------------------------------------#

    def __init__(self, vaga_id, id_dia, hora_inicio, hora_fim):
        self.vaga_id = vaga_id
        self.id_dia = id_dia
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim

#---------------------------------------------------------------------------------#

    def __repr__(self):
        return "<Dias Vaga - {} - {} - {} - {}>".format(self.vaga_id, self.id_dia, self.hora_inicio, self.hora_fim)