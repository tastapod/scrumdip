from flask import Flask, redirect, render_template, request, url_for

import database
import fetch

app = Flask(__name__)


@app.route("/hello")
def index():
    return render_template("index.html")


@app.route("/update", methods=["POST"])
def update_counts():
    database.check_or_create_tables()
    counts = fetch.get_all_counts()
    print(counts)
    for cert, count in counts:
        database.insert_results(cert, count)

    return redirect(url_for("latest_counts")), 302


@app.route("/latest")
def latest_counts():
    counts = database.latest_counts()
    counts = [(cert, counts, ts.date()) for cert, counts, ts in counts]
    print(counts)
    return render_template("latest_counts.html", counts=counts)
