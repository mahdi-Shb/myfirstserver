from flask import Flask, request, jsonify

app = Flask(__name__)

# Global variable to store the number
stored_number = None

# POST route to save a number
@app.route("/save_number", methods=["POST"])
def save_number():
    global stored_number
    data = request.get_json()

    if not data or "number" not in data:
        return jsonify({"error": "Missing 'number' field"}), 400

    stored_number = data["number"]
    return jsonify({"message": "successful"}), 200

# GET route to return the number
@app.route("/get_number", methods=["GET"])
def get_number():
    if stored_number is None:
        return jsonify({"error": "No number has been saved yet"}), 404
    return str(stored_number), 200


if __name__ == "__main__":
    app.run(debug=True)
