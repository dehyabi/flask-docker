from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# Koneksi ke MongoDB
client = MongoClient(os.getenv("MONGO_URI", "mongodb://mongo:27017/"))
db = client.todo_db
todos = db.todos

@app.route("/todos", methods=["GET"])
def get_todos():
    return jsonify([{ "id": str(todo["_id"]), "task": todo["task"] } for todo in todos.find()])

@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.json
    if not data or "task" not in data:
        return jsonify({"error": "Task is required"}), 400
    todos.insert_one({"task": data["task"]})
    return jsonify({"message": "Task added"}), 201

@app.route("/todos/<id>", methods=["DELETE"])
def delete_todo(id):
    todos.delete_one({"_id": id})
    return jsonify({"message": "Task deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
