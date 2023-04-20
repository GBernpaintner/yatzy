//-------------------- Constants --------------------//


const IMAGES_URL = '/static/images'

const COMBO_HEADERS = [ // in swedish since it's for family
    'Namn',
    'Ettor', 'Tvåor', 'Treor', 'Fyror', 'Femmor', 'Sexor',
    'Summa', 'Bonus', 'Ett par', 'Två par', 'Tretal', 'Fyrtal',
    'Liten stege', 'Stor stege', 'Kåk', 'Chans', 'Yatzy', 'Summa'
]


//-------------------- Helpers --------------------//


// https://stackoverflow.com/questions/5639346/what-is-the-shortest-function-for-reading-a-cookie-by-name-in-javascript
const getCookieValue = (name) => (
    document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)')?.pop() || ''
)

function updateOverlay(state) {
    let player_id = getCookieValue('player_id')
    // If the player is in the game,
    // or the game has already started, hide the overlay
    if (state.player_ids.includes(player_id) || state.has_started) {
        let overlay = document.getElementsByClassName('overlay')[0]
        overlay.classList.remove('active')
        overlay.classList.add('inactive')
    } else {
        let overlay = document.getElementsByClassName('overlay')[0]
        overlay.classList.remove('inactive')
        overlay.classList.add('active')
    }
}

function updateScoresheet(state) {
    // create scoresheet
    let scoresheet = []
    let player_names = []
    for (let player_id of state.player_ids) {
        player_names.push(state.player_names[player_id])
    }
    scoresheet.push({
        'header': COMBO_HEADERS[0],
        'cells': player_names
    })
    for (let header of COMBO_HEADERS.slice(1)) {
        scoresheet.push({
            'header': header,
            'cells': [null] * state.player_ids.length
        })
    }
    
    // populate scoresheet
    const table = document.getElementById('scoresheet')
    // add extra columns if needed
    if (table.rows[0].cells.length < player_names.length + 1) {
        for (let i = 0; i < table.rows.length; i++) {
            let row = table.rows[i]
            for (let j = row.cells.length; j < player_names.length + 1; j++) {
                row.insertCell(-1)
            }
        }
    }
    for (let i = 0; i < table.rows.length; i++) {
        let row = table.rows[i]
        for (let j = 0; j < row.cells.length; j++) {
            let cell = row.cells[j]
            if (j == 0) {
                cell.textContent = scoresheet[i]['header']
            } else {
                cell.textContent = scoresheet[i]['cells'][j - 1]
            }
        }
    }
    

}

function updateVisuals(state) {
    getDiceImages().forEach(dice => {
        diceNumber = getIndex(dice)
        if (state.kept[diceNumber]) {
            dice.classList.add('kept')
        } else {
            dice.classList.remove('kept')
        }
        dice.src = `${IMAGES_URL}/${state.values[diceNumber]}.png`
    })
    document.getElementById('throw-counter').textContent = state.counter
}


//-------------------- SocketIO --------------------// 


const socket = io();

socket.on('connect', () => {
    socket.emit('join', document.URL)
});

let state = {}
socket.on('update', newState => {
    state = {...state, ...newState}
    updateOverlay(state)
    updateScoresheet(state)
    updateVisuals(state)
})


//-------------------- Interface --------------------// 


function roll() {
    socket.emit('roll')
}

function keep(index) {
    socket.emit('keep', index)
}

function reset() {
    socket.emit('reset')
}


//-------------------- Overlay --------------------//


function joinGame() {
    let name = document.getElementById('player-name').value
    if (name) {
        socket.emit('join_game', name)
    }  
}


//-------------------- Dice --------------------//


function getIndex(element) {
    return parseInt(element.attributes['index'].value)
}

function getDiceImages() {
    let diceImages = document.getElementsByClassName('dice')
    return diceImages = Array.prototype.slice.call(diceImages, 0);
}

const images = []
function preloadImages() {
    for (let i = 1; i <= 6; i++) {
        images.push(new Image())
        images[i - 1].src = `${IMAGES_URL}/${i}.png`
    }
}

preloadImages()
