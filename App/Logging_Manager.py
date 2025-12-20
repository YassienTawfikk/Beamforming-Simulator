import logging
import os
import sys


class LoggingManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LoggingManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, log_file="simulation.log"):
        if hasattr(self, 'logger'):
            return

        self.logger = logging.getLogger("BeamformingApp")
        self.logger.setLevel(logging.INFO)
        # Prevent adding multiple handlers if re-initialized
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        
        self.logger.propagate = False

        formatter = logging.Formatter("%(asctime)s - [%(levelname)s] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

        # File Handler
        log_directory = "logging"
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        log_path = os.path.join(log_directory, log_file)
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def log(self, message, level='info'):
        """General log method that logs messages based on the level specified."""
        lvl = level.lower()
        if lvl == 'info':
            self.logger.info(message)
        elif lvl == 'error':
            self.logger.error(message)
        elif lvl == 'warning':
            self.logger.warning(message)
        elif lvl == 'debug':
            self.logger.debug(message)
        else:
            self.logger.info(message)

    def log_action(self, message):
        self.logger.info(message)

    def log_error(self, message, exc_info=False):
        self.logger.error(message, exc_info=exc_info)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_debug(self, message):
        self.logger.debug(message)
