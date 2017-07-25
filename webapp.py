from flask import Flask, render_template, request
import database

app = Flask(__name__)

@app.route("/hello")
def index():
    return render_template("index.html")

@app.route("/search", methods=['POST'])
def search():
    cert = request.form['cert']
    print('Searching for cert ' + cert)
    count = database.latest_count(cert)
    
    return '''
    <html>
    <head><title>ScrumDip results for {0}</title>
    </head>
    <body>
    <h1>Results for {0}</h1>
    <p>We found <strong>{1}</strong> people with a <strong>{0}</strong> certificate.</p>
    </body>
    </html>
    '''.format(cert, count)
