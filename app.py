import os
import sqlite3
import cloudinary
import cloudinary.uploader
from flask import Flask, render_template, request, redirect


os.environ['HTTP_PROXY'] = 'http://proxy.server:3128'
os.environ['HTTPS_PROXY'] = 'http://proxy.server:3128'

# Cloudinary Setup
cloudinary.config(
    cloud_name="hnou3cx6",
    api_key="278196854721826",
    api_secret="EDnAwQ0NocXYdNiAcRXMwxzL_bc",
    secure=True
)


app = Flask(__name__)


UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def home():
    # home page
    return render_template('home.html')


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
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM uploads WHERE category = 'digital'")
    uploads = cur.fetchall()
    conn.close()
    return render_template('digital.html', uploads=uploads)


@app.route('/others.html')
def other():
    # other page
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM uploads WHERE category = 'other'")
    uploads = cur.fetchall()
    conn.close()
    return render_template('others.html', uploads=uploads)


@app.route('/art/<int:art_id>')
def art_page(art_id):
    previous_page = request.args.get('from', 'home')

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM uploads WHERE id = ?", (art_id,))
    art = cur.fetchone()

    cur.execute(
        "SELECT username, comment_text, rating FROM comments "
        "WHERE upload_id = ?",
        (art_id,)
    )
    comments = cur.fetchall()

    conn.close()

    return render_template(
        'art_page.html',
        art=art,
        comments=comments,
        previous_page=previous_page
    )


@app.route('/add_comment/<int:art_id>', methods=['POST'])
def add_comment(art_id):
    previous_page = request.args.get('from', 'home')
    rating = request.form['rating']
    comment_text = request.form['comment_text']
    username = "Anonymous"

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO comments "
        "(upload_id, username, comment_text, rating) "
        "VALUES (?, ?, ?, ?)",
        (art_id, username, comment_text, rating)
    )
    conn.commit()
    conn.close()

    return redirect(f"/art/{art_id}?from={previous_page}")


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        image_url = ""

        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            upload_result = cloudinary.uploader.upload(file)
            image_url = upload_result['secure_url']
        else:
            image_url = 'sampleart.jpg'

        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        username = request.form['username']

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO uploads (username, title, image, description, category)"
            "VALUES (?, ?, ?, ?, ?)",
            (username, title, image_url, description, category)
        )
        conn.commit()
        conn.close()

        redirect_page = "others.html" if category == "other" else f"{category}.html"
        return redirect(f"/{redirect_page}")

    return render_template('upload.html')


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
