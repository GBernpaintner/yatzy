from urllib.parse import urlparse
from uuid import uuid4
from functools import wraps

from flask import Flask, render_template, request, url_for, redirect, make_response
from flask_socketio import SocketIO, join_room

from game import roll, keep, reset


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sercrutkee'
socketio = SocketIO(app)


# -------------------- Web Pages -------------------- #


# The keys are the socketio room names that are also 
# used in the url as the <room> in the route play
states = {
    'asdf': {
        'values': [1,5,1,5,1],
        'counter': 0,
        'kept': [False, False, False, False, False],
        'player_ids': [],
        'player_names': {},
        'has_started': False
    }, '12345': {
        'values': [1,2,3,4,5],
        'counter': 0,
        'kept': [False, False, False, False, False],
        'player_ids': [],
        'player_names': {},
        'has_started': False
    }
}


IMAGE_FOLDER = 'images'


COMBO_HEADERS = [ # in swedish since it's for family
    'Namn',
    'Ettor', 'Tvåor', 'Treor', 'Fyror', 'Femmor', 'Sexor',
    'Summa', 'Bonus', 'Ett par', 'Två par', 'Tretal', 'Fyrtal',
    'Liten stege', 'Stor stege', 'Kåk', 'Chans', 'Yatzy', 'Summa'
]


class OVERLAY:
    """Constants for the overlay css classes"""
    ACTIVE = 'active'
    INACTIVE = 'inactive'


# Generate a unique id for users to be stored as cookies
def generate_unique_id():
    return str(uuid4())


def generate_player_id(route):
    """
    Generate a user id cookie if one does not exist.
    Use as a decorator for all routes.
    """
    @wraps(route)
    def wrapper(*args, **kwargs):
        if 'player_id' not in request.cookies:
            response = make_response(route(*args, **kwargs))
            response.set_cookie('player_id', generate_unique_id(), max_age=60*60*24*365*10)
            return response
        return route(*args, **kwargs)
    return wrapper


def generate_scoresheet(state):
    scoresheet = []
    scoresheet.append({
        'header': COMBO_HEADERS[0],
        'cells': [state['player_names'][player_id] for player_id in state['player_ids']]
    })
    for header in COMBO_HEADERS[1:]:
        scoresheet.append({
            'header': header,
            'cells': [None] * len(state['player_ids'])
        })
    return scoresheet


@app.route('/index')
@app.route('/')
@generate_player_id
def index():
    rooms = states.keys()
    return render_template('index.j2', rooms=rooms)


@app.route('/play/<room>')
@generate_player_id
def play(room):
    try:
        state = states[room]
    except KeyError:
        return redirect(url_for('index'), 302)
    image_data = []
    for i, value, kept in zip(range(len(state['values'])), state['values'], state['kept']):
        image_data.append({
            'index': i,
            'filename': f'{IMAGE_FOLDER}/{value}.png',
            'kept': 'kept' if kept else ''
        })
    scoresheet = generate_scoresheet(state)
    should_show_overlay = request.cookies.get('player_id') not in state['player_ids']
    show_overlay = OVERLAY.ACTIVE if should_show_overlay else OVERLAY.INACTIVE
    return render_template('play.j2',
                           image_data=image_data,
                           counter=state['counter'],
                           scoresheet=scoresheet,
                           show_overlay=show_overlay)


# -------------------- SocketIO -------------------- #


# All sids are stored along with the room they belong to.
rooms = {}


# Emittable events
UPDATE = 'update'
GAME_STARTED = 'game_started'


@socketio.event
def join(url):
    """
    url: The url from which the client made the connection contains
    the room for the socket.
    """
    room = urlparse(url).path.split('/')[-1]
    join_room(room)
    rooms[request.sid] = room


def do_game_action(f, *args, **kwargs):
    """Contains logic common to all actions

    Grabs the current sid's room and calls the action f with
    the correct state, updates the state, and emits an update.
    """
    room = rooms[request.sid]
    states[room] = f(*args, **kwargs, state=states[room])
    socketio.emit(UPDATE, states[room], room=room)


@socketio.on('roll')
def do_roll():
    do_game_action(roll)


@socketio.on('keep')
def do_keep(index):
    do_game_action(keep, index)


@socketio.on('reset')
def do_reset():
    do_game_action(reset)


@socketio.on('join_game')
def do_join_game(player_name):
    room = rooms[request.sid]
    state = states[room]
    player_id = request.cookies.get('player_id')
    if player_id not in state['player_ids']:
        print(f'{player_name} joined the game in room {room}')
        state_update = {
            'player_ids': [*state['player_ids'], player_id],
            'player_names': {**state['player_names'], player_id: player_name}
        }
        states[room] = {**state, **state_update}
        socketio.emit(UPDATE, states[room], room=room)


# -------------------- Startup -------------------- #


if __name__ == '__main__':
    # TODO: on server, use debug=False
    socketio.run(app, debug=True)
