from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def home():
    # home page
    return render_template('home.html')


@app.route('/login.html')
def login():
    # login page
    return render_template('login.html')


@app.route('/traditional.html')
def traditional():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM uploads WHERE category = 'traditional'")
    uploads = cur.fetchall()
    conn.close()
    return render_template('traditional.html', uploads=uploads)


@app.route('/digital.html')
def digital():
    # digital page
    return render_template('digital.html')


@app.route('/others.html')
def other():
    #other page#
    return render_template('others.html')


if __name__ == "__main__":
    app.run(debug=True)

#sign up