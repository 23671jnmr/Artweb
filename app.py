from flask import Flask, render_template

app = Flask(__name__)


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
    # traditional page
    return render_template('traditional.html')

@app.route('/digital.html')
def digital():
    # digital page
    return render_template('digital.html')

@app.route('/others.html')
def other():
    #other page
    return render_template('others.html')


if __name__ == "__main__":
    app.run(debug=True)
    