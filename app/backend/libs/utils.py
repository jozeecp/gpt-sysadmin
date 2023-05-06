"""General utility functions and classes."""
import logging
import sys


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
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(formatter)

        # Add the stream handler to the logger
        logger.addHandler(stream_handler)

        return logger
