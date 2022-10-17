#
# CRUD utilizando SQLAlchemy e MYSQL - Pythonanywhere
# fins didáticos
# Arnott Ramos Caiado
# janeiro de 2022
# fonte:
# https://www.youtube.com/watch?v=VNaTl2i5P1U
# https://www.youtube.com/watch?v=WDpPGFkI9UU
#
# rota principal
# https://icapp.pythonanywhere.com/
#
from flask import Flask, Response, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import json
import os
import time
from datetime import datetime, date

arq='/home/icapp/mysite/arquivos/log.csv'

os.environ["TZ"] = "America/Recife"
time.tzset()

# configuração base do sqlalchemy
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://icapp:1234567ABC@icapp.mysql.pythonanywhere-services.com/icapp$usuarios'
db = SQLAlchemy(app)

# criação da classe com a estrutura da tabela Usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    nome = db.Column(db.String(50))
    email = db.Column(db.String(50))

    def to_json(self):
        return {"id": self.id, "nome": self.nome, "email": self.email}


# app atraves de html
# tabela de dados com opções de alteração, inclusão e edição
# opções de busca.
# ?order=desc . ordena em ordem descendente, pelo nome
# ?order=no . em ordem de cadastro
# filter e pfilter . usados pelo endpoit de pesquisa para pesquisar por nome ou email. Exemplo: maria% para buscar nomes iniciados por maria
# https://icapp.pythonanywhere.com/
@app.route("/")
def menu():
    order = request.args.get('order', default = "asc", type = str )
    filters = request.args.get('filters', default = "*", type = str )
    pfilter = request.args.get('pfilter', default ="none", type = str )

    ipuser = request.headers['X-Real-IP']
    salva_log( arq, str(ipuser))
    if filters != "*" and pfilter == "nome" :
#        usuarios = Usuario.query.filter( Usuario.nome.in_(filters))
        usuarios = Usuario.query.filter(Usuario.nome.like(filters))
        return render_template( 'usuarios.html', usuarios=usuarios )
    if filters != "*" and pfilter == "email" :
        usuarios = Usuario.query.filter(Usuario.email.like(filters))
        return render_template( 'usuarios.html', usuarios=usuarios )
    if order == "asc" :
        usuarios = Usuario.query.order_by( Usuario.nome )
    elif order == "desc":
        usuarios = Usuario.query.order_by( Usuario.nome.desc() )
    else:
        usuarios = Usuario.query.all()

    return render_template( 'usuarios.html', usuarios=usuarios )
#
# inclusão de dados
# https://icapp.pythonanywhere.com/incluir
@app.route("/incluir", methods=['GET','POST'])
def incluir():
    if request.method == 'POST':
        nome =request.form['nome']
        email =request.form['email']
        if ( len(nome) != 0 and len(email) != 0 ):
            usuario=Usuario(nome=nome, email=email)
            db.session.add(usuario)
            db.session.commit()
        return redirect(url_for('menu'))

    return render_template('incluir.html')
#
# edição de dados - utiliza o id da linha escolhida
# https://icapp.pythonanywhere.com/editar
@app.route("/editar/<int:id>", methods=['GET','POST'])
def editar(id):
    usuario=Usuario.query.get(id)
    if request.method == 'POST':
        usuario.nome=request.form['nome']
        usuario.email=request.form['email']
        db.session.commit()
        return redirect(url_for('menu'))

    return render_template('editar.html', usuario=usuario)
#
# exclusao de dados - utiliza o id da linha escolhida
# https://icapp.pythonanywhere.com/excluir
@app.route("/excluir/<int:id>")
def excluir(id):
    usuario=Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect( url_for('menu'))

#
# busca de dados - permite a busca por nome ou email ou todos se nome e email em branco
#
@app.route("/pesquisar", methods=['GET','POST'])
def pesquisar():
    if request.method == 'POST':
        nome=request.form['nome']
        email=request.form['email']
        filters="*"
        pfilter=""
        if ( len(nome) != 0 ) :
            filters = nome
            pfilter = "nome"
        elif ( len(email) != 0) :
            filters= email
            pfilter = "email"
        return redirect(url_for('menu', filters=filters, pfilter=pfilter))
    return render_template('pesquisar.html')

#
# salva log - data hora e ip. possibilita pelo menos medir acessos
#
def salva_log( arquivo, ipuser) :
    arq = open(arquivo,'a')
    data_atual = str(date.today())
    hora_atual = str(datetime.time(datetime.utcnow()))
    hora_atual = hora_atual[0:5]
    arq.write(data_atual+";"+hora_atual+";"+ipuser+"\n")
    arq.close()
    return

# #### APIs ###########
# Selecionar Tudo
@app.route("/usuarios", methods=["GET"])
def seleciona_usuarios():
    usuarios_objetos = Usuario.query.all()
    usuarios_json = [usuario.to_json() for usuario in usuarios_objetos]

    return gera_response(200, "usuarios", usuarios_json)

# Selecionar Individual
@app.route("/usuario/<id>", methods=["GET"])
def seleciona_usuario(id):
    usuario_objeto = Usuario.query.filter_by(id=id).first()
    usuario_json = usuario_objeto.to_json()

    return gera_response(200, "usuario", usuario_json)

# Cadastrar
# https://icapp.pythonanywhere.com/usuario
@app.route("/usuario", methods=["POST"])
def cria_usuario():
    body = request.get_json()

    try:
        usuario = Usuario(nome=body["nome"], email= body["email"])
        db.session.add(usuario)
        db.session.commit()
        return gera_response(201, "usuario", usuario.to_json(), "Criado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "usuario", {}, "Erro ao cadastrar")


# Atualizar
# https://icapp.pythonanywhere.com/usuario/<id>
@app.route("/usuario/<id>", methods=["PUT"])
def atualiza_usuario(id):
    usuario_objeto = Usuario.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if('nome' in body):
            usuario_objeto.nome = body['nome']
        if('email' in body):
            usuario_objeto.email = body['email']

        db.session.add(usuario_objeto)
        db.session.commit()
        return gera_response(200, "usuario", usuario_objeto.to_json(), "Atualizado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "usuario", {}, "Erro ao atualizar")

# Deletar
# https://icapp.pythonanywhere.com/usuario/<id>
@app.route("/usuario/<id>", methods=["DELETE"])
def deleta_usuario(id):
    usuario_objeto = Usuario.query.filter_by(id=id).first()

    try:
        db.session.delete(usuario_objeto)
        db.session.commit()
        return gera_response(200, "usuario", usuario_objeto.to_json(), "Deletado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "usuario", {}, "Erro ao deletar")


def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")


