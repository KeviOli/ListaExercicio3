from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Arquivo JSON para armazenar as tarefas
TASKS_FILE = "tasks.json"
# Variável para controlar o próximo ID disponível
next_task_id = 1

# Função para carregar as tarefas do arquivo JSON
def load_tasks():
    try:
        with open(TASKS_FILE, "r") as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = []
    return tasks

# Função para salvar as tarefas no arquivo JSON
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file)

# Rota para listar todas as tarefas
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = load_tasks()
    return jsonify(tasks)

# Rota para adicionar uma nova tarefa
@app.route('/tasks', methods=['POST'])
def add_task():
    global next_task_id
    data = request.json
    data['id'] = next_task_id
    next_task_id += 1
    tasks = load_tasks()
    tasks.append(data)
    save_tasks(tasks)
    return jsonify(data), 201

# Rota para marcar uma tarefa como concluída
@app.route('/tasks/<int:task_id>/complete', methods=['PUT'])
def complete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = True
            save_tasks(tasks)
            return jsonify(task)
    return jsonify({"error": "Tarefa não encontrada"}), 404

# Rota para excluir uma tarefa
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = load_tasks()
    for i, task in enumerate(tasks):
        if task['id'] == task_id:
            del tasks[i]
            save_tasks(tasks)
            return jsonify({"message": "Tarefa excluída com sucesso"})
    return jsonify({"error": "Tarefa não encontrada"}), 404

if __name__ == '__main__':
    app.run(debug=True)
