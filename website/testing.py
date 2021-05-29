import json

from flask import Blueprint, render_template, request
from flask_login import current_user

from . import db
from .model import Room
from .response import Response

testing = Blueprint('testing', __name__)


@testing.route("/test", methods=['GET', 'POST'])
def test():
    game_state = Room.query.get(current_user.room_id).game
    print("Room State : \"" + game_state + "\"")
    return render_template("test-template.html", message='', state=game_state)


@testing.route("/test-update", methods=['GET', 'POST'])
def test_update():
    game_state = Room.query.get(current_user.room_id).game
    print("Test Update Room State : \"" + game_state + "\"")
    all_messages = db.session.query(Room).get(current_user.room_id).messages
    data = []
    for message in all_messages:
        data.__add__(message.to_json())
    response = Response('POST', 'test_update')
    response.data = data
    response_json = json.dumps(response.__dict__)
    print(response_json)
    return response_json


@testing.route("/api-call", methods=['GET', 'POST'])
def test_api_call():
    game_state = Room.query.get(current_user.room_id).game
    print("Test Update Room State : \"" + game_state + "\"")
    response_json = get_all_messages()
    return response_json


def get_all_messages():
    all_messages = db.session.query(Room).get(current_user.room_id).messages
    data = []
    for message in all_messages:
        data.append(message.to_json())
    response = Response(request.method, 'get-update')
    response.messages = data
    response_json = json.dumps(response.__dict__)
    print(response_json)
    return response_json
