from typing import Optional
from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QThread, Signal, Slot, QObject
from PySide6.QtGui import QPalette, QColor, QCloseEvent, QIcon, QAction, QTextDocument
from PySide6.QtWidgets import QApplication, QHBoxLayout, QTextEdit, QGridLayout, QMenu,QMainWindow, QSystemTrayIcon, QStackedLayout, QDockWidget, QGraphicsView, QWidget, QGraphicsScene, QVBoxLayout
import pystray
import PIL.Image
import threading
import time
from utils import extract_code

class Controler(QWidget):
    def __init__(self, on_start, on_stop):
        super().__init__()
        self.on_start = on_start
        self.on_stop = on_stop
        self.start_button = QtWidgets.QPushButton("Start")
        self.stop_button = QtWidgets.QPushButton("Stop")
        self.start_button.clicked.connect(self.on_start)
        self.stop_button.clicked.connect(self.on_stop)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.start_button)
        self.layout().addWidget(self.stop_button)



class AnswerPopup(QWidget):
    def __init__(self, answer):
        super().__init__()
        self.answer = answer
        self.windowTitle = "Answer"
        self.setLayout(QHBoxLayout())
        self.text_widget = QTextEdit()
        self.text_widget.setMarkdown(self.answer)
        self.layout().addWidget(self.text_widget)

        self.copy_button = QtWidgets.QPushButton("Copy")
        self.copy_button.clicked.connect(self.copy_code)
        self.layout().addWidget(self.copy_button)

    def copy_code(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(extract_code(self.answer))

class Icon():
    def __init__(self, image_path, on_open, on_exit, on_stop, on_start):
        self.image_path = image_path
        icon = QIcon(self.image_path)
        self.tray_icon = QSystemTrayIcon(icon)

        menu = QMenu()
        open_controller = QAction("Open controller")
        open_controller.triggered.connect(on_open)
        end = QAction("End")
        end.triggered.connect(on_exit)
        start = QAction("Start")
        start.triggered.connect(on_start)
        stop = QAction("Stop")
        stop.triggered.connect(on_stop)

        menu.addAction(open_controller)
        menu.addAction(end)
        menu.addAction(start)
        menu.addAction(stop)
        
        open_controller.triggered.emit()
        end.triggered.emit()
        start.triggered.emit()
        stop.triggered.emit()

        self.tray_icon.setContextMenu(menu)
    
    def show(self):
        self.tray_icon.setVisible(True)
        

class GUI_Controller():
    def __init__(self):
        print("GUI init")
        self.on_start = lambda icon, item: print(item)
        self.on_stop = lambda icon, item: print(item)
        self.on_exit = lambda icon, item: icon.stop()
        image = PIL.Image.open("GUI/jarvis.png")
        self.icon = Icon(image, self.on_start, self.on_exit, self.on_stop, self.on_start)

    def run(self):
        self.icon.run()


if __name__ == "__main__":
    print("GUI main")
