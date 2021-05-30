import json

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from . import db
from .auth import display_db
from .model import Message, Room, Game
from .response import Response

view = Blueprint("view", __name__)


@view.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        data = request.form.get('message')
        if len(data) > 1:
            message = Message(username=current_user.username, data=data, room_id=current_user.room_id,
                              player_id=current_user.id)
            db.session.add(message)
            db.session.commit()
    all_messages = db.session.query(Room).get(current_user.room_id).messages
    return render_template('home.html', user=current_user, messages=all_messages)


@view.route("/update", methods=['GET', 'POST'])
def test_api_call():
    display_db()
    response_json = get_update_response()
    return response_json


@view.route("/select-box/<box_slot>", methods=['GET', 'POST'])
def select_box(box_slot):
    print("Box selected : " + box_slot)
    box_id = int(box_slot)
    room_game = Room.query.get(current_user.room_id).game[0]
    game_state = room_game.game_state
    print("game state - " + game_state)
    if current_user.username == room_game.current_x:
        game_state = ''.join((game_state[:box_id], 'X', game_state[box_id + 1:]))
    else:
        game_state = ''.join((game_state[:box_id], 'O', game_state[box_id + 1:]))

    Game.query.filter(Game.room_id == current_user.room_id).update({Game.game_state: game_state})
    db.session.commit()
    response = Response(request.method, 'select_box')
    response.game = get_game()
    response_json = json.dumps(response.__dict__)
    print(response_json)
    return response_json


def get_update_response():
    response = Response(request.method, 'get_update')
    response.messages = get_all_messages()
    response.game = get_game()
    response_json = json.dumps(response.__dict__)
    print(response_json)
    return response_json


def get_game():
    return Room.query.get(current_user.room_id).game[0].to_json()


def get_all_messages():
    all_messages = db.session.query(Room).get(current_user.room_id).messages
    data = []
    for message in all_messages:
        data.append(message.to_json())
    return data
