from flask import Flask, request, jsonify
from models import db, Aluno

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alunos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Inicializar o banco de dados
@app.before_first_request
def create_tables():
    db.create_all()

# Rota para obter todos os alunos
@app.route('/alunos', methods=['GET'])
def get_alunos():
    alunos = Aluno.query.all()
    output = [{"id": aluno.id, "nome": aluno.nome, "idade": aluno.idade, "curso": aluno.curso} for aluno in alunos]
    return jsonify(output)

# Rota para adicionar um novo aluno
@app.route('/alunos', methods=['POST'])
def add_aluno():
    data = request.get_json()
    novo_aluno = Aluno(nome=data['nome'], idade=data['idade'], curso=data['curso'])
    db.session.add(novo_aluno)
    db.session.commit()
    return jsonify({"message": "Aluno adicionado com sucesso!"})

# Rota para consultar um aluno pelo ID
@app.route('/alunos/<int:id>', methods=['GET'])
def get_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    return jsonify({"id": aluno.id, "nome": aluno.nome, "idade": aluno.idade, "curso": aluno.curso})

# Rota para excluir um aluno pelo ID
@app.route('/alunos/<int:id>', methods=['DELETE'])
def delete_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    db.session.delete(aluno)
    db.session.commit()
    return jsonify({"message": "Aluno excluído com sucesso!"})

if __name__ == '__main__':
   app.run(debug=True)
