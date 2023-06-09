"""Backend API for the task manager"""
import os
import sys
import time
from uuid import uuid4

from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from functions.hosts.get.handler import handler as host_get_handler
from functions.hosts.host_id.delete.handler import handler as host_delete_handler
from functions.hosts.host_id.get.handler import handler as host_host_id_get_handler
from functions.hosts.post.handler import handler as host_post_handler
from functions.tasks.post.handler import handler as task_post_handler
from functions.tasks.task_id.confirm.handler import handler as task_id_confirm_handler
from functions.tasks.task_id.get.handler import handler as task_id_get_handler
from functions.tasks.task_id.put.handler import handler as task_id_put_handler
from libs.utils import LoggingService
from models.host import HostCreate
from models.task import Task
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

# Set up logging
logger = LoggingService.get_logger(__name__)

# Add the directory containing this script to the Python path
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_dir)
app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

tasks = {}

requests_total = Counter("requests_total", "Total number of HTTP requests.")
request_hist = Histogram(
    "confirm_request_latency_seconds", "Request latency in seconds."
)


@app.route("/v1/tasks", methods=["POST"])
def create_task():
    """Create a new task"""

    # increment the counter
    requests_total.inc()
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


# @app.route("/v1/tasks/<string:task_id>/messages/machine_messages", methods=["POST"])
# def send_message(task_id):
#     """Send a message to a task"""

#     increment the counter
#     requests_total.inc()

#     machine_msg = request.json.get("machine_msg")

#     msg = HostMessage(machine_msg=machine_msg)

#     new_task = task_id_messages_post_handler(msg, task_id)

#     new_gpt_msg: GPTMessage = new_task.messages[-1]
#     return jsonify(new_gpt_msg.dict()), 201


@app.route("/v1/tasks/<string:task_id>", methods=["GET"])
def get_task(task_id):
    """Get a task"""

    # increment the counter
    requests_total.inc()

    logger.debug("Getting task: %s", task_id)

    task = task_id_get_handler(task_id)
    return jsonify(task.dict()), 200


@app.route("/v1/tasks/<string:task_id>", methods=["PUT"])
def modify_task(task_id):
    """Modify a task"""

    # increment the counter
    requests_total.inc()

    logger.debug("Getting task: %s", task_id)
    request_data = request.json
    logger.debug("Request data: %s", request_data)

    try:
        task = task_id_put_handler(request_data)
    except Exception as e:
        logger.error("Error modifying task: %s", e)
        return jsonify({"error": "Error modifying task"}), 500

    return jsonify(task.dict()), 200


@app.route("/v1/tasks/<string:task_id>/confirm", methods=["POST"])
def confirm_next_step(task_id):
    """Go to the next step in a task"""

    # increment the counter
    requests_total.inc()

    logger.debug("Getting task: %s", task_id)
    try:
        t_0 = time.time()
        task = task_id_confirm_handler(task_id)
        t_1 = time.time()
        request_hist.observe(t_1 - t_0)
    except Exception as e:
        logger.error("Error confirming task: %s", e)
        return jsonify({"error": f"Error confirming task: {e}"}), 500
    return jsonify({"task": task.dict()}), 200


@app.route("/v1/hosts", methods=["POST"])
def create_host():
    """Create a new host"""

    # increment the counter
    requests_total.inc()

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


@app.route("/v1/hosts", methods=["GET"])
def get_hosts():
    """Get all hosts"""

    # increment the counter
    requests_total.inc()

    logger.debug("Getting all hosts...")
    try:
        hosts = host_get_handler()
        host_dict_list = [host.dict() for host in hosts]
        logger.debug("Hosts: %s", hosts)
    except Exception as e:
        logger.error("Error getting hosts: %s", e)
        return jsonify({"error": f"Error getting hosts: {e}"}), 500

    return jsonify(host_dict_list), 200


@app.route("/v1/hosts/<string:host_id>", methods=["GET"])
def get_host(host_id):
    """Get a host"""

    # increment the counter
    requests_total.inc()

    host = host_host_id_get_handler(host_id)

    return jsonify(host.dict()), 200


@app.route("/v1/hosts/<string:host_id>", methods=["DELETE"])
def delete_host(host_id):
    """Delete a host"""

    # increment the counter
    requests_total.inc()

    logger.debug("Deleting host: %s", host_id)
    try:
        host_delete_handler(host_id)
    except Exception as e:
        logger.error("Error deleting host: %s", e)
        return jsonify({"error": f"Error deleting host: {e}"}), 500

    return jsonify({}), 200


# prometheus metrics endpoint
@app.route("/metrics")
def metrics():
    """Prometheus metrics endpoint"""

    # increment the counter
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
