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
# #Routes allow binding a function to a URL. Here we create a route to our home page
@app.route('/')
def home():
    # List of todos pulled from database
    todo_list = Todo.query.all()
    # HTML rendered of todo list
    # #Templates allow a base model for an app that can be built off of. 
    return render_template("base.html", todo_list=todo_list)

# #Route allows us to add todo function to the add button
# Route to add new todo
@app.route("/add", methods=["POST"])
def add():
    # New todo is created 
    #Requests allow accessing data from a form 
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    # Database is updated
    # #Sessions allow storing information specific to a user, so we save a new todo for the current user
    db.session.add(new_todo)
    db.session.commit()
    # Redirect back to homepage
    # #Redirects allow me to send the user to another endpoint
    return redirect(url_for("home"))

# #Route allows us to link an update function with to the update URL
# Route to update a certain todo's completion
@app.route("/update/<int:todo_id>")
def update(todo_id):
    # Todos are filtered by given id
    todo = Todo.query.filter_by(id=todo_id).first()
    # That todo's completion is toggled
    todo.complete = not todo.complete
    # Database is updated
    # #Session allows us to update our todo in the DB for the current user
    db.session.commit()
    # Redirect back to homepage
    # #Redirects allow me to send the user to another endpoint
    return redirect(url_for("home"))

# #Route allows us to link a delete function to a url
# Route to delete a todo
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    # Todo to be deleted is found by filtering for id
    todo = Todo.query.filter_by(id=todo_id).first()
    # That todo is deleted from the database
    db.session.delete(todo)
    # Database is updated
    # #Session allows us to reflect a deleted todo for our current user 
    db.session.commit()
    # Redirect back to homepage
    # #Redirects allow me to send the user to another endpoint
    return redirect(url_for("home"))

if __name__ == "__main__":
    # Creates database and tables
    with app.app_context():
        db.create_all()
        # debug=True means server doesn't reload for changes in code
        app.run(debug=True)

