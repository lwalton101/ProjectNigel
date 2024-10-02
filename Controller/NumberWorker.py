import time
from PySide6.QtCore import Signal, QThread

class NumberWorker(QThread):
    
    numberChanged = Signal(int)
    
    def __init__(self) -> None:
        super().__init__()
        self.number = 0
    
    def run(self) -> None:
        while True:
            self.number += 1
            self.numberChanged.emit(self.number)
            print(f"Increasing number to {self.number}")
            time.sleep(10)