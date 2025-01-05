import logging
import os


class LoggingManager:
    def __init__(self, log_file="Simulation.log"):
        """Initialize logging configuration."""
        log_directory = "Logging"
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)  # Create the Logging directory if it does not exist

        log_path = os.path.join(log_directory, log_file)
        self.log_file = log_path

        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,  # Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def log(self, message, level='info'):
        """General log method that logs messages based on the level specified."""
        {
            'info': logging.info,
            'error': logging.error,
            'warning': logging.warning,
            'debug': logging.debug
        }[level](message)

    def log_action(self, message):
        logging.info(message)

    def log_error(self, message):
        logging.error(message)

    def log_warning(self, message):
        logging.warning(message)

    def log_debug(self, message):
        logging.debug(message)
