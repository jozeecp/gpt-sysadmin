"""Backend API for the task manager"""
import logging
import os
import sys
from uuid import uuid4

from flask import Flask, jsonify, request
from functions.hosts.get.handler import handler as host_get_handler
from functions.hosts.post.handler import handler as host_post_handler
from functions.tasks.post.handler import handler as task_post_handler
from libs.utils import LoggingService
from models.host import Host, HostCreate
from models.task import Task

# Set up logging
logger = LoggingService.get_logger(__name__)

# Add the directory containing this script to the Python path
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_dir)
app = Flask(__name__)

tasks = {}


@app.route("/v1/tasks", methods=["POST"])
def create_task():
    """Create a new task"""
    task_data = request.json

    logger.info("Creating task...")
    logger.debug("Received task data: %s", task_data)

    task_id = str(uuid4())
    logger.debug("Task ID: %s", task_id)
    task_data["taskId"] = task_id
    task_data["status"] = "pending"
    task = Task(**task_data)

    try:
        new_task = task_post_handler(task)
    except Exception as e:
        logger.error("Error creating task: %s", e)
        return jsonify({"error": "Error creating task"}), 500

    logger.info("Task created successfully")
    logger.debug("Task created: %s", new_task.dict())

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

    # if task_id not in tasks:
    #     return jsonify({"error": "Task not found"}), 404

    # task = tasks[task_id]
    # response = {
    #     "taskId": task["taskId"],
    #     "status": task["status"],
    #     "messages": task["messages"],
    # }
    # return jsonify(response), 200


@app.route("/v1/hosts", methods=["POST"])
def create_host():
    """Create a new host"""

    host_data = request.json

    logger.info("Creating host...")
    logger.debug("Received host data: %s", host_data)

    host_id = str(uuid4())
    logger.debug("Host ID: %s", host_id)
    host_data["host_id"] = host_id
    host = HostCreate(**host_data)
    logger.debug("Host create data: %s", host.dict())

    try:
        new_host = host_post_handler(host)
    except Exception as e:
        logger.error("Error creating host: %s", e)
        return jsonify({"error": "Error creating host"}), 500
    logger.info("Host created successfully")
    logger.debug("Host created: %s", new_host.dict())

    return jsonify({"host_id": host_id}), 201


@app.route("/v1/hosts/<string:host_id>", methods=["GET"])
def get_host(host_id):
    """Get a host"""

    host = host_get_handler(host_id)

    return jsonify(host.dict()), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
