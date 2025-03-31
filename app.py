import logging
from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Connect to MongoDB
try:
    client = MongoClient(os.getenv("MONGO_URI", "mongodb://root:root@mongo:27017/"))
    db = client.todo_db
    todos = db.todos
    logger.info("✅ Connected to MongoDB")
except Exception as e:
    logger.error(f"❌ MongoDB connection error: {e}")
    exit(1)

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

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
