"""Backend API for the task manager"""
import os
import sys
from uuid import uuid4

from flask import Flask, jsonify, request

from app.backend.functions.tasks.post.handler import handler as task_post_handler
from app.backend.models.task import Task

# Add the directory containing this script to the Python path
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_dir)
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

    new_task = task_post_handler(task)

    response = {"task": new_task.dict()}
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


@app.route("v1/hosts", methods=["POST"])
def create_host():
    """Create a new host"""


@app.route("v1/hosts/<string:host_id>", methods=["GET"])
def get_host(host_id):
    """Get a host"""

    print(host_id)


if __name__ == "__main__":
    app.run(debug=True)
