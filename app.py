from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_mail import Mail, Message
from boto.s3.connection import S3Connection
import os

app = Flask(__name__)


s3 = S3Connection(os.environ['MAIL_DEFAULT_SENDER'], os.environ['MAIL_PASSWORD'], os.environ['MAIL_USERNAME'], os.environ['SECRET_KEY'])

# Configure send emails
app.config["MAIL_DEFAULT_SENDER"] = os.environ['MAIL_DEFAULT_SENDER']
app.config["MAIL_PASSWORD"] = os.environ['MAIL_PASSWORD']
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ['MAIL_USERNAME']
mail = Mail(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/test", methods=["GET", "POST"])
def test():
    if request.method =="POST":
        email = request.form.get("email")
        message = Message("Hola ", recipients=[email])
        message.body = "Enhorabuena! ah funcionado el envio de correos. Te invito a mantenerte en contacto con el creador de la pagina para saber cuando hayan nuevas actualizaciones en la funcionalidad de esta aplicacion web"
        mail.send(message)

        # aparentemente flash funciona solo dentro de las seciones
        # flash("esta es una prueba de envio de correo electronico, por favor revisa tu buzon de correos", "message")
        
        return render_template("index.html")
    return render_template("test.html")

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)