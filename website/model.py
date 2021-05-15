from flask_login import UserMixin
from sqlalchemy.sql import func

from . import db


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(150))
    players = db.relationship('Player')
    messages = db.relationship('Message')


class Player(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    data = db.Column(db.String(1000))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    username = db.Column(db.String)

    def serialize(self):
        return {
            'username': self.username,
            'data': self.data,
        }
