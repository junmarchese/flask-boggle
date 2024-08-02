from flask import Flask, request, render_template, session, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "SPB-boggle-exercise"

boggle_game = Boggle(10)

@app.route("/")
def homepage():
    """Generate a new Boggle board and render homepage."""
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    return render_template("index.html", board=board, highscore=highscore, nplays=nplays)

@app.route("/check-word")
def check_word():
    """Check if a word is valid on the current board."""
    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)
    return jsonify({'result': response})

@app.route("/post-score", methods=["POST"])
def post_score():
    """Update high score and number of plays."""
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session['highscore'] = max(score, highscore)
    session['nplays'] = nplays + 1

    return jsonify(newBestScore=score > highscore)

if __name__ == "__main__":
    app.run(debug=True)