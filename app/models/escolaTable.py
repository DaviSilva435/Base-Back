from app import db


class Escola(db.Model):
    __tablename__ = "escola"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cep = db.Column(db.String(10), nullable=False)
    endereco = db.Column(db.String(255), nullable=False)
    bairro = db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    cnpj = db.Column(db.String(20), nullable=False, unique=True)

    cidade_id = db.Column(db.Integer, db.ForeignKey('cidade.id'), nullable=False)

    Estudante = db.relationship('Estudante', backref='escola', lazy=True)

    # --------------------------------------------------------------------------------------------------#

    def __init__(self, nome, cep, endereco, bairro, cidade_id, telefone, email, cnpj):
        self.nome = nome
        self.cep = cep
        self.endereco = endereco
        self.bairro = bairro
        self.cidade_id = cidade_id
        self.telefone = telefone
        self.email = email
        self.cnpj = cnpj

    # --------------------------------------------------------------------------------------------------#

    def __repr__(self):
        return "<Escola - {} - {} - {} - {} - {} - {} - {} - {} - {}>".format(self.nome,self.cep,self.endereco,self.bairro,self.cidade_id,self.telefone, self.email,self.cnpj)