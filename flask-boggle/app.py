from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config["SECRET_KEY"] = "LORD_GANDOFFFF"

app.debug = true
toolbar = DebugToolbarExtension(app)
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

boggle = Boggle()


@app.route("/")
def start():
    """Starts the board."""

    board = boggle.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    return render_template("index.html", board=board,
                           highscore=highscore,
                           nplays=nplays)


@app.route("/check-word")
def check_word():
    """seeing if there is a valid word in the dict"""

    word = request.args["word"]
    board = session["board"]
    response = boggle.check_valid_word(board, word)

    return jsonify({'result': response})


@app.route("/post-score", methods=["POST"])
def post_score():
    """takes in the score and how many times played. then checks if the highsocre needs to be ammended"""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)
