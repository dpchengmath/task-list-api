from flask import Blueprint, abort, make_response, Response, request
from app.models.task import Task
from app.db import db
from sqlalchemy import asc, desc


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@tasks_bp.get("")
def get_all_tasks():
    query = db.select(Task)

    title_param_key = request.args.get("sort")

    if title_param_key == "asc":
        query = query.order_by(asc(Task.title))
    elif title_param_key == "desc":
        query = query.order_by(desc(Task.title))

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Task.title.ilike(f"%{title_param}%"))

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Task.description.ilike(f"%{description_param}%"))

    is_complete_param = request.args.get("is_complete")
    if is_complete_param:
        query = query.where(Task.is_complete.ilike(f"%{is_complete_param}%"))
 
    query = query.order_by(Task.id)
    tasks = db.session.scalars(query)

    task_response_body = [task.task_dictionary() for task in tasks]
    # task_response_body = []

    # for task in tasks:
    #     task_response_body.append(task.task_dictionary())
    return task_response_body


# @tasks_bp.get("")
# def get_all_tasks():
#     query = db.select(Task).order_by(Task.id)
#     tasks = db.session.scalars(query)
#     response_body = [task.task_dictionary() for task in tasks]
#     return response_body


@tasks_bp.post("")
def create_task():
    request_body = request.get_json()

    if not "title" in request_body or not "description" in request_body:
        response_body = {"details": "Invalid data"}
        return make_response(response_body, 400)

    title = request_body["title"]
    description = request_body["description"]
    # is_complete = request_body["is_complete"]

    new_task = Task(title=title, description=description)
    db.session.add(new_task)
    db.session.commit()

    response_body = {
        "task": new_task.task_dictionary()
    }

    return response_body, 201


@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_task(task_id)
    response_body = {"task": task.task_dictionary()}
    return response_body


@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()
    task.title = request_body.get("title", task.title)
    task.description = request_body.get("description", task.description)
    task.is_complete = request_body.get("is_complete", task.is_complete)
    db.session.commit()

    response_body = {
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
        }
    }
    return make_response(response_body, 200)


@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_task(task_id)  
    db.session.delete(task)
    db.session.commit()

    response_body = {
        "details": f'Task {task.id} "{task.title}" successfully deleted'
    }
    return make_response(response_body, 200)

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        response_body = {"message": f"task {task_id} invalid"}
        abort(make_response(response_body , 400))

    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)
    
    if not task:
        response_body = {"message": f"task {task_id} not found"}
        abort(make_response(response_body, 404))

    return task