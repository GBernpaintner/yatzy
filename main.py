from urllib.parse import urlparse

from flask import Flask, render_template, request, url_for, redirect
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
        'kept': [False, False, False, False, False] 
    }, '12345': {
        'values': [1,2,3,4,5],
        'counter': 0,
        'kept': [False, False, False, False, False]
    }
}


IMAGE_FOLDER = 'images'


COMBO_HEADERS = [ # in swedish since it's for family
    'Namn',
    'Ettor', 'Tvåor', 'Treor', 'Fyror', 'Femmor', 'Sexor',
    'Summa', 'Bonus', 'Ett par', 'Två par', 'Tretal', 'Fyrtal',
    'Liten stege', 'Stor stege', 'Kåk', 'Chans', 'Yatzy', 'Summa'
]


@app.route('/index')
@app.route('/')
def index():
    rooms = states.keys()
    return render_template('index.j2', rooms=rooms)


@app.route('/play/<room>')
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
    return render_template('play.j2', image_data=image_data,
                           counter=state['counter'], combo_headers=COMBO_HEADERS)


# -------------------- SocketIO -------------------- #


# All sids are stored along with the room they belong to.
rooms = {}


# Emittable events
UPDATE = 'update'


@socketio.event
def join(url):
    """
    url: The url from which the client made the connection contains
    the room for the socket.
    """
    room = urlparse(url).path.split('/')[-1]
    join_room(room)
    rooms[request.sid] = room


def do_action(f, *args, **kwargs):
    """Contains logic common to all actions

    Grabs the current sid's room and calls the action f with
    the correct state, updates the state, and emits an update.
    """
    room = rooms[request.sid]
    states[room] = f(*args, **kwargs, state=states[room])
    socketio.emit(UPDATE, states[room], room=room)


@socketio.on('roll')
def do_roll():
    do_action(roll)


@socketio.on('keep')
def do_keep(index):
    do_action(keep, index)


@socketio.on('reset')
def do_reset():
    do_action(reset)


# -------------------- Startup -------------------- #


if __name__ == '__main__':
    socketio.run(app, debug=True)
