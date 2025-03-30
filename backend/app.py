# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Simple in-memory data store
tasks = [
    {"id": 1, "title": "Learn Flask", "completed": True},
    {"id": 2, "title": "Learn Next.js", "completed": False},
    {"id": 3, "title": "Build a full-stack app", "completed": False}
]

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task:
        return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route('/api/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        return jsonify({"error": "Title is required"}), 400
    
    new_task = {
        "id": max(task["id"] for task in tasks) + 1 if tasks else 1,
        "title": request.json["title"],
        "completed": request.json.get("completed", False)
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    if not request.json:
        return jsonify({"error": "No data provided"}), 400
    
    if 'title' in request.json:
        task['title'] = request.json['title']
    if 'completed' in request.json:
        task['completed'] = request.json['completed']
    
    return jsonify(task)

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    tasks.remove(task)
    return jsonify({"message": "Task deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)