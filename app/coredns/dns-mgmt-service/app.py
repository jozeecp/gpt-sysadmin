"""DNS Management Service"""
import json
import logging
import sys
from os.path import exists

from flask import Flask, jsonify, request

app = Flask(__name__)

host_file_name = "/etc/coredns/hosts"


class JsonFormatter(logging.Formatter):
    """JSON log formatter"""

    def format(self, record):
        if isinstance(record.msg, (dict, list)):
            # line below pretty prints json
            record.msg = json.dumps(record.msg, indent=4)
            # pprint.pprint(record.msg)
        return super().format(record)


logger = logging.getLogger(__name__)

# Set the log level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)
logger.setLevel(logging.DEBUG)

# Create a stream handler to write logs to stdout
stream_handler = logging.StreamHandler(sys.stdout)

# Set the log format
formatter = JsonFormatter("%(asctime)s - %(levelname)s - %(message)s")
stream_handler.setFormatter(formatter)

# Add the stream handler to the logger
logger.addHandler(stream_handler)


@app.route("/hosts", methods=["GET"])
def get_hosts():
    """Get all hosts from DNS"""
    logger.debug("Getting all hosts from DNS")
    # read all lines from /etc/hosts file
    with open(host_file_name, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # remove comments and empty lines
    lines = [line for line in lines if not line.startswith("#") and line.strip()]

    # parse lines to get ip and hostname
    hosts = []
    for line in lines:
        ip, hostname = line.split()
        hosts.append({"ip": ip, "hostname": hostname})

    logger.info("Hosts retrieved from DNS: %s", hosts)

    return jsonify(hosts), 200


@app.route("/hosts", methods=["POST"])
def add_host_to_dns():
    """Add a host to DNS"""

    logger.debug("Adding a host to DNS")
    host_data = request.json

    # add line to /etc/hosts file
    assert exists(host_file_name)
    with open(host_file_name, "a", encoding="utf-8") as f:
        f.write(f"{host_data['ip']} {host_data['hostname']}")

    logger.info("Host added to DNS: %s", host_data)

    return jsonify({"message": "Host added to DNS"}), 200


@app.route("/hosts/<string:ip>", methods=["DELETE"])
def delete_host(ip):
    """Delete a host from DNS"""

    logger.debug("Deleting a host from DNS")

    # read all lines from /etc/hosts file
    with open(host_file_name, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # remove line with ip
    with open(host_file_name, "w", encoding="utf-8") as f:
        for line in lines:
            if not line.startswith(ip):
                f.write(line)

    logger.debug("Host deleted from DNS: %s", ip)
    return jsonify({"message": "Host deleted from DNS"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
