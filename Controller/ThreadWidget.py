import random
from PySide6 import QtCore, QtWidgets

from NumberWorker import NumberWorker

class ThreadWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.worker = NumberWorker()
        self.worker.start()
        
        self.text = QtWidgets.QLabel(str(self.worker.number),
                                     alignment=QtCore.Qt.AlignCenter)
        
        self.worker.numberChanged.connect(self.text.setNum)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        