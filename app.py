from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)

tasks = []
task_id = 1

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id
    data = request.get_json()
    newTask = Task(task_id, data.get('title'),data.get('description', ''), False)
    tasks.append(newTask)
    task_id += 1
    return jsonify({"message": "Nova tarefa criada com sucesso."})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks_list = [task.to_dict() for task in tasks]

    output = {
        "tasks":tasks_list,
        "total_tasks": len(tasks_list)
    }

    return jsonify(output)


@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    for task in tasks:
        if task.id == id:
            return jsonify(task.to_dict())
        
    return jsonify({"message": "Tarefa não encontrada"}),404

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    for task in tasks:
        if task.id == id:
            data = request.get_json()
            task.title = data['title']
            task.description = data['description']
            task.completed = data['completed']
            return jsonify({'message': 'Tarefa atualizada.'})
    return jsonify({'message': 'Tarefa não encontrada'}), 404

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    for task in tasks:
        if task.id == id:
            tasks.remove(task)
            return jsonify({'message': 'Tarefa Deletada.'})
    return jsonify({'message': 'Não foi possivel deletar a tarefa.'}), 404
    
    



if __name__ == "__main__":
    app.run(debug=True)
