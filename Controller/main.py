import sys
import random
from PySide6 import QtCore, QtWidgets
from ThreadWidget import ThreadWidget

from TestWidget import MyWidget

if __name__ == "__main__":
    print("Welcome to the controller")
    app = QtWidgets.QApplication(["tys"])
    app.setApplicationName("Project Nigel Controller")
    app.setApplicationDisplayName("Project Nigel Controller")

    tabWidget = QtWidgets.QTabWidget()
    widget = MyWidget()
    widget2 = ThreadWidget()
    
    tabWidget.addTab(widget, "Name")
    tabWidget.addTab(widget2, "Threaded")
    tabWidget.resize(1280, 800)
    tabWidget.show()
    sys.exit(app.exec())