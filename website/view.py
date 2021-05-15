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
    display_db()
    return render_template('home.html', user=current_user, messages=all_messages)


@view.route('/update', methods=['POST'])
def update():
    print('Reaching?')
    all_messages = db.session.query(Room).get(current_user.room_id).messages
    print('update called!')
    return jsonify('', render_template('chat.html', user=current_user, messages=all_messages))
