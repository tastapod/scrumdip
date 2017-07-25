from flask import Flask, render_template

app = Flask(__name__)

@app.route("/hello")
def index():
    return render_template("index.html")
