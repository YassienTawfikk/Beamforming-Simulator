import sys
from PyQt5 import QtWidgets
from app.controllers.main_controller import MainController
from app.utils.logging_manager import LoggingManager

if __name__ == '__main__':
    # Initialize Logger
    logger_manager = LoggingManager()
    logger_manager.log("--- Application Starting ---", "info")

    try:
        app = QtWidgets.QApplication(sys.argv)
        controller = MainController(app)
        sys.exit(controller.run())
    except Exception as e:
        logger_manager.log_error(f"Critical Application Error: {e}", exc_info=True)
        sys.exit(1)
