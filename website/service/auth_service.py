from flask import flash
from flask_login import login_user

from website import db
from website.model import Room
from website.service.dao_service import add_player, add_room
from website.service.game_service import initialise_game, get_game


def create_room_if_valid(request):
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        room_password = data.get('password')
        if room_valid(username, room_password):
            room = add_room(room_password)
            player = add_player(room.id, username)
            initialise_game(room.id)
            login_user(user=player, remember=True)
            return True
    return False


def join_room_if_valid(request):
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        room_id = data.get('roomId')
        room_password = data.get('password')
        if user_valid(room_id, username, room_password):
            player = add_player(room_id, username)
            db.session.commit()
            login_user(user=player, remember=True)
            return True
    return False


def room_valid(username, room_password):
    if len(username) < 1:
        flash('Username cannot be empty!', category='error')
        return False
    elif len(room_password) < 1:
        flash('Room password cannot be empty!', category='error')
        return False
    return True


def user_valid(room_id, username, room_password):
    room = Room.query.filter_by(id=room_id).first()
    if room:
        if len(username) < 1:
            flash('Username cannot be empty!', category='error')
            return False
        elif room.password != room_password:
            flash('Invalid Password!', category='error')
            return False
        elif any(room_players.username == username for room_players in room.players):
            flash('Username already present in room. Please select other username!', category='error')
            return False
        return True
    return False
