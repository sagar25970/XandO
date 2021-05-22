from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required

from . import db
from .model import Room, Player, Message

auth = Blueprint("auth", __name__)


@auth.route('/create-room', methods=['GET', 'POST'])
def create_room():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        room_password = data.get('password')
        if len(username) < 1:
            flash('Username cannot be empty!', category='error')
        elif len(room_password) < 1:
            flash('Room password cannot be empty!', category='error')
        else:
            room = Room(password=room_password, game='         ')
            db.session.add(room)
            db.session.flush()
            player = Player(username=username, room_id=room.id)
            db.session.add(player)
            db.session.commit()
            display_db()
            login_user(user=player, remember=True)
            return redirect(url_for('view.home'))
    display_db()
    return render_template('create-room.html', user=current_user)


@auth.route('/join-room', methods=['GET', 'POST'])
def join_room():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        room_id = data.get('roomId')
        room_password = data.get('password')
        room = Room.query.filter_by(id=room_id).first()
        if room:
            if len(username) < 1:
                flash('Username cannot be empty!', category='error')
            else:
                if room.password != room_password:
                    flash('Invalid Password!', category='error')
                else:
                    player = Player(username=username, room_id=room_id)
                    db.session.add(player)
                    db.session.flush()
                    db.session.commit()
                    login_user(user=player, remember=True)
                    return redirect(url_for('view.home'))
    display_db()
    return render_template('join-room.html', user=current_user)


@auth.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    display_db()
    room = Room.query.filter_by(id=current_user.room_id).first()
    players = room.players
    Player.query.filter_by(id=current_user.id).delete()
    if len(players) == 1:
        Message.query.filter_by(room_id=room.id).delete()
        Room.query.filter_by(id=current_user.room_id).delete()
        print('DB cleared!!!')
    db.session.commit()
    display_db()
    logout_user()
    return redirect(url_for('auth.create_room'))


def display_db():
    print('Displaying DB')
    rooms = Room.query.all()
    players = Player.query.all()
    messages = Message.query.all()
    print('Room ID\t\tRoom Password\t\tRoom Game')
    for room in rooms:
        print(str(room.id) + '\t\t\t' + room.password + '\t\t\t' + room.game)
    print('\n')

    print('Player ID\t\tPlayer Username')
    for player in players:
        print(str(player.id) + '\t\t\t' + player.username)
    print('\n')

    print('Message ID\t\tMessage\t\tRoom ID')
    for message in messages:
        print(str(message.id) + '\t\t\t' + message.data + '\t\t\t' + str(message.room_id))
    print('\n')
