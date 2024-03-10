from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
USERS_FILE = "users.json"

def read_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as file:
        return json.load(file)

def write_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)

@app.route("/users", methods=["GET"])
def get_users():
    users = read_users()
    return jsonify(users)

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    users = read_users()
    for user in users:
        if user["id"] == user_id:
            return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    users = read_users()
    user_ids = [user["id"] for user in users]
    if "id" not in data or data["id"] in user_ids:
        return jsonify({"error": "Invalid or duplicate user ID"}), 400
    users.append(data)
    write_users(users)
    return jsonify(data), 201

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    users = read_users()
    for i, user in enumerate(users):
        if user["id"] == user_id:
            users[i] = data
            write_users(users)
            return jsonify(data)
    return jsonify({"error": "User not found"}), 404

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    users = read_users()
    for i, user in enumerate(users):
        if user["id"] == user_id:
            del users[i]
            write_users(users)
            return jsonify({"message": "User deleted successfully"})
    return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
