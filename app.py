from flask import Flask, render_template, redirect, url_for
from forms import GameForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'fknv678fdvc'


class Game:
    def __init__(self, player1, player2):
        self.number = 1
        self.poles = [0, 4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4]
        self.turn = 0
        self.playerOne = player1
        self.playerTwo = player2
        self.players = []
        self.winner = 'none'


class Player:
    global chosenForCPU
    global board
    def __init__(self, name):
        self.name = name
        self.summary = 0

    def choosePole(self):
        myPola = [6, 5, 4, 3, 2, 1]
        notEmpty = []
        empty = []

        for el in myPola:
            if board.poles[el] != 0:
                notEmpty.append(el)
            else:
                empty.append(el)

        chosenForCPU = notEmpty[0]


        for m in empty:
            mOpposite = (14 - m) % 14
            for a in notEmpty:
                porownanie = (board.poles[a] + a) % 14 # tu sprawdzam czy starczy koamykow
                if porownanie == m and mOpposite != 0:
                    chosenForCPU = a
                    return chosenForCPU
        else:
            for k in notEmpty:
                iloscKamykow = board.poles[k]
                if (k + iloscKamykow == 7):
                    chosenForCPU = k
                    return chosenForCPU


        return chosenForCPU


    def move(self, id):
        global board
        global playerName
        global turn
        global players
        global changeTurn
        global winner
        # i fmamy id, a jesli nie ma id to pusta plansza
        changeTurn = True

        strona0 = [8, 9, 10, 11, 12, 13]
        strona1 = [1, 2, 3, 4, 5, 6]

        start = id  # start to startowe pole
        ilosc = board.poles[id]  # ilosc kamieni
        lastp = (start + ilosc) % 14  # ostatnie pole
        opp_lastp = (14 - lastp) % 14  # opposite ostatniegopola
        board.poles[id] = 0  # empty one which was start

        while (ilosc > 0):
            if (ilosc == 1):  # ostatni kamyk
                if ((lastp == 0) or (lastp == 7)):
                    if (lastp == 0):  # dim of player0
                        if (turn == 0):  # kolej gracza 0 => nie zmienia sie turn
                            changeTurn = False
                        id += 1
                        id %= 14
                        board.poles[id] += 1
                        ilosc = 0
                    if (lastp == 7):  # dim of player1
                        if (turn == 1):  # kolej gracza 1
                            changeTurn = False  # nie zmienia sie turn
                        id += 1
                        id %= 14
                        board.poles[id] += 1
                        ilosc = 0
                else:  # eto obycznoe pole
                    if (board.poles[lastp] == 0):  # puste
                        if (board.poles[opp_lastp] != 0):  # opposite niepuste
                            if ((lastp in strona0) and (turn == 0)):
                                board.poles[0] += board.poles[
                                    opp_lastp]  # trafia do domu gracza 1 jesli to byl jego ruch
                                board.poles[0] += 1
                                board.poles[opp_lastp] = 0
                                board.poles[lastp] = 0
                                ilosc = 0
                                changeTurn = False
                            elif ((lastp in strona1) and (turn == 1)):
                                board.poles[7] += board.poles[
                                    opp_lastp]  # trafia do domu gracza 1 jesli to byl jego ruch
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
                        else:  # opposite puste
                            id += 1
                            id %= 14
                            board.poles[id] += 1
                            ilosc -= 1
                            changeTurn = True
                    else:  # nepuste
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

        # if ((board.poles[8] == 0) and (board.poles[9] == 0) and (board.poles[10] == 0) and (board.poles[11] == 0) and (
        #         board.poles[12] == 0) and (board.poles[13] == 0)):
        #     for k in range(0, 6):
        #         board.poles[7] += board.poles[k]
        #     board.endgame(player1, player2)
        #
        # if ((board.poles[1] == 0) and (board.poles[2] == 0) and (board.poles[3] == 0) and (board.poles[4] == 0) and (
        #         board.poles[5] == 0) and (board.poles[6] == 0)):
        #     for a in range(8, 13):
        #         board.poles[0] += board.poles[a]
        #     board.endgame(player1, player2)
        #     # return redirect(url_for('endGame', winner=winner))
        if (changeTurn == True):
            turn = (turn + 1) % 2

        playerName = players[turn].name

#
# def starting():
#     global board
#     global turn
#     global player1
#     global player2
#     global players
#     turn = 0
#     board = Game(player1, player2)
#     players = [player1, player2]



@app.route('/')
def stronaOne():
    return render_template('pageOne.html')


@app.route('/rules', methods=['GET', 'POST'])
def rules():
    return render_template('instructions.html')

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
    global player1
    global player2

    global board
    global players
    global turn
    global playerName

    board = Game(player1, player2)
    turn = 0
    # starting()
    players = [player1, player2]
    playerName = players[turn].name


    return render_template('pageGame.html', poles=board.poles, playerName=playerName, player1=player1, player2=player2,
                           board=board, turn=turn)


@app.route('/computer', methods=['GET', 'POST'])
def computer():
    global human
    global computer
    global board
    global players
    global turn
    global playerName
    turn = 0
    human = Player('Human')
    computer = Player('Computer')
    players = [human, computer]
    board=Game(human,computer)
    playerName = players[turn].name
    return render_template('pageGameComp.html', poles=board.poles, playerName=playerName, board=board, turn=turn)

@app.route('/cpuGameMove/<int:id>', methods=['GET', 'POST'])
def cpuGameMove(id):
    global playerName
    global turn
    global players
    global changeTurn
    global winner
    global chosenForCPU
    chosenForCPU = 1
    playerName = players[turn].name

    if turn == 0:
        human.move(id)
    elif turn == 1:
        chosenForCPU = computer.choosePole()
        computer.move(chosenForCPU)
        # return render_template('pageGameComp.html', b=b, poles=board.poles, playerName=playerName, turn=turn)
    if ((board.poles[8] == 0) and (board.poles[9] == 0) and (board.poles[10] == 0) and (board.poles[11] == 0) and (
            board.poles[12] == 0) and (board.poles[13] == 0)):
        for k in range(1, 7):
            board.poles[7] += board.poles[k]
        # board.endgame(player1, player2)
        return redirect(url_for('endGame'))
    elif ((board.poles[1] == 0) and (board.poles[2] == 0) and (board.poles[3] == 0) and (board.poles[4] == 0) and (
            board.poles[5] == 0) and (board.poles[6] == 0)):
        for a in range(8, 14):
            board.poles[0] += board.poles[a]
        # board.endgame(player1, player2)
        return redirect(url_for('endGame'))
    else:
        return render_template('pageGameComp.html', b=chosenForCPU, poles=board.poles, playerName=playerName, turn=turn)




@app.route('/move/<int:id>', methods=['GET', 'POST'])
def surrender(id):
    global playerName
    global turn
    global players
    global changeTurn
    global winner
    players[turn].move(id)
    if ((board.poles[8] == 0) and (board.poles[9] == 0) and (board.poles[10] == 0) and (board.poles[11] == 0) and (
            board.poles[12] == 0) and (board.poles[13] == 0)):
        for k in range(1, 7):
            board.poles[7] += board.poles[k]
        # board.endgame(player1, player2)
        return redirect(url_for('endGame'))
    elif ((board.poles[1] == 0) and (board.poles[2] == 0) and (board.poles[3] == 0) and (board.poles[4] == 0) and (
            board.poles[5] == 0) and (board.poles[6] == 0)):
        for a in range(8, 14):
            board.poles[0] += board.poles[a]
        # board.endgame(player1, player2)
        return redirect(url_for('endGame'))
    else:
        return render_template('pageGame.html', poles=board.poles, playerName=playerName, turn=turn)


@app.route('/endgame')
def endGame():
    global board
    global players
    players[0].summary = board.poles[0]
    players[1].summary = board.poles[7]
    if players[0].summary > players[1].summary:
        board.winner = players[0].name
    elif players[0].summary < players[1].summary:
        board.winner = players[1].name
    elif players[0].summary == players[1].summary:
        board.winner = 'It is a draw!'
    return render_template('endGame.html', winner=board.winner, nameOne=players[0].name, nameTwo=players[1].name, sumaOne=players[0].summary, sumaTwo=players[1].summary)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5130, debug=True)