"""General utility functions and classes."""
import json
import logging
import sys


class JsonFormatter(logging.Formatter):
    """JSON log formatter"""

    def format(self, record):
        if isinstance(record.msg, (dict, list)):
            # line below pretty prints json
            record.msg = json.dumps(record.msg, indent=4)
            # pprint.pprint(record.msg)
        return super().format(record)


class LoggingService:
    """Logging service"""

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """Get a logger"""

        # Create a logger
        logger = logging.getLogger(name)

        # Set the log level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)
        logger.setLevel(logging.DEBUG)

        # Create a stream handler to write logs to stdout
        stream_handler = logging.StreamHandler(sys.stdout)

        # Set the log format
        formatter = JsonFormatter("%(asctime)s - %(levelname)s - %(message)s")
        stream_handler.setFormatter(formatter)

        # Add the stream handler to the logger
        logger.addHandler(stream_handler)

        return logger
