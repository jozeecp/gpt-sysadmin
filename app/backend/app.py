"""Backend API for the task manager"""
from uuid import uuid4

from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)

tasks = {}


@app.route("/v1/tasks", methods=["POST"])
def create_task():
    """Create a new task"""
    task_data = request.json

    task_id = str(uuid4())
    task = Task(
        **{
            "taskId": task_id,
            "status": "pending",
            "taskDescription": task_data["taskDescription"],
            "hostDescription": task_data["hostDescription"],
            "host": task_data["host"],
            "user": task_data.get("user", "root"),
            "supervised": task_data["supervised"],
            "messages": [],
        }
    )
    tasks[task_id] = task

    response = {"task": task.dict()}
    return jsonify(response), 201


@app.route("/v1/tasks/<string:task_id>/messages", methods=["POST"])
def send_message(task_id):
    """Send a message to a task"""

    message = request.json.get("message")

    if task_id not in tasks:
        return jsonify({"error": "Task not found"}), 404

    tasks[task_id]["messages"].append(message)
    return jsonify({"status": "success"}), 201


@app.route("/v1/tasks/<string:task_id>", methods=["GET"])
def get_task(task_id):
    """Get a task"""

    if task_id not in tasks:
        return jsonify({"error": "Task not found"}), 404

    task = tasks[task_id]
    response = {
        "taskId": task["taskId"],
        "status": task["status"],
        "messages": task["messages"],
    }
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(debug=True)
