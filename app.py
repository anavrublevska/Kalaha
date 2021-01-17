from flask import Flask, render_template

app = Flask(__name__)

class Game:
    def __init__(self):
        self.poles = [0, 4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4]

class Player:
    def __init__(self, name):
        self.name = name
# def make_board():
#     poles = [0, 4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4]
#     return poles


# squares = [
#     {'number': '0', 'amount': '0'},
#     {'number': '1', 'amount': '4'},
#     {'number': '2', 'amount': '4'},
#     {'number': '3', 'amount': '4'},
#     {'number': '4', 'amount': '4'},
#     {'number': '5', 'amount': '4'},
#     {'number': '6', 'amount': '4'},
#     {'number': '7', 'amount': '0'},
#     {'number': '8', 'amount': '4'},
#     {'number': '9', 'amount': '4'},
#     {'number': '10', 'amount': '4'},
#     {'number': '11', 'amount': '4'},
#     {'number': '12', 'amount': '4'},
#     {'number': '13', 'amount': '4'}
# ]
# board = make_board()
# board = Game()

@app.route('/pageGame')
def pageGame():
    global board
    board = Game()
    return render_template('pageGame.html', poles=board.poles)

@app.route('/move/<int:id>')
def move(id):
    # global board
    # board = pageGame()
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


    return render_template('pageGame.html', poles=board.poles)


@app.route('/pageOne')
def stronaOne():
    return render_template('pageOne.html')



if __name__ == '__main__':
    app.run()
