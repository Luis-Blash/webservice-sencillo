from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

#------ SQLAlchemy
urldb= "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"
app.config['SQLALCHEMY_DATABASE_URI']=urldb
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
ma = Marshmallow(app)


# app de tareas ------
# ------- Tablas ---------
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), unique= True)
    description = db.Column(db.String(100))

    def __init__(self, title, description):
        self.title = title
        self.description = description
# con esto hacemos que crea todas nuestras tablas
db.create_all()


# creamos un esquema que nos permite interactuar con nuestra tabla
class TaskSchema(ma.Schema):
    class Meta: 
        fields = ('id','title','description')
task_schema =  TaskSchema()
tasks_schema = TaskSchema(many=True)


@app.route('/tasks', methods=['POST'])
def create_task():
    title = request.json['title']
    description = request.json['description']
    new_task = Task(title, description)
    db.session.add(new_task)
    db.session.commit()
    return task_schema.jsonify(new_task)

# usando la misma direccion usamos get para recibir
@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_task =  Task.query.all()
    result = tasks_schema.dump(all_task)
    return jsonify(result)

# si quiremos una tarea en especifico
@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    return task_schema.jsonify(task)

# si queremos actualizar una tarea
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task =  Task.query.get(id)
    title = request.json['title']
    description = request.json['description']
    task.title = title
    task.description =  description
    db.session.commit()
    return task_schema.jsonify(task)


# eliminar
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task =  Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return task_schema.jsonify(task)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message":"Bienvenido a mi api"})

if __name__ == "__main__":
    #host="0.0.0.0"
    app.run(debug=True, port=5000,host="0.0.0.0")