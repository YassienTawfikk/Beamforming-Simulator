import sys

from PyQt5 import QtWidgets

from App.Controller import MainController


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = MainController(app)
    sys.exit(controller.run())


if __name__ == "__main__":
    main()
