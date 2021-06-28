from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def get_name():
    con = sqlite3.connect('names.db')
    cur = con.cursor()
    try:
        cur.execute('''CREATE TABLE names (name text, lastname text)''')
    except Exception as e:
        pass

    try:
        last_entry = cur.execute('SELECT * FROM names').fetchall()[-1]
        _name, _lastname = last_entry[0], last_entry[1]
    except IndexError:
        _name = _lastname = "unknown name"

    if request.method == "POST":
        _name = request.form['name']
        _lastname = request.form['lastname']
        cur.execute("INSERT INTO names VALUES (?, ?)", (_name, _lastname))
        con.commit()
        con.close()

    return render_template("index.html", name=_name + " " + _lastname)


app.run(host="localhost", port=8080)
