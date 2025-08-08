"""
Tests for the Todo App Flask application
"""

import pytest
import json
import tempfile
import os
from src.main import app


@pytest.fixture
def client(temp_tasks_file, monkeypatch):
    """Create a test client for the Flask application using a temp tasks file"""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    # Ensure the app reads and writes to the temporary tasks file
    monkeypatch.setenv('TASKS_FILE', temp_tasks_file)

    with app.test_client() as client:
        yield client


@pytest.fixture
def temp_tasks_file():
    """Create a temporary tasks file for testing"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump([], f)
        temp_file = f.name
    
    yield temp_file
    
    # Cleanup
    if os.path.exists(temp_file):
        os.unlink(temp_file)


def test_index_route(client):
    """Test the main index route"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data


def test_add_task(client):
    """Test adding a new task"""
    task_data = {'title': 'Test task'}
    response = client.post('/add_task', 
                          data=json.dumps(task_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'task' in data


def test_add_empty_task(client):
    """Test adding an empty task (should fail)"""
    task_data = {'title': ''}
    response = client.post('/add_task',
                          data=json.dumps(task_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False


def test_complete_task(client):
    """Test completing a task"""
    # First add a task
    task_data = {'title': 'Test task for completion'}
    add_response = client.post('/add_task',
                              data=json.dumps(task_data),
                              content_type='application/json')
    add_data = json.loads(add_response.data)
    task_id = add_data['task']['id']
    
    # Then complete it
    response = client.post(f'/complete_task/{task_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True


def test_delete_task(client):
    """Test deleting a task"""
    # First add a task
    task_data = {'title': 'Test task for deletion'}
    add_response = client.post('/add_task',
                              data=json.dumps(task_data),
                              content_type='application/json')
    add_data = json.loads(add_response.data)
    task_id = add_data['task']['id']
    
    # Then delete it
    response = client.post(f'/delete_task/{task_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True


def test_complete_nonexistent_task(client):
    """Test completing a task that doesn't exist"""
    response = client.post('/complete_task/999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['success'] is False


def test_delete_nonexistent_task(client):
    """Test deleting a task that doesn't exist"""
    response = client.post('/delete_task/999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['success'] is False 