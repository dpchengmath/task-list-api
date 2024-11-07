from flask import abort, make_response
from ..db import db
import os
import requests


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} id {(model_id)} invalid"}, 400))
    
    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        abort(make_response({ "message": f"{cls.__name__} {model_id} not found"}, 404))
    
    return model


def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
        # new_model = {"{cls.__name__}": cls.from_dict(model_data)}
    
    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))
    
    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201


def get_models_with_filters(cls, filters=None):
    query = db.select(cls)

    if filters:
        for attribute, value in filters.items():
            if hasattr(cls, attribute):
                query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))
    
    models = db.session.scalars(query.order_by(cls.id))
    models_response = [model.to_dict() for model in models]

    return models_response


def post_slack_message(task):

    url = "https://slack.com/api/chat.postMessage"

    token = os.environ.get("SLACK_BOT_TOKEN")
    headers = {"Authorization": f"Bearer {token}"}
    request_body = {
        "channel": "api-test-channel",
        "text": f"Someone just completed the task {task.title}"
        }

    notification = requests.post(url, headers=headers, json=request_body)

    return notification