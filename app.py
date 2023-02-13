# Imports
from flask import Flask, render_template, current_app, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


# Instantiate our app
app = Flask(__name__)

# Setting configuration parameters for the database
# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creating the database
db = SQLAlchemy(app)


# Creating a model class for the todo items with three entries
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

# Every url/route needs a function and @app.route(**)

# Homepage will list all the todos
@app.route('/')
def home():
    # List of todos pulled from database
    todo_list = Todo.query.all()
    # HTML rendered of todo list
    return render_template("base.html", todo_list=todo_list)

# Route to add new todo
@app.route("/add", methods=["POST"])
def add():
    # New todo is created 
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    # Database is updated
    db.session.add(new_todo)
    db.session.commit()
    # Redirect back to homepage
    return redirect(url_for("home"))

# Route to update a certain todo's completion
@app.route("/update/<int:todo_id>")
def update(todo_id):
    # Todos are filtered by given id
    todo = Todo.query.filter_by(id=todo_id).first()
    # That todo's completion is toggled
    todo.complete = not todo.complete
    # Database is updated
    db.session.commit()
    # Redirect back to homepage
    return redirect(url_for("home"))

# Route to delete a todo
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    # Todo to be deleted is found by filtering for id
    todo = Todo.query.filter_by(id=todo_id).first()
    # That todo is deleted from the database
    db.session.delete(todo)
    # Database is updated
    db.session.commit()
    # Redirect back to homepage
    return redirect(url_for("home"))

if __name__ == "__main__":
    # Creates database and tables
    with app.app_context():
        db.create_all()
        # debug=True means server doesn't reload for changes in code
        app.run(debug=True)

