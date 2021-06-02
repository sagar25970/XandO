import json

from flask import Blueprint, render_template
from flask_login import current_user

from . import db
from .model import Room, Game
from .response import Response
from .service.dao_service import display_db

testing = Blueprint('testing', __name__)


@testing.route("/test", methods=['GET', 'POST'])
def test():
    game_state = Room.query.get(current_user.room_id).game
    print("Room State : \"" + game_state + "\"")
    return render_template("test-template.html", message='', state=game_state)


@testing.route("/reset", methods=['GET'])
def reset():
    Game.query.filter(Game.room_id == current_user.room_id).update({Game.game_state: '         '})
    db.session.commit()
    return {}


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
    return response_json


@testing.route("/test-api", methods=['GET', 'POST'])
def test_api():
    game_state = Room.query.get(current_user.room_id).game
    print("Room State : \"" + game_state + "\"")


@testing.route("/db", methods=['GET', 'POST'])
def db():
    display_db()
    return {}
