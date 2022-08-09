from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

#connecting our app to flask
app = Flask(__name__)

# connecting database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://banga:banga123@localhost:5432/todoapp'

# disable database-track-modifications that add overhead
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#linking our app with SQLALchemy
db = SQLAlchemy(app)

# Models
class Todo(db.Model):
    __tablename__= 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)


    def __repr__(self):
        return f'<Todo {self.id}, {self.description}>'

#code below creates the Todo {Table} in the todoapp {database}
db.create_all()




## code below links html template and our Todo-app
@app.route('/') # <-- controller
def index(): 
    return render_template('index.html', data=Todo.query.all())  # <-- first part {'index.html'} is the 'View' layer,
     # second layer {data=Todo.query.all()} is the 'Model'. This code represents the 'R' in CRUD



## code below creates a new todo item, saves the new record to the db 
# and updates the View with new list of records
@app.route('/todos/create', methods=['POST'])
def create_todo():
    description = request.get_json()['description']
    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    return jsonify({
        'description': todo.description
    })

#always include this at the bottom of your code (port 3000 is only necessary in workspaces)

#if __name__ == '__main__':
#   app.run(host="0.0.0.0", port=3000)