from flask import Flask, request, jsonify
import time
from threading import Thread

app = Flask(__name__)

thread = None
win_number = 0
has_won = False

default_stored_number = 169

# Global variable to store the number
stored_number = default_stored_number

# POST route to save a number
@app.route("/save_number", methods=["POST"])
def save_number():
    global stored_number
    data = request.get_json()

    if not data or "number" not in data:
        return jsonify({"error": "Missing 'number' field"}), 400

    stored_number = data["number"]
    return jsonify({"message": "successful"}), 200


@app.route("/save_default_number", methods=["POST"])
def save_default_number():
    global default_stored_number
    data = request.get_json()

    if not data or "number" not in data:
        return jsonify({"error": "Missing 'number' field"}), 400

    default_stored_number = data["number"]
    return 'ok', 200



# GET route to return the number
@app.route("/get_number", methods=["GET"])
def get_number():
    if stored_number is None:
        return jsonify({"error": "No number has been saved yet"}), 404
    return str(stored_number), 200



@app.route("/get_win_number", methods=["GET"])
def get_win_number():
    return str(win_number), 200

@app.route("/reset_win_number", methods=["GET"])
def reset_win_number():
    global win_number
    win_number = 0
    return 'ok', 200

@app.route("/win", methods=["GET"])
def win():
    global has_won, win_number, stored_number
    has_won = True
    stored_number = default_stored_number
    win_number += 1
    return 'ok', 200

def decrease_number(rate):
    global stored_number, has_won
    while not has_won:
        stored_number = max(7, stored_number - rate)
        time.sleep(1)
    has_won = False

@app.route("/make_it_easy", methods=["POST"])
def make_it_easy():
    global thread
    data = request.get_json()

    if not data or "rate" not in data:
        return jsonify({"error": "Missing 'rate' field"}), 400

    rate = data["rate"]
    if thread is not None:
        thread.join(timeout=1)

    thread = Thread(target=decrease_number, args=(rate,))
    thread.daemon = True
    thread.start()
    
    return 'ok', 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
