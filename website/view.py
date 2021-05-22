from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user

from . import db
from .auth import display_db
from .model import Message, Room

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


@view.route('/update', methods=['POST'])
def update():
    all_messages = db.session.query(Room).get(current_user.room_id).messages
    print("Called by : " + str(current_user.id))
    return jsonify('', render_template('chat.html', user=current_user, messages=all_messages))


@view.route("/select-box/<box_slot>", methods=['GET', 'POST'])
def select_box(box_slot):
    print("Box selected : " + box_slot)
    box_id = int(box_slot)
    room_game = Room.query.get(current_user.room_id).game
    room_game = ''.join((room_game[:box_id], 'X', room_game[box_id + 1:]))
    Room.query.filter(Room.id == current_user.room_id).update({Room.game: room_game})
    db.session.commit()
    room_game = Room.query.get(current_user.room_id).game
    print('Room State : "' + room_game + '"')
    return {'data': room_game}


@view.route("/test", methods=['GET', 'POST'])
def test():
    display_db()
    game_state = Room.query.get(current_user.room_id).game
    print("Room State : \"" + game_state + "\"")
    return render_template("test-template.html", message='', state=game_state)


@view.route("/testUpdate", methods=['GET', 'POST'])
def test_update():
    game_state = Room.query.get(current_user.room_id).game
    print("Test Update Room State : \"" + game_state + "\"")
    all_messages = db.session.query(Room).get(current_user.room_id).messages
    print(custom_jsonify(all_messages))
    return custom_jsonify(all_messages)


def custom_jsonify(messages):
    data = '{\n"message_data": [\n'
    for message in messages:
        data = data + message.__str__() + ','
    data = data[:-1] + ']\n}'
    return data

