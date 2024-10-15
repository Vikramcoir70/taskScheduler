from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Task
from datetime import datetime

task_bp = Blueprint('task', __name__)


@task_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    title = request.json.get('title')
    description = request.json.get('description')
    reminder_time = request.json.get('reminder_time')
    user_id = get_jwt_identity()['user_id']

    if reminder_time:
        reminder_time = datetime.fromisoformat(reminder_time)

    new_task = Task(title=title, description=description, user_id=user_id,
                    reminder_time=reminder_time)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"msg": "Task created successfully",
                    "task_id": new_task.id}), 201


@task_bp.route('/', methods=['GET'])
@jwt_required()
def get_tasks():
    current_user = get_jwt_identity()
    user_id = current_user['user_id']
    is_admin = current_user['is_admin']
    if is_admin:
        tasks = Task.query.all()
    else:
        tasks = Task.query.filter_by(user_id=user_id).all()

    return jsonify([{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'reminder_time': task.reminder_time.isoformat() if task.reminder_time else None,  # noqa
        'user_id': task.user_id
    } for task in tasks]), 200


@task_bp.route('/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    current_user = get_jwt_identity()
    user_id = current_user['user_id']
    is_admin = current_user['is_admin']

    if is_admin:
        task = Task.query.filter_by(id=task_id).first()
    else:
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if task is None:
        return jsonify({"msg": "Task not found"}), 404

    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'reminder_time': task.reminder_time.isoformat() if task.reminder_time else None,  # noqa
        'user_id': task.user_id
    }), 200


@task_bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    current_user = get_jwt_identity()
    user_id = current_user['user_id']
    is_admin = current_user['is_admin']

    task = Task.query.filter_by(id=task_id).first()

    if task is None:
        return jsonify({"msg": "Task not found"}), 404

    if not is_admin and task.user_id != user_id:
        return jsonify({"msg":
                        "You do not have permission to update this task"}), 403

    title = request.json.get('title', task.title)
    description = request.json.get('description', task.description)
    reminder_time = request.json.get('reminder_time', task.reminder_time)

    if reminder_time:
        reminder_time = datetime.fromisoformat(reminder_time)

    task.title = title
    task.description = description
    task.reminder_time = reminder_time
    db.session.commit()

    return jsonify({"msg": "Task updated successfully"}), 200


@task_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    current_user = get_jwt_identity()
    user_id = current_user['user_id']
    is_admin = current_user['is_admin']

    task = Task.query.filter_by(id=task_id).first()

    if task is None:
        return jsonify({"msg": "Task not found"}), 404

    if not is_admin and task.user_id != user_id:
        return jsonify({"msg":
                        "You do not have permission to delete this task"}), 403

    db.session.delete(task)
    db.session.commit()

    return jsonify({"msg": "Task deleted successfully"}), 200
