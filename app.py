# app.py
import os
import sqlite3
from datetime import datetime
from flask import Flask, g, render_template, request, redirect, url_for, send_from_directory, flash

from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
DB_PATH = os.path.join(BASE_DIR, "gallery.db")
ALLOWED_EXT = {"png","jpg","jpeg","gif"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = "dev-local-only"  # change for real use (not necessary for local demo)


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.executescript("""
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        author TEXT NOT NULL,
        content TEXT NOT NULL,
        image TEXT,
        created_at TEXT NOT NULL
    );
    """)
    db.commit()

@app.teardown_appcontext
def close_connection(exc):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

@app.route("/", methods=["GET", "POST"])
def index():
    db = get_db()
    init_db()

    if request.method == "POST":
        author = request.form.get("author", "").strip() or "Anonymous"
        content = request.form.get("content", "").strip()
        file = request.files.get("image")

        if not content and (not file or file.filename == ""):
            flash("Add some text or an image for the post.", "warning")
            return redirect(url_for("index"))

        filename = None
        if file and file.filename != "":
            if allowed_file(file.filename):
                fname = secure_filename(f"{datetime.utcnow().timestamp()}_{file.filename}")
                path = os.path.join(app.config["UPLOAD_FOLDER"], fname)
                file.save(path)
                filename = fname
            else:
                flash("File type not allowed. Allowed: png, jpg, jpeg, gif", "error")
                return redirect(url_for("index"))

        db.execute(
            "INSERT INTO posts (author, content, image, created_at) VALUES (?,?,?,?)",
            (author, content, filename, datetime.utcnow().isoformat()),
        )
        db.commit()
        flash("Post created (local demo).", "success")
        return redirect(url_for("index"))

    posts = db.execute("SELECT * FROM posts ORDER BY created_at DESC").fetchall()
    return render_template("index.html", posts=posts)

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# small admin to reset DB (local-only)
@app.route("/admin", methods=["GET","POST"])
def admin():
    db = get_db()
    init_db()
    if request.method == "POST":
        # delete all posts and uploaded files
        rows = db.execute("SELECT image FROM posts WHERE image IS NOT NULL").fetchall()
        for r in rows:
            if r["image"]:
                try:
                    os.remove(os.path.join(app.config["UPLOAD_FOLDER"], r["image"]))
                except Exception:
                    pass
        db.execute("DELETE FROM posts")
        db.commit()
        flash("Database cleared (local demo).", "info")
        return redirect(url_for("admin"))
    count = db.execute("SELECT COUNT(*) as c FROM posts").fetchone()["c"]
    return render_template("admin.html", count=count)

if __name__ == "__main__":
    # create DB file if missing
    if not os.path.exists(DB_PATH):
        open(DB_PATH, "a").close()
    app.run(debug=True, port=5000)
