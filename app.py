from subprocess import CompletedProcess
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys ## use to print out system info incase code brings out an error
from flask_migrate import Migrate

#connecting our app to flask
app = Flask(__name__)

# connecting database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://banga:banga123@localhost:5432/todoapp'

# disable database-track-modifications that add overhead
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#linking our app with SQLALchemy
db = SQLAlchemy(app)

## enables db migration
migrate = Migrate(app, db)

# Models
class Todo(db.Model):
    __tablename__= 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)


    def __repr__(self):
        return f'<Todo {self.id}, {self.description}>'

#code below creates the Todo {Table} in the todoapp {database}
#db.create_all()


class TodoList(db.Model):
    __tablename__ = 'todolists'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='list', lazy=True)

    def __repr__(self):
        return f'<Todolist {self.id} {self.name}>'


#This code below represents the 'R' in CRUD
## code below links html template and our Todo-app
@app.route('/') # <-- controller
def index(): 
    return render_template('index.html', todos=Todo.query.order_by('id').all())  # <-- first part {'index.html'} is the 'View' layer,
     # second layer {data=Todo.query.all()} is the 'Model' that has the data to be displayed. 


## Code below reprensents the 'C' in CRUD
## code below creates a new todo item, saves the new record to the db 
# and updates the View with new list of records
# it uses ajax to fetch requests from client side and
##? how to make the client refresh only a part of it, instead of the whole webpage
@app.route('/todos/create', methods=['POST'])
def create_todo():
  error = False
  body = {}
  try:
    description = request.get_json()['description']
    todo = Todo(description=description, completed=False)
    db.session.add(todo)
    db.session.commit()
    body['id'] = todo.id
    body['completed'] = todo.completed
    body['description'] = todo.description
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    return jsonify(body)



# controller code below deals with the "U" section in CRUD 
@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        completed = request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()

    except:
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('index')) # after refresh, <- will return fresh items in the list 


# code below deals with "D" in CRUD
# delete todo 
@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
 try:
     Todo.query.filter_by(id=todo_id).delete()
     db.session.commit()
 except:
       db.session.rollback()
 finally:
     db.session.close()
 return jsonify({ 'success': True })








    
#always include this at the bottom of your code (port 3000 is only necessary in workspaces)

#if __name__ == '__main__':
#    app.run(host="0.0.0.0", port=3000)