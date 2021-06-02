from website import db
from website.model import Player, Room, Message, Game


def add_room(room_password):
    room = Room(password=room_password)
    db.session.add(room)
    db.session.commit()
    return room


def add_player(room_id, player_username):
    player = Player(room_id=room_id, username=player_username)
    db.session.add(player)
    db.session.commit()
    return player


def display_db():
    print('Displaying DB')
    rooms = Room.query.all()
    players = Player.query.all()
    messages = Message.query.all()
    games = Game.query.all()
    print('Room ID\t\tRoom Password\t\tRoom Game')
    for room in rooms:
        print(str(room.id) + '\t\t\t' + room.password + '\t\t\t')
    print('\n')

    print('Player ID\t\tPlayer Username')
    for player in players:
        print(str(player.id) + '\t\t\t' + player.username)
    print('\n')

    print('Message ID\t\tMessage\t\tRoom ID')
    for message in messages:
        print(str(message.id) + '\t\t\t' + message.data + '\t\t\t' + str(message.room_id))
    print('\n')

    print('Game Id\t\tMessage\t\tRoom ID')
    for game in games:
        print(game.to_json())
    print('\n')
