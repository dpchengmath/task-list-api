from flask import Blueprint, abort, make_response, Response, request
from .route_utilities import validate_model, create_model, get_models_with_filters
from ..db import db
from app.models.goal import Goal
from app.models.task import Task
from sqlalchemy import asc, desc
from datetime import datetime
import pytz


goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


@goals_bp.post("")
def create_goal():
    request_body = request.get_json()

    if not "title" in request_body:
        response_body = {"details": "Invalid data"}
        return make_response(response_body, 400)

    new_goal = Goal.from_dict(request_body)
    db.session.add(new_goal)
    db.session.commit()

    response_body = {"goal": new_goal.to_dict()}
    
    return response_body, 201


@goals_bp.get("")
def get_all_goals():
    return get_models_with_filters(Goal, request.args)


@goals_bp.get("/<goal_id>")
def get_one_task(goal_id):
    goal = validate_model(Goal, goal_id)
    response_body = {"goal": goal.to_dict()}
    return response_body


@goals_bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    goal.title = request_body.get("title", goal.title)
    db.session.commit()

    response_body = {"goal": goal.to_dict()}

    return make_response(response_body, 200)


@goals_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)  
    db.session.delete(goal)
    db.session.commit()

    response_body = {
        "details": f'Goal {goal.id} "{goal.title}" successfully deleted'
    }
    return make_response(response_body, 200)


@goals_bp.post("/<goal_id>/tasks")
def post_task_ids_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    tasks = request_body.get("task_ids")
    tasks_list = []

    for task in tasks:
        task = validate_model(Task, task)
        tasks_list.append(task)

    goal.tasks = tasks_list
    db.session.commit()

    task_ids = [task.id for task in goal.tasks]

    response = {
        "id": goal.id,
        "task_ids": task_ids
    }

    return response, 200


@goals_bp.get("/<goal_id>/tasks")
def get_tasks_for_specific_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks_response = [
        {
            "id": task.id,
            "goal_id": task.goal_id,
            "description": task.description,
            "is_complete": task.completed_at if task.completed_at else False,
            "title": task.title
        }
        for task in goal.tasks
    ]

    response = {
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks_response
    }
  
    return response, 200


@goals_bp.get("/<task_id>")
def get_tasks_includes_goal_id(task_id):
    task = validate_model(Task, task_id)
    goal = task.goal

    goal_id = goal.id if goal else None

    response_body = {
        "task": {
            "id": task.id,
            "goal_id": goal.id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.completed_at if task.completed_at else False
        }
    }

    return response_body, 200