from website import db
from website.model import Game


def initialise_game(room_id):
    game = Game(room_id=room_id, game_state='         ')
    db.session.add(game)
    db.session.commit()
    return game


def get_game(room_id):
    return Game.query.filter(Game.room_id == room_id).first()


def reset_game(room_id):
    game = get_game(room_id)
    game.game_state = '         '
    game.current_x = None
    game.current_o = None
    game.current_turn = None
    game.game_won = None
    db.session.commit()
    return game


def update_game_state(room_id, piece, box_id):
    game = get_game(room_id)
    game_state = game.game_state
    game_state = ''.join((game_state[:box_id], piece, game_state[box_id + 1:]))
    game.game_state = game_state
    update_turn(room_id)
    db.session.commit()


def update_current_x(room_id, username):
    game = get_game(room_id)
    if game.current_x is None:
        game.current_x = username
        game.current_turn = username
    db.session.commit()
    return game


def update_current_o(room_id, username):
    game = get_game(room_id)
    if game.current_o is None:
        game.current_o = username
    db.session.commit()
    return game


def update_turn(room_id):
    game = get_game(room_id)
    current_x = game.current_x
    current_o = game.current_o
    if game.current_turn == current_x:
        game.current_turn = current_o
    else:
        game.current_turn = current_x


def check_game_status(room_id, username):
    game = get_game(room_id)
    game_state = game.game_state
    if check_if_won(game_state):
        game.game_won = username
    if ' ' not in game_state:
        game.game_won = 'Draw'
    db.session.commit()


def check_if_won(game_state):
    return (check_three_in_a_line(game_state, 0, 1, 2)
            or check_three_in_a_line(game_state, 3, 4, 5)
            or check_three_in_a_line(game_state, 6, 7, 8)
            or check_three_in_a_line(game_state, 0, 3, 6)
            or check_three_in_a_line(game_state, 1, 4, 7)
            or check_three_in_a_line(game_state, 2, 5, 8)
            or check_three_in_a_line(game_state, 0, 4, 8)
            or check_three_in_a_line(game_state, 2, 4, 6)
            )


def check_three_in_a_line(game_state, index_1, index_2, index_3):
    if game_state[index_1] == game_state[index_2] == game_state[index_3]:
        return True
    return False

