from flask import Flask, render_template, url_for, request, redirect 

from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from werkzeug.security import generate_password_hash, check_password_hash 

from models import User, obter_conexao

login_manager = LoginManager()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SUPERULTRAMEGADIFICIL'
login_manager.init_app(app)

# quando precisar saber qual o usuário conectado
# temos como consultar ele no banco

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    erro = None
    if request.method == 'POST':
        matricula = request.form['matricula']
        senha = request.form['pass']

        user = User.get_by_mat(matricula)

        if user and check_password_hash(user.senha, senha):
            login_user(user)
            return redirect(url_for('dash'))
        else: 
            erro = "Sua matrícula ou senha estão incorretos. Tente novamente."

        
    return render_template('login.html', erro=erro)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['pass']
        matricula = request.form['matricula']

        # criptografar a senha e o e-mail
        hashed_senha = generate_password_hash(senha)
        hashed_email = generate_password_hash(email)

        conexao = obter_conexao()
        INSERT = 'INSERT INTO usuarios(matricula, email, senha) VALUES (?,?,?)'
        conexao.execute(INSERT, (matricula, hashed_email, hashed_senha))
        conexao.commit()

        # buscar o usuário recém-criado
        user = User.get_by_mat(matricula)

        if user: 
            login_user(user)
            return redirect(url_for('dash'))
        
        conexao.close()
    
    return render_template('register.html')

@app.route('/dash', methods=['POST', 'GET'])
@login_required 
def dash():
    conexao = obter_conexao()

    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        usuario_id = current_user.id

        INSERT = 'INSERT INTO exercicios(nome, descricao, usuario) VALUES (?,?,?)'
        
        conexao.execute(INSERT, (nome, descricao, usuario_id))
        conexao.commit()
        conexao.close()
            
        return render_template('dash.html')


    return render_template('dash.html')

@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))
