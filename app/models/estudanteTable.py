from app import db

class Estudante(db.Model):
	__tablename__ = "estudante"
	__table_args__ = (
		db.UniqueConstraint('centro_estagio_id', 'cpf', name='unique_component_commit'),
	)

	id = db.Column(db.Integer, primary_key = True)
	nome = db.Column(db.String(255), nullable=False)

	sexo = db.Column(db.String(1), nullable=False)
	cep = db.Column(db.String(10), nullable=False)
	endereco = db.Column(db.String(255), nullable=False)
	bairro = db.Column(db.String(255), nullable=False)
	telefone = db.Column(db.String(30), nullable=False)
	celular = db.Column(db.String(30), nullable=False)
	email = db.Column(db.String(255), nullable=False)
	data_nascimento = db.Column(db.Date, nullable=False)
	rg = db.Column(db.String(20), nullable=False)
	cpf = db.Column(db.String(20), nullable=False)
	nome_pai = db.Column(db.String(255), nullable=False)
	nome_mae = db.Column(db.String(255), nullable=False)
	ano = db.Column(db.Integer, nullable=False)
	habilitacao = db.Column(db.Boolean, nullable=False)
	conducao_propria = db.Column(db.Boolean, nullable=False)

	cidade_id = db.Column(db.Integer, db.ForeignKey('cidade.id'), nullable=False)
	estado_civil_id = db.Column(db.Integer, db.ForeignKey('estado_civil.id'), nullable=False)
	curso_id = db.Column(db.Integer, db.ForeignKey('curso_estudante.id'), nullable=False)
	escola_id = db.Column(db.Integer, db.ForeignKey('escola.id'), nullable=False)
	periodo_curso_id = db.Column(db.Integer, db.ForeignKey('periodo_curso.id'), nullable=False)
	grau_instrucao_id = db.Column(db.Integer, db.ForeignKey('grau_instrucao.id'), nullable=False)
	categoria_habilitacao_id = db.Column(db.Integer, db.ForeignKey('categoria_habilitacao.id'), nullable=True)
	tipo_veiculo_id = db.Column(db.Integer, db.ForeignKey('tipo_veiculo.id'), nullable=True)
	centro_estagio_id = db.Column(db.BigInteger, db.ForeignKey('centro_estagio.id'), nullable=False)

	ApoliceEstudante = db.relationship('ApoliceEstudante', backref='estudante', lazy=True)
	ExperienciaProfissional = db.relationship('ExperienciaProfissionalEstudante', backref='estudante', lazy=True)
	ConhecimentoEstudante = db.relationship('ConhecimentoEstudante', backref='estudante', lazy=True)
	CursoAdicionalEstudante = db.relationship('CursoAdicionalEstudante', backref='estudante', lazy=True)
	EstudanteEncaminhado = db.relationship('EstudanteEncaminhado', backref='estudante', lazy=True)

#--------------------------------------------------------------------------------------------------#

	def __init__(self, nome, sexo, cep, endereco, bairro, cidade_id, telefone, celular, email, estado_civil_id,
				 data_nascimento, rg
				 , cpf, nome_pai, nome_mae, curso_id, escola_id, periodo_curso_id, grau_instrucao_id, ano, habilitacao,
				 categoria_habilitacao_id
				 , conducao_propria, tipo_veiculo_id, centro_estagio_id):
		self.nome = nome
		self.sexo = sexo
		self.cep = cep
		self.endereco = endereco
		self.bairro = bairro
		self.cidade_id = cidade_id
		self.telefone = telefone
		self.celular = celular
		self.email = email
		self.estado_civil_id = estado_civil_id
		self.data_nascimento = data_nascimento
		self.rg = rg
		self.cpf = cpf
		self.nome_pai = nome_pai
		self.nome_mae = nome_mae
		self.curso_id = curso_id
		self.escola_id = escola_id
		self.periodo_curso_id = periodo_curso_id
		self.grau_instrucao_id = grau_instrucao_id
		self.ano = ano
		self.habilitacao = habilitacao
		self.categoria_habilitacao_id = categoria_habilitacao_id
		self.conducao_propria = conducao_propria
		self.tipo_veiculo_id = tipo_veiculo_id
		self.centro_estagio_id = centro_estagio_id

	#--------------------------------------------------------------------------------------------------#

	def __repr__(self):
		return "<Estudante - {} - {} - {} - {} - {} - {} - {} - {} - {} - {} - {} - {} - {} - {} - {} - {} - {} - {} - {} - {} - {} - {} - {} - {} - {} - {}>".format(
				self.id, self.nome, self.sexo, self.cep, self.endereco, self.bairro, self.cidade_id, self.telefone, self.celular, self.email, self.estado_civil_id,
				 self.data_nascimento, self.rg
				 , self.cpf, self.nome_pai, self.nome_mae, self.curso_id, self.escola_id, self.periodo_curso_id, self.grau_instrucao_id, self.ano, self.habilitacao,
				 self.categoria_habilitacao_id
				 , self.conducao_propria, self.tipo_veiculo_id, self.centro_estagio_id)
