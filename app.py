from flask import Flask, render_template, request, redirect
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
        image = request.form['image_url'].strip()
        title = request.form['title']
        description = request.form['description']
        rating = request.form['rating']
        category = request.form['category']
        username = request.form['username']

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO uploads (title, image, description, rating, username,"
            "category) VALUES (?, ?, ?, ?, ?, ?)",
            (title, image, description, rating, username, category)
        )
        conn.commit()
        conn.close()

        return redirect('/')
    return render_template('upload.html')


if __name__ == "__main__":
    app.run(debug=True)
