from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)  # setting app name as this file

# stating that sqlite will be used as db
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///crud_db.db"
db = SQLAlchemy(app)


class Task(db.Model):
    """Creating model for task"""
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(150), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Task {self.id}>"


# set route of the homepage(index) as "/" and allow given http methods
@app.route("/", methods=['POST', 'GET'])
def index():
    """Defining homepage and task-adding http logic"""
    if request.method == 'POST':
        # taking the task content from a HTML form
        task_content = request.form['content']
        new_task = Task(content=task_content)

        try:
            # if everything is correct add the task to the database
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except ValueError:
            # otherwise, if for example task is incorrectly added show an error
            return "some issue occurred"

    else:
        # show sorted all the tasks(working with HTML template)
        tasks = Task.query.order_by(Task.date_created).all()
        return render_template("index.html", tasks=tasks)


# set route of the delete page with specified task id
@app.route("/delete/<int:id>")
def delete(id):
    to_delete = Task.query.get_or_404(id)  # get task id

    try:
        # try to delete the task and redirect to homepage
        db.session.delete(to_delete)
        db.session.commit()
        return redirect("/")

    except ValueError:
        return "some issue occurred regarding DELETING that task"


# set route of the update page with specified task id, allow given http methods
@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    to_update = Task.query.get_or_404(id)  # get task id

    if request.method == 'POST':
        # taking the task content from a HTML form
        to_update.content = request.form['content']

        try:
            # commit the changes to the database
            db.session.commit()
            return redirect("/")

        except ValueError:
            return "some issue occurred regarding UPDATING that task"

    else:
        # show update page with choosen task
        return render_template("update.html", task=to_update)


# running app in debug mode to let it show errors, do not use in production
if __name__ == "__main__":
    app.run(debug=True)
