import chess
import cv2
import numpy as np
import time
import chess.engine
import stockfish
from flask import Flask, render_template

x=""
app = Flask(__name__)
@app.route('/')
def home():
    global x
    # Define a message to display
    message =x
    return render_template("index.html", message=message)

if (__name__ == "__main__"):
    app.run(debug=True)


# el paramatre mta3 stabilisation
stability_counter = 0
stable_frames_required = 5

board=chess.Board()

def play():
    return none



def pixel_to_chess(x, y, board_width, board_height):
    square_width = board_width / 8
    square_height = board_height / 8
    column = int(x // square_width)
    row = int(y // square_height)
    chess_notation = f"{chr(column + ord('a'))}{8 - row}"
    return chess_notation

def detect_pieces(board, templates, board_width, board_height):
    """Detect pieces on the board and return their positions in chess notation."""
    piece_positions = {}
    for piece_name, template in templates.items():
        if template is None:
            continue
        result = cv2.matchTemplate(board, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        if max_val > 0.8:
            notation = pixel_to_chess(max_loc[0], max_loc[1], board_width, board_height)
            piece_positions[notation] = piece_name
    return piece_positions

templates = {
    "queen_white": cv2.imread("queen_white.png", 0),
    "queen_black": cv2.imread("queen_black.png", 0),
    "king_white": cv2.imread("king_white.png", 0),
    "king_black": cv2.imread("king_black.png", 0),
    "bishop_white": cv2.imread("bishop_white.png", 0),
    "bishop_black": cv2.imread("bishop_black.png", 0),
    "knight_white": cv2.imread("knight_white.png", 0),
    "knight_black": cv2.imread("knight_black.png", 0),
    "rook_white": cv2.imread("rook_white.png", 0),
    "rook_black": cv2.imread("rook_black.png", 0),
    "pawn_white": cv2.imread("pawn_white.png", 0),
    "pawn_black": cv2.imread("pawn_black.png", 0),
}

# t7a4er el camera
cap = cv2.VideoCapture(0)

# taswira lil 7ala el 3adiya mta3 chessboard
ret, frame = cap.read()
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
_, pic0 = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
board_width, board_height = gray.shape[1], gray.shape[0] #ennajmou en3aw4ouha
old_positions = detect_pieces(pic0, templates, board_width, board_height)


test=True# bech na3mil boucle mat7abbes kan chekmate
while test:
    result = engine.analyse(board, chess.engine.Limit(time=0.1))
    best_move = result["pv"][0]
    time.sleep(2)
    ret, frame = cap.read()
    if not ret:
        continue
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, pic = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    # bech enchoufou est ce que thamma differance walla !!
    if not np.array_equal(pic0, pic):
        new_positions = detect_pieces(pic, templates, board_width, board_height)
        stability_counter += 1
        if stability_counter >= stable_frames_required:
            old_pos = None
            new_pos = None
            for pos in old_positions.keys():
                if pos not in new_positions:  # el 9at3a win kanit
                    old_pos = pos  # blasa 9dima

            for pos in new_positions.keys():
                if pos not in old_positions:  # el 9at3a win tbadlit
                    new_pos = pos  # blasa jdida
            move = old_pos + new_pos
            legal_moves = list(board.legal_moves)
            leg = False
            for i in legal_moves:
                if (move==i):
                    leg = True
            # legal or illegal move
            if (leg==False):
                x="illegal move"
                home()
            else:
                pic0 = pic  # taswirat el board titbaddel
                old_positions = new_positions
                stability_counter = 0
                x=best_move
                home()
                board.push_san(str(move))
                result = engine.analyse(board, chess.engine.Limit(time=0.1))
                best_move = result["pv"][0]
                board.push_san(str(best_move))
                play(best_move)
                result = engine.analyse(board, chess.engine.Limit(time=0.1))
                score = result["score"]

                # el code ha4a bech y5alli el program yfonctioni 7atta kan 8alit
                time.sleep(5)

                # y3awid y updati ettaswira
                ret, frame = cap.read()
                if ret:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    _, pic0 = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
                if(score.is_mate()):
                    test=False
        else:
            stability_counter = 0  # reset lil compteur

cap.release()
engine.quit()