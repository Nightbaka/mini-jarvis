from typing import Optional
from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QInputDialog, QLineEdit, QDockWidget, QGraphicsView, QWidget, QGraphicsScene, QVBoxLayout
import pystray
import PIL.Image

class Controler(QMainWindow):
    def __init__(self, on_start, on_stop):
        super().__init__()
        self.start_button = QtWidgets.QPushButton("Start")
        self.stop_button = QtWidgets.QPushButton("Stop")
        self.start_button.clicked.connect(on_start)
        self.stop_button.clicked.connect(on_stop)

        widget = QWidget()
        widget.setLayout(QVBoxLayout())
        widget.layout().addWidget(self.start_button)
        widget.layout().addWidget(self.stop_button)
        self.setCentralWidget(widget)

class AnswerPopup(QGraphicsView):
    def __init__(self, answer):
        super().__init__()
        self.answer = answer
        scene = AnswerScene(self.answer)
        self.setScene(scene)

    def copy(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.answer)

class AnswerScene(QGraphicsScene):
    def __init__(self, answer):
        super().__init__()
        self.answer = answer
        self.addText(self.answer)

class Icon():
    def __init__(self, image, on_open, on_exit, on_stop, on_start):
        self.icon = pystray.Icon("mini_jarvis", image, "mini-jarvis", menu=pystray.Menu(
            pystray.MenuItem("Open controller", on_open),
            pystray.MenuItem("End", on_exit),
            pystray.MenuItem("Start", on_start),
            pystray.MenuItem("Stop", on_stop)
        ))
        self.icon.run()

class GUI_Controller():
    def __init__(self):
        print("GUI init")
        self.on_start = lambda icon, item: print(item)
        self.on_stop = lambda icon, item: print(item)
        self.on_exit = lambda icon, item: icon.stop()
        image = PIL.Image.open("GUI/jarvis.png")
        self.icon = Icon(image, self.on_start, self.on_exit, self.on_stop, self.on_start)


if __name__ == "__main__":
    app = GUI_Controller()
    
