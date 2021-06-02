from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required

from . import db
from .model import Room, Player, Message, Game
from .service.auth_service import create_room_if_valid, join_room_if_valid

auth = Blueprint("auth", __name__)


@auth.route('/create-room', methods=['GET', 'POST'])
def create_room():
    if create_room_if_valid(request):
        return redirect(url_for('view.home'))
    return render_template('create-room.html', user=current_user)


@auth.route('/join-room', methods=['GET', 'POST'])
def join_room():
    if join_room_if_valid(request):
        return redirect(url_for('view.home'))
    return render_template('join-room.html', user=current_user)


@auth.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    room = Room.query.filter_by(id=current_user.room_id).first()
    players = room.players
    Player.query.filter_by(id=current_user.id).delete()
    if len(players) == 1:
        Message.query.filter_by(room_id=room.id).delete()
        Room.query.filter_by(id=current_user.room_id).delete()
        print('DB cleared!!!')
        Game.query.filter_by(room_id=current_user.room_id).delete()
    db.session.commit()
    logout_user()
    return redirect(url_for('auth.create_room'))



