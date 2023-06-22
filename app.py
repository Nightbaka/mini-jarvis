from typing import Optional
import keyboard
from SoundHandler import SoundHandler
from SpeechInterface import SpeechInterface
from gpt_service import QuestionHandler
from dotenv import load_dotenv
import os
import threading
from GUI.GUI import Icon, Controler, AnswerPopup
import PIL.Image
import time
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QThread, QObject, Signal
from PySide6.QtGui import QAction
import EdgeUtils
import asyncio


class Jarvis(QObject):

    def __init__(self):
        super().__init__()
        self.executor: JarvisExecutor = None
        self.executor_thread: QThread = None
        
        load_dotenv()
        self.sound_input = os.getenv("SOUND_INPUT")
        self.sound_output = os.getenv("SOUND_OUTPUT")
        self.speach_interface = SpeechInterface(self.sound_input, self.sound_output)
        self.sound_handler = SoundHandler(self.sound_input, self.sound_output)
        self.response_handler = ShowIfCodeInResponse(self.speach_interface, self.sound_handler)

    def run(self):
        if self.executor is not None:
            return
        if self.executor_thread is not None and self.executor_thread.isRunning():
            return
        self.executor = JarvisExecutor()
        self.executor_thread = QThread()
        self.executor.response_output.connect(self.handle_response)
        self.executor.moveToThread(self.executor_thread)
        self.executor_thread.started.connect(self.executor.start)
        self.executor_thread.finished.connect(lambda: self.finish_running)
        self.executor_thread.start()

    def finish_running(self):
        if self.executor_thread is None:
            return
        if self.executor_thread.isRunning():
            self.executor_thread.quit()
        self.executor = None
        self.executor_thread = None

    def handle_response(self, prompt: EdgeUtils.Query):
        self.response_handler.handle_response(prompt)

class JarvisExecutor(QObject):
    response_output = Signal(EdgeUtils.Query)

    def __init__(self):
        super().__init__()
        load_dotenv()
        self.sound_input = os.getenv("SOUND_INPUT")
        self.sound_output = os.getenv("SOUND_OUTPUT")
        self.speach_interface: SpeechInterface = SpeechInterface(self.sound_input, self.sound_output)
        self.sound_handler = SoundHandler(self.sound_input, self.sound_output)
        self.question_handler = QuestionHandler()
        self.response_action = QAction()

    def ask_gpt(self):
        print("recording")
        self.sound_handler.record()
        print("done recording")
        question = self.speach_interface.to_text()
        print(question)
        response = self.question_handler.ask(question)
        self.response_output.emit(self.question_handler.prompt)
        

    def start(self):
        keyboard.add_hotkey('ctrl+alt+p', self.ask_gpt)
        keyboard.wait()

    def stop(self):
        self.event.set()




class ResponseHandler():
    def __init__(self):
        pass

    def handle_response(self, response):
        pass

class ShowIfCodeInResponse(ResponseHandler):
    def __init__(self, speech_interface: SpeechInterface, sound_handler: SoundHandler):
        self.speech_interface = speech_interface
        self.sound_handler = sound_handler
        self.answer_widget = None

    def handle_response(self, query: EdgeUtils.Query):
        response = query.output
        print(response)
        code_blocks = response.split("```")[1:-1:2]
        if len(code_blocks) == 0:
            print("no code blocks")
            self.speech_interface.to_speach(response)
            self.sound_handler.play()
        else:
            self.show_code(response)

    def show_code(self, code):
        print("showing code:",code)
        self.answer_widget = AnswerPopup(code)
        self.answer_widget.show()
        print("done showing code")

class App():
    stop = Signal()
    start = Signal()

    def __init__(self):
        self.app = QApplication()
        self.app.setQuitOnLastWindowClosed(False)
        self.jarvis = Jarvis()
        self.icon = Icon(
            "GUI/jarvis.png",
            self.show_controller,
            self.exit,
            self.jarvis.run,
            self.jarvis.finish_running
        )
        self.controller = None

    def run(self):
        self.create_icon()
        self.jarvis.run()
        self.show_controller()
        self.app.exec()

    def create_icon(self):
        self.icon.show()
        
        
    def exit(self):
        self.jarvis.finish_running()
        self.hide_controller()
        self.app.quit()

    def show_controller(self):
        if self.controller is None:
            self.controller = Controler(self.jarvis.run, self.jarvis.finish_running)
        if self.controller.isVisible():
            return
        self.controller.show()

    def hide_controller(self):
        if self.controller is None:
            return
        if not self.controller.isVisible():
            return
        self.controller.destroy()

if __name__ == '__main__':
    app = App()
    app.run()