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

# board = make_board()
# board = Game()
@app.route('/pageOne')
def stronaOne():
    return render_template('pageOne.html')
#
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = GameForm()
#     if form.validate_on_submit():
#         global playerOn
#         global playerTw
#         playerOn = Player(name=form.playerOne.data)
#         playerTw = Player(name=form.playerTwo.data)
#         return redirect(url_for('pageGame'))
#     return render_template('form.html', title='Form', form=form)

@app.route('/pageGame', methods=['GET', 'POST'])
def pageGame():
    global board
    board = Game()
    # nameOne = requests.post('register', 'playerOne')
    # nameTwo = requests.post('register', 'playerTwo')
    # print(playerOn.name)
    # print(playerTw.name)
    global player1
    global player2
    player1 = Player('Ana')
    player2 = Player('two')
    return render_template('pageGame.html', poles=board.poles)

@app.route('/move/<int:id>')
def move(id):
    # global board
    # board = pageGame()
    # polowaOne = []
    # polowaTwo = []
    # el = 6
    # for n in range(8, 13):
    #     polowaOne.append(board.poles[n])
    #
    # for k in range(1, 6):
    #     polowaTwo.append(board.poles[k])
    #
    start = id
    ilosc = board.poles[id] #ilosc = 4 id =3
    lastp = (start + ilosc)%14
    opp_lastp = 14 - lastp
    board.poles[id] = 0 #empty one which waas start
    while (ilosc > 0):
        if (ilosc == 1):
            if ((board.poles[lastp] == 0) & (lastp != 0) & (lastp != 7)):
                board.poles[7] += board.poles[opp_lastp]
                board.poles[opp_lastp] = 0
                board.poles[7] += 1
                board.poles[id] = 0
                ilosc = 0
            else:
                id += 1
                id %= 14
                board.poles[id] += 1
                ilosc = 0
        else:
            id += 1
            id %= 14
            board.poles[id] += 1
            ilosc -= 1
    if ((board.poles[8] == 0) & (board.poles[9] == 0) & (board.poles[10] == 0) & (board.poles[11] == 0) & (board.poles[12] == 0) & (board.poles[13] == 0)):
        for k in range(1, 6):
            board.poles[7] += board.poles[k]
        return redirect(url_for('endGame'))
    if ((board.poles[1] == 0) & (board.poles[2] == 0) & (board.poles[3] == 0) & (board.poles[4] == 0) & (board.poles[5] == 0) & (board.poles[6] == 0)):
        for a in range(8, 13):
            board.poles[0] += board.poles[a]
        return redirect(url_for('endGame'))
    return render_template('pageGame.html', poles=board.poles)

@app.route('/endgame')
def endGame():
    if board.poles[7] > board.poles[0]:
        print('PlayerTwo wins!')
    if board.poles[7] < board.poles[0]:
        print('PlayerOne wins!')
    if board.poles[7] == board.poles[0]:
        print('Its a draw!')
    return render_template('endGame.html')












if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5130, debug=True)