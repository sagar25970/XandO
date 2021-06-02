from flask_login import UserMixin
from sqlalchemy.sql import func

from . import db


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(150))
    game = db.relationship('Game')
    players = db.relationship('Player')
    messages = db.relationship('Message')


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    game_state = db.Column(db.String(9))
    current_x = db.Column(db.String)
    current_o = db.Column(db.String)
    current_turn = db.Column(db.String)

    def to_json(self):
        return {"game_state": self.game_state, "current_x": self.current_x, "current_o": self.current_o, "current_turn": self.current_turn}


class Player(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    data = db.Column(db.String(1000))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    username = db.Column(db.String)

    def to_json(self):
        return {"username": self.username, "data": self.data}

