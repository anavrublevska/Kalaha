from flask import Flask, render_template, redirect, url_for
from forms import GameForm
app = Flask(__name__)


app.config['SECRET_KEY'] = 'fknv678fdvc'

class Game:
    def __init__(self):
        self.poles = [0, 4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4]

class Player:
    def __init__(self, name):
        self.name = name

def starting():
    global gra
    global board
    global turn
    board = Game()
    global player1
    global player2



# board = make_board()
# board = Game()
@app.route('/')
def stronaOne():
    return render_template('pageOne.html')
#
@app.route('/register', methods=['GET', 'POST'])
def register():
    global player1
    global player2
    form = GameForm()
    if form.validate_on_submit():
        player1 = Player(name=form.playerOne.data)
        player2 = Player(name=form.playerTwo.data)
        return redirect(url_for('pageGame'))
    return render_template('form.html', title='Form', form=form)

@app.route('/pageGame', methods=['GET', 'POST'])
def pageGame():
    # global board was
    # board = Game() was
    global board
    starting()
    global player1
    global player2
    global players
    global turn
    global playerName
    turn = 0
    players = [player1, player2]
    playerName = players[turn].name
    return render_template('pageGame.html', poles=board.poles, playerName=playerName, player1=player1, player2=player2, board=board, turn=turn)

@app.route('/move/<int:id>', methods=['GET', 'POST'])
def move(id):

    global playerName
    global turn
    global players
    global changeTurn

    changeTurn = True

    strona0 = [8,9,10,11,12,13]
    strona1 = [1,2,3,4,5,6]

    start = id #start to startowe pole
    ilosc = board.poles[id] #ilosc kamieni
    lastp = (start + ilosc) % 14 #ostatnie pole
    opp_lastp = (14 - lastp) % 14 #opposite ostatniegopola
    board.poles[id] = 0 #empty one which was start

    while (ilosc > 0):
        if (ilosc == 1): #ostatni kamyk
            if ((lastp == 0) or (lastp == 7)):
                if (lastp == 0): #dim of player0
                    if (turn == 0): #kolej gracza 0 => nie zmienia sie turn
                        changeTurn = False
                    id += 1
                    id %= 14
                    board.poles[id] += 1
                    ilosc = 0
                if (lastp == 7): #dim of player1
                    if (turn == 1): #kolej gracza 1
                        changeTurn = False #nie zmienia sie turn
                    id += 1
                    id %= 14
                    board.poles[id] += 1
                    ilosc = 0
            else: #eto obycznoe pole
                if (board.poles[lastp] == 0): #puste
                    if (board.poles[opp_lastp] != 0): #opposite niepuste
                        if ((lastp in strona0) and (turn == 0)):
                            board.poles[0] += board.poles[opp_lastp]  # trafia do domu gracza 1 jesli to byl jego ruch
                            board.poles[0] += 1
                            board.poles[opp_lastp] = 0
                            board.poles[lastp] = 0
                            ilosc = 0
                            changeTurn = False
                        elif ((lastp in strona1) and (turn == 1)):
                            board.poles[7] += board.poles[opp_lastp]  # trafia do domu gracza 1 jesli to byl jego ruch
                            board.poles[7] += 1
                            board.poles[opp_lastp] = 0
                            board.poles[lastp] = 0
                            ilosc = 0
                            changeTurn = False
                        else:
                            id += 1
                            id %= 14
                            board.poles[id] += 1
                            ilosc -= 1
                            changeTurn = True
                    else: # opposite puste
                        id += 1
                        id %= 14
                        board.poles[id] += 1
                        ilosc -= 1
                        changeTurn = True
                else: #nepuste
                    id += 1
                    id %= 14
                    board.poles[id] += 1
                    ilosc -= 1
                    changeTurn = True
        else:
           id += 1
           id %= 14
           board.poles[id] += 1
           ilosc -= 1


    if ((board.poles[8] == 0) & (board.poles[9] == 0) & (board.poles[10] == 0) & (board.poles[11] == 0) & (board.poles[12] == 0) & (board.poles[13] == 0)):
        for k in range(0, 6):
            board.poles[7] += board.poles[k]
        sum = board.poles[7]
        return redirect(url_for('endGame', sum=sum))
    if ((board.poles[1] == 0) & (board.poles[2] == 0) & (board.poles[3] == 0) & (board.poles[4] == 0) & (board.poles[5] == 0) & (board.poles[6] == 0)):
        for a in range(8, 13):
            board.poles[0] += board.poles[a]
        sum = board.poles[0]
        return redirect(url_for('endGame', sum=sum))
    if (changeTurn == True):
        turn = (turn+1) % 2

    playerName = players[turn].name

    return render_template('pageGame.html', poles=board.poles, playerName=playerName, turn=turn)

@app.route('/endgame')
def endGame():
    global winner
    if board.poles[7] > board.poles[0]:
        winner = 'PlayerTwo wins!'
    if board.poles[7] < board.poles[0]:
        winner = 'PlayerOne wins!'
    if board.poles[7] == board.poles[0]:
        winner = 'Its a draw!'
    return render_template('endGame.html', winner=winner)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5130, debug=True)