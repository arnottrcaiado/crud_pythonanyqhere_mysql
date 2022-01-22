
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask( __name__)


SQLALCHEMY_DATABASE_URI = "icapp.mysql.pythonanywhere-services.com://{username}:{password}@{hostname}/{databasename}".format(
    username="icapp 'Databases' tab",
    password="1234567@@@' tab",
    hostname="icapp.mysql.pythonanywhere-services.com 'Databases' tab",
    databasename="icapp$default",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


@app.route('/')
def hello_world():
    return 'Olá. Esta é nossa primeira aplicação Flask!'


@app.route('/ictela/<string:frase>')
def ictela( frase ):
    return render_template( 'index.html' , texto=frase)


@app.route("/graph")
def graph():
    data = [
        ("01-01-2020", 100),
        ("02-01-2020", 200),
        ("03-01-2020", 150),
        ("04-01-2020", 100),
        ("05-01-2020", 200),
        ("06-01-2020", 90),
        ("01-01-2020", 10),
        ("02-01-2020", 200),
        ("03-01-2020", 120),
        ("04-01-2020", 100),
        ("05-01-2020", 200),
        ("06-01-2020", 90),
        ("07-01-2020", 230)
        ]

    labels = [row[0] for row in data]
    values = [row[1] for row in data]

    return render_template("graph.html", labels=labels, values=values )


@app.route("/table", methods=["GET","POST"] )
def table():
    cabecalho = ("Id","Criterio","S/N/NSA")
    dados = (
        ("01","Sistema Qualidade","_"),
        ("02","Sistema Gestão","_"),
        ("03","Sistema Mkt","_"),
        ("04","Sistema Vendas","_"),
        ("01","Sistema Qualidade","_"),
        ("02","Sistema Gestão","_"),
        ("03","Sistema Mkt","_"),
        ("04","Sistema Vendas","_"),
        ("01","Sistema Qualidade","_"),
        ("02","Sistema Gestão","_"),
        ("03","Sistema Mkt","_"),
        ("04","Sistema Vendas","_"),
        ("01","Sistema Qualidade","_"),
        ("02","Sistema Gestão","_"),
        ("03","Sistema Mkt","_"),
        ("04","Sistema Vendas","_"),
        ("01","Sistema Qualidade","_"),
        ("02","Sistema Gestão","_"),
        ("03","Sistema Mkt","_"),
        ("04","Sistema Vendas","_"),
        ("01","Sistema Qualidade","_"),
        ("02","Sistema Gestão","_"),
        ("03","Sistema Mkt","_"),
        ("04","Sistema Vendas","_"),
        ("01","Sistema Qualidade","_"),
        ("02","Sistema Gestão","_"),
        ("03","Sistema Mkt","_"),
        ("04","Sistema Vendas","_"),
        ("01","Sistema Qualidade","_"),
        ("02","Sistema Gestão","_"),
        ("03","Sistema Mkt","_"),
        ("04","Sistema Vendas","_"),
        ("01","Sistema Qualidade","_"),
        ("02","Sistema Gestão","_"),
        ("03","Sistema Mkt","_"),
        ("04","Sistema Vendas","_"),

        )

    return render_template("table.html", cabecalho=cabecalho, dados=dados )


