from app import app
from flask import render_template

@app.route("/")
def hello_world2():
    return render_template("index.html")

@app.route("/add/<first_number>/<second_number>")
def adding_2_numbera(first_number, second_number):
    a = [first_number,second_number]
    b = list(map(int, a))
    s = str(sum(b))
    return render_template("Adding.html", variable=s)
