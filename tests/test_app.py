import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app import app, db # noqa
import pytest # noqa


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


@pytest.fixture
def jwt_token(client):

    user_data = {
        'username': 'test',
        'email': 'testuser@example.com',
        'password': 'testpassword'
    }
    client.post('/api/auth/register', json=user_data)
    response = client.post('/api/auth/login', json={
        'username': 'test',
        'password': 'testpassword'
    })
    return response.json['access_token']


def test_create_task(client, jwt_token):
    headers = {'Authorization': f'Bearer {jwt_token}'}
    response = client.post('/api/tasks/', json={
        'title': 'task',
        'description': 'T=sadas',
        'reminder_time': '2024-10-20T10:00:00'
    }, headers=headers)
    assert response.status_code == 201
    assert 'task_id' in response.json


def test_get_tasks(client, jwt_token):
    headers = {'Authorization': f'Bearer {jwt_token}'}
    client.post('/api/tasks/', json={
        'title': 'task',
        'description': 'T=sadas',
        'reminder_time': '2024-10-20T10:00:00'
    }, headers=headers)

    response = client.get('/api/tasks/', headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) > 0


def test_get_task(client, jwt_token):
    headers = {'Authorization': f'Bearer {jwt_token}'}
    response = client.post('/api/tasks/', json={
        'title': 'task',
        'description': 'T=sadas',
        'reminder_time': '2024-10-20T10:00:00'
    }, headers=headers)

    task_id = response.json['task_id']
    response = client.get(f'/api/tasks/{task_id}', headers=headers)
    assert response.status_code == 200
    assert response.json['id'] == task_id


def test_update_task(client, jwt_token):
    headers = {'Authorization': f'Bearer {jwt_token}'}
    response = client.post('/api/tasks/', json={
        'title': 'task',
        'description': 'T=sadas',
        'reminder_time': '2024-10-20T10:00:00'
    }, headers=headers)

    task_id = response.json['task_id']
    update_response = client.put(f'/api/tasks/{task_id}', json={
        'title': 'Updated Task Title',
        'description': 'Updated T=sadas',
        'reminder_time': '2024-10-21T10:00:00'
    }, headers=headers)

    assert update_response.status_code == 200
    assert update_response.json['msg'] == 'Task updated successfully'


def test_delete_task(client, jwt_token):
    headers = {'Authorization': f'Bearer {jwt_token}'}
    response = client.post('/api/tasks/', json={
        'title': 'My Task',
        'description': 'Task Description',
        'reminder_time': '2024-10-20T10:00:00'
    }, headers=headers)

    task_id = response.json['task_id']
    delete_response = client.delete(f'/api/tasks/{task_id}', headers=headers)
    assert delete_response.status_code == 200
    assert delete_response.json['msg'] == 'Task deleted successfully'


def test_get_nonexistent_task(client, jwt_token):
    headers = {'Authorization': f'Bearer {jwt_token}'}
    response = client.get('/api/tasks/999', headers=headers)
    assert response.status_code == 404
    assert response.json['msg'] == 'Task not found'


def test_update_nonexistent_task(client, jwt_token):
    headers = {'Authorization': f'Bearer {jwt_token}'}
    response = client.put('/api/tasks/999', json={
        'title': 'Nonexistent Task',
        'description': 'T=sadas',
        'reminder_time': '2024-10-21T10:00:00'
    }, headers=headers)
    assert response.status_code == 404
    assert response.json['msg'] == 'Task not found'


def test_delete_nonexistent_task(client, jwt_token):
    headers = {'Authorization': f'Bearer {jwt_token}'}
    response = client.delete('/api/tasks/999', headers=headers)
    assert response.status_code == 404
    assert response.json['msg'] == 'Task not found'
