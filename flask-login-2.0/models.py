from flask_login import UserMixin
import sqlite3 

BANCO = 'database.db'

def obter_conexao():
    conn = sqlite3.connect(BANCO)
    conn.row_factory = sqlite3.Row 
    return conn 

# classe python - Modelo (acessa o banco)
class User(UserMixin):
    id : str 
    def __init__(self, matricula, email, senha, id=None):
        self.matricula = matricula
        self.email = email
        self.senha = senha 
        self.id = id

    @classmethod 
    def get(cls, id):
        conexao = obter_conexao()
        SELECT = 'SELECT * FROM usuarios WHERE id=?'
        dados = conexao.execute(SELECT, (id,)).fetchone()
        conexao.close()
        if dados: 
            return cls(dados['matricula'], dados['email'], dados['senha'], dados['id'])
        return None
    
    @classmethod
    def get_by_email(cls, email):
        conexao = obter_conexao()
        SELECT = 'SELECT * FROM usuarios WHERE email=?'
        dados = conexao.execute(SELECT, (email,)).fetchone()
        conexao.close()

        if dados:
            return cls(dados['matricula'], dados['email'], dados['senha'], dados['id'])
        return None
    
    @classmethod
    def get_by_mat(cls, matricula):
        conexao = obter_conexao()
        SELECT = 'SELECT * FROM usuarios WHERE matricula=?'
        dados = conexao.execute(SELECT, (matricula,)).fetchone()
        conexao.close()

        if dados:
            return cls(dados['matricula'], dados['email'], dados['senha'], dados['id'])
        return None