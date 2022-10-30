from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_mail import Mail, Message
from boto.s3.connection import S3Connection
import os


# ELIMINAR AL TERMINAR PRUEBA TO LO RELACIONADO CON LA BASE DE DATOS
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)


s3 = S3Connection(os.environ['MAIL_DEFAULT_SENDER'], os.environ['MAIL_PASSWORD'], os.environ['MAIL_USERNAME'], os.environ['SECRET_KEY'], os.environ['DATABASE'])

# Configure send emails
app.config["MAIL_DEFAULT_SENDER"] = os.environ['MAIL_DEFAULT_SENDER']
app.config["MAIL_PASSWORD"] = os.environ['MAIL_PASSWORD']
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ['MAIL_USERNAME']
mail = Mail(app)

# Configure Postrge Heroku as database
engine = create_engine(os.environ['DATABASE'])
db = scoped_session(sessionmaker(bind=engine))

#desaciendome de la chache
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/test", methods=["GET", "POST"])
def test():
    # ELIMINAR DESPUES DE HACER PRUEBA
    rows = db.execute("SELECT * FROM emojis").fetchall()
    if request.method =="POST":
        email = request.form.get("email")
        message = Message("Hola estimad@", recipients=[email])
        message.body = "Enhorabuena! ah funcionado el envio de correos. Te invito a mantenerte en contacto con el creador de la pagina para saber cuando hayan nuevas actualizaciones en la funcionalidad de esta aplicacion web"
        mail.send(message)

        # aparentemente flash funciona solo dentro de las seciones
        return render_template("index.html")
    return render_template("test.html", imgs=rows)

@app.route("/search")
def search():
    emoji_input = request.args.get("q")
    # Uso hex(ord()) porque guarde los emojis con apariencia hexadecimal en la base de datos
    # Luego lo convierto en str para poder remplazar el "0" que ocupa el primer caracter 
    # un MILLON DE GRACIAS A https://www.otaviomiranda.com.br/2020/normalizacao-unicode-em-python/
    
    if emoji_input:
        emoji_html = str(hex(ord(emoji_input))).replace("0x", "x")
        print(emoji_html)

        emoji_data = db.execute("SELECT * FROM emojis WHERE hexa = :hexa", {"hexa":emoji_html}) 
        return render_template("search.html", emoji_data=emoji_data)

    return render_template("search.html")



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)