from flask import Flask, render_template, request, jsonify, session
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Initialize tasks file
TASKS_FILE = 'tasks.json'

def load_tasks():
    """Load tasks from JSON file"""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    """Save tasks to JSON file"""
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    """Main page route"""
    # Set default language to English if not set
    if 'language' not in session:
        session['language'] = 'en'
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """API endpoint to get all tasks"""
    tasks = load_tasks()
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def add_task():
    """API endpoint to add a new task"""
    data = request.get_json()
    tasks = load_tasks()
    
    new_task = {
        'id': len(tasks) + 1,
        'title': data.get('title', ''),
        'completed': False,
        'created_at': datetime.now().isoformat()
    }
    
    tasks.append(new_task)
    save_tasks(tasks)
    return jsonify(new_task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """API endpoint to update a task"""
    data = request.get_json()
    tasks = load_tasks()
    
    for task in tasks:
        if task['id'] == task_id:
            task['title'] = data.get('title', task['title'])
            task['completed'] = data.get('completed', task['completed'])
            save_tasks(tasks)
            return jsonify(task)
    
    return jsonify({'error': 'Task not found'}), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """API endpoint to delete a task"""
    tasks = load_tasks()
    
    for i, task in enumerate(tasks):
        if task['id'] == task_id:
            deleted_task = tasks.pop(i)
            save_tasks(tasks)
            return jsonify(deleted_task)
    
    return jsonify({'error': 'Task not found'}), 404

@app.route('/api/language', methods=['POST'])
def set_language():
    """API endpoint to set language preference"""
    data = request.get_json()
    language = data.get('language', 'en')
    session['language'] = language
    return jsonify({'language': language})

@app.route('/api/language', methods=['GET'])
def get_language():
    """API endpoint to get current language"""
    return jsonify({'language': session.get('language', 'en')})

if __name__ == '__main__':
    app.run(debug=True) 