from flask import Flask, render_template_string, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

DB_USER = os.getenv("DB_USER", "admin")          # RDS username
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")  # RDS password
DB_HOST = os.getenv("DB_HOST", "your-rds-endpoint.rds.amazonaws.com")  # RDS endpoint
DB_NAME = os.getenv("DB_NAME", "todo_db")       # Database name

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)


HTML_TEMPLATE = """
<!doctype html>
<title>Flask + AWS RDS Todo</title>
<h1>Todo List (AWS RDS)</h1>
<form method="POST">
    <input name="title" placeholder="New todo" required>
    <button type="submit">Add</button>
</form>
<ul>
{% for item in todos %}
  <li>{{ item.title }}</li>
{% endfor %}
</ul>
"""


@app.before_first_request
def create_tables():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title")
        if title:
            todo = Todo(title=title)
            db.session.add(todo)
            db.session.commit()
        return redirect("/")
    todos = Todo.query.all()
    return render_template_string(HTML_TEMPLATE, todos=todos)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
