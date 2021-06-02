import json

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from . import db
from .model import Message, Room
from .response import Response
from .service.game_service import update_game_state, reset_game, update_current_x, update_current_o, get_game, \
    update_turn

view = Blueprint("view", __name__)


@view.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        data = request.form.get('message')
        if len(data) > 1:
            message = Message(username=current_user.username, data=data, room_id=current_user.room_id)
            db.session.add(message)
            db.session.commit()
    all_messages = db.session.query(Room).get(current_user.room_id).messages
    return render_template('home.html', user=current_user, messages=all_messages)


@view.route("/update", methods=['GET', 'POST'])
def update():
    response_json = get_update_response()
    return response_json


@view.route("/select-box/<box_slot>", methods=['GET', 'POST'])
def select_box(box_slot):
    print("Box selected : " + box_slot)
    box_id = int(box_slot)
    game = get_game(current_user.room_id)
    response = Response(request.method, 'select_box')
    if current_user.username == game.current_turn:
        if current_user.username == game.current_x:
            update_game_state(current_user.room_id, 'X', box_id)
        else:
            update_game_state(current_user.room_id, 'O', box_id)
        response.status = '200'
        response.game = get_game(current_user.room_id).to_json()
    response_json = json.dumps(response.__dict__)
    return response_json


@view.route("/reset", methods=['GET'])
def reset():
    reset_game(current_user.room_id)
    return {}


@view.route("/player1", methods=['GET', 'POST'])
def choose_x():
    update_current_x(current_user.room_id, current_user.username)
    return {}


@view.route("/player2", methods=['GET', 'POST'])
def choose_o():
    update_current_o(current_user.room_id, current_user.username)
    return {}


def get_update_response():
    response = Response(request.method, 'get_update', '200')
    response.messages = get_all_messages()
    response.game = get_game(current_user.room_id).to_json()
    response_json = json.dumps(response.__dict__)
    return response_json


def get_all_messages():
    all_messages = db.session.query(Room).get(current_user.room_id).messages
    data = []
    for message in all_messages:
        data.append(message.to_json())
    return data
