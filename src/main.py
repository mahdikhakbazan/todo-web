from flask import Flask, render_template, request, jsonify, session
import json
import os
from datetime import datetime
from config.config import SECRET_KEY, DEBUG

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['DEBUG'] = DEBUG

# File to store tasks (can be overridden via env var for testing)
TASKS_FILE = os.getenv('TASKS_FILE', 'tasks.json')

def _resolve_tasks_file() -> str:
    """Resolve tasks file path dynamically, allowing env override after import."""
    return os.getenv('TASKS_FILE', TASKS_FILE)

def load_tasks():
    """Load tasks from JSON file"""
    tasks_file = _resolve_tasks_file()
    if os.path.exists(tasks_file):
        try:
            with open(tasks_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

def save_tasks(tasks):
    """Save tasks to JSON file"""
    tasks_file = _resolve_tasks_file()
    with open(tasks_file, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def get_next_task_id(tasks):
    """Get the next available task ID"""
    if not tasks:
        return 1
    return max(task['id'] for task in tasks) + 1

@app.route('/')
def index():
    """Main page route"""
    # Determine language from session or query parameter (default to English)
    language = session.get('language', request.args.get('lang', 'en'))
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks, language=language)

# -----------------------------
# API endpoints for SPA frontend
# -----------------------------

@app.route('/api/tasks', methods=['GET'])
def api_get_tasks():
    """Return all tasks"""
    tasks = load_tasks()
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def api_add_task():
    """Create a new task (returns the created task)"""
    data = request.get_json() or {}
    title = (data.get('title') or '').strip()
    if not title:
        return jsonify({'error': 'Title is required'}), 400

    tasks = load_tasks()
    new_task = {
        'id': get_next_task_id(tasks),
        'title': title,
        'completed': False,
        'created_at': datetime.now().isoformat()
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return jsonify(new_task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def api_update_task(task_id: int):
    """Update an existing task"""
    data = request.get_json() or {}
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['title'] = (data.get('title')
                             if data.get('title') is not None
                             else task['title'])
            if data.get('completed') is not None:
                task['completed'] = bool(data['completed'])
            save_tasks(tasks)
            return jsonify(task)
    return jsonify({'error': 'Task not found'}), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def api_delete_task(task_id: int):
    """Delete a task and return it"""
    tasks = load_tasks()
    for i, task in enumerate(tasks):
        if task['id'] == task_id:
            deleted = tasks.pop(i)
            save_tasks(tasks)
            return jsonify(deleted)
    return jsonify({'error': 'Task not found'}), 404

@app.route('/api/language', methods=['GET'])
def api_get_language():
    """Get current language preference"""
    return jsonify({'language': session.get('language', 'en')})

@app.route('/api/language', methods=['POST'])
def api_set_language():
    """Set language preference in session"""
    data = request.get_json() or {}
    language = data.get('language', 'en')
    session['language'] = language
    return jsonify({'language': language})

@app.route('/add_task', methods=['POST'])
def add_task():
    """Add a new task"""
    try:
        data = request.get_json()
        title = data.get('title', '').strip()
        
        if not title:
            return jsonify({
                'success': False,
                'message': 'Please enter a task title!'
            }), 400
        
        tasks = load_tasks()
        new_task = {
            'id': get_next_task_id(tasks),
            'title': title,
            'completed': False,
            'created_at': datetime.now().isoformat()
        }
        
        tasks.append(new_task)
        save_tasks(tasks)
        
        return jsonify({
            'success': True,
            'message': 'Task added successfully!',
            'task': new_task
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error adding task: {str(e)}'
        }), 500

@app.route('/complete_task/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    """Mark a task as completed"""
    try:
        tasks = load_tasks()
        task = next((t for t in tasks if t['id'] == task_id), None)
        
        if not task:
            return jsonify({
                'success': False,
                'message': 'Task not found!'
            }), 404
        
        task['completed'] = not task['completed']  # Toggle completion status
        save_tasks(tasks)
        
        status = 'completed' if task['completed'] else 'uncompleted'
        return jsonify({
            'success': True,
            'message': f'Task {status} successfully!',
            'task': task
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error updating task: {str(e)}'
        }), 500

@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    """Delete a task"""
    try:
        tasks = load_tasks()
        task = next((t for t in tasks if t['id'] == task_id), None)
        
        if not task:
            return jsonify({
                'success': False,
                'message': 'Task not found!'
            }), 404
        
        tasks = [t for t in tasks if t['id'] != task_id]
        save_tasks(tasks)
        
        return jsonify({
            'success': True,
            'message': 'Task deleted successfully!'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error deleting task: {str(e)}'
        }), 500

if __name__ == '__main__':
    # Create tasks.json if it doesn't exist
    if not os.path.exists(_resolve_tasks_file()):
        save_tasks([])
    
    app.run(debug=app.config.get('DEBUG', True), host='0.0.0.0', port=5000)
