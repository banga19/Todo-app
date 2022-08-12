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


    def __repr__(self):
        return f'<Todo {self.id}, {self.description}>'

#code below creates the Todo {Table} in the todoapp {database}
#db.create_all()



#This code below represents the 'R' in CRUD
## code below links html template and our Todo-app
@app.route('/') # <-- controller
def index(): 
    return render_template('index.html', data=Todo.query.all())  # <-- first part {'index.html'} is the 'View' layer,
     # second layer {data=Todo.query.all()} is the 'Model'. 


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
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    if error: ## if something goes wrong in the code, then show error with status (400)
        abort (400)

    if not error: ## if code runs succcesfully, display the new object to the Client after adding it to the DB
        return jsonify(body)

#always include this at the bottom of your code (port 3000 is only necessary in workspaces)

#if __name__ == '__main__':
#    app.run(host="0.0.0.0", port=3000)