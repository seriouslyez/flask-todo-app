# Imports
from flask import Flask, render_template
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

if __name__ == "__main__":
# Creates database and tables
    db.create_all()
# debug=True means server doesn't reload for changes in code
    app.run(debug=True)

