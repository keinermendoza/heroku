from flask import Flask, flash, redirect, render_template, request, session, url_for

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/test", methods=["GET", "POST"])
def test():
    return render_template("test.html")