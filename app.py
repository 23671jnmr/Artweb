import os
import sqlite3
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename


app = Flask(__name__)


UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def fix_image_url(url):
    """Clean up and convert webpage links into direct image URLs."""
    if not url:
        return url

    url = url.strip()

    if not (url.startswith('http://') or url.startswith('https://')):
        return url

# like turning https://....12345 to https://....12345.jpg
    if 'imgur.com/' in url and 'i.imgur.com' not in url:
        image_id = url.split('/')[-1]
        return f"https://i.imgur.com/{image_id}.jpg"

    # if it already has an HTTP link but missing an extension
    image_extension = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg')
    if not url.lower().endswith(image_extension):
        url = url + '.jpg'

    return url


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
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM uploads WHERE id = ?", (art_id,))
    art = cur.fetchone()
    cur.execute(
        "SELECT username, comment_text, timestamp FROM comments "
        "WHERE upload_id = ?",
        (art_id,)
    )
    comments = cur.fetchall()

    conn.close()

    return render_template('art_page.html', art=art, comments=comments)


@app.route('/add_comment/<int:art_id>', methods=['POST'])
def add_comment(art_id):
    comment_text = request.form['comment_text']
    username = "User12345"

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO comments (upload_id, username, comment_text, timestamp) "
        "VALUES (?, ?, ?, datetime('now'))",
        (art_id, username, comment_text)
    )
    conn.commit()
    conn.close()

    return redirect(f"/art/{art_id}")


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        image_value = ""

        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_value = filename

        elif (
            'image_url' in request.form
            and request.form['image_url'].strip() != ''
        ):
            image_value = fix_image_url(request.form['image_url'])

        else:
            image_value = 'sampleart.jpg'

        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        username = request.form['username']

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO uploads (title, image, description, rating, username,"
            "category) VALUES (?, ?, ?, ?, ?, ?)",
            (title, image_value, description, username, category)
        )
        conn.commit()
        conn.close()

        redirect_page = (
            "others.html" if category == "other" else f"{category}.html"
        )
        return redirect(f"/{redirect_page}")

    return render_template('upload.html')


if __name__ == "__main__":
    app.run(debug=True)
