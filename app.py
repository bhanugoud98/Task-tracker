from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        category = request.form["category"]
        new_task = Task(name=name, category=category)
        db.session.add(new_task)
        db.session.commit()
        return redirect("/")

    tasks = db.session.query(Task.name, Task.category, db.func.count(Task.name)).group_by(Task.name, Task.category).all()
    return render_template("index.html", tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)