from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)  # setting app name as this file
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///crud_db.db"
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(150), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Task {self.id}>"


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Task(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except ValueError:
            return "some issue occurred"

    else:
        tasks = Task.query.order_by(Task.date_created).all()
        return render_template("index.html", tasks=tasks)


@app.route("/delete/<int:id>")
def delete(id):
    to_delete = Task.query.get_or_404(id)

    try:
        db.session.delete(to_delete)
        db.session.commit()
        return redirect("/")

    except ValueError:
        return "some issue occurred regarding DELETING that task"


@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    to_update = Task.query.get_or_404(id)

    if request.method == 'POST':
        to_update.content = request.form['content']

        try:
            db.session.commit()
            return redirect("/")

        except ValueError:
            return "some issue occurred regarding UPDATING that task"

    else:
        return render_template("update.html", task=to_update)


if __name__ == "__main__":
    app.run(debug=True)
