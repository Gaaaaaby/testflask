from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean 
from sqlalchemy import exc
#flask run 


#- [ ] Usar endpoints con async-await.
# - [ ] Modelo Task con `id`, `title`, `description`, `completed`.
# - [ ] Endpoints para listar tareas, obtener detalles de una tarea, crear una nueva tarea, actualizar una tarea existente y eliminar una tarea.
# - [ ] Validación de entrada para todos los endpoints.
# - [ ] (Opcional) Autenticación básica para proteger los endpoints.

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:121224@localhost:5432/testdb'
db = SQLAlchemy(app)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    completed = Column(Boolean)

with app.app_context():
    db.create_all()

@app.route('/tasks', methods=['POST'])
def create_task():
    try:
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        completed = data.get('completed')

        if not title or not isinstance(title, str):
            return "Error: the title is empty or isnt string.", 400
        if not description:
            return "Error: the description is empty.", 400
        if not isinstance(completed, bool):
            return "Error: completed must be a boolean.", 400

        task = Task(title=title, description=description, completed=completed)
        db.session.add(task)
        db.session.commit()

        return jsonify({'title': task.title, 'description':task.description,'completed': task.completed}), 201
    except exc.SQLAlchemyError:
        print('there was a problem updating the task')
        db.session.rollback()

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    try:
        task = Task.query.get(task_id)
        if task is None:
            abort(404)

        return jsonify({'task': task.title})
    except exc.SQLAlchemyError:
        print('there was a problem updating the task')
        db.session.rollback()

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        data = request.get_json()
        if not data:
            abort(400)

        task = Task.query.get(task_id)
        if task is None:
            abort(404)

        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'completed' in data:
            if isinstance(data['completed'], bool):
                task.completed = data['completed']
        else:
            return "Error: completed must be a boolean.", 400

        db.session.commit()

        return jsonify({'task': task.title, 'description': task.description, 'completed': task.completed})
    except exc.SQLAlchemyError:
        print('there was a problem updating the task')
        db.session.rollback()


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        task = Task.query.get(task_id)
        if task is None:
            abort(404)

        db.session.delete(task)
        db.session.commit()

        return jsonify({'result': True})
    except exc.SQLAlchemyError:
        print('there was a problem deleting the task')
        db.session.rollback()