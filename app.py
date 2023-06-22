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
from PySide6.QtCore import QThread

class Jarvis:
    def __init__(self):
        load_dotenv()
        self.speach_interface = SpeechInterface()
        self.sound_input = os.getenv("SOUND_INPUT")
        self.sound_output = os.getenv("SOUND_OUTPUT")
        self.listen_thread = None
        self.event = threading.Event()

    def ask_gpt(self):
        print("recording")
        SoundHandler.record(self.sound_input)
        print("done recording")

        question = self.speach_interface.to_text(self.sound_input)
        print(question)

        print("asking")
        handler = QuestionHandler()
        response = handler.ask(question)
        
        self.speach_interface.to_speech(response, filename = self.sound_output)
        print("playing")
        SoundHandler.play(self.sound_output) 
        print("done playing")

    # Start the background thread
    def _start_listening(self):
        keyboard.add_hotkey('ctrl+alt+p', self.ask_gpt)
        while not self.event.is_set():
            time.sleep(1)


    def run(self):
        if self.listen_thread.is_alive():
            return
        self.event.clear()
        self.listen_thread = threading.Thread(target=self.start_listening, args=(self.event,))
        self.listen_thread.start()

    def stop(self):
        self.event.set()
        

class App():
    def __init__(self):
        #self.qapp = QApplication()
        self.jarvis = Jarvis()

        self.controler_thread = None
        self.controler_event = threading.Event()
        self.controler = Controler(self.controler_event, lambda: self.jarvis.run(), lambda: self.jarvis.stop())

        image = PIL.Image.open("GUI/jarvis.png")
        self.icon = Icon(image=image, 
                         on_open= self.open_controler,
                         on_start = lambda x,y: Jarvis.run, 
                         on_stop = lambda x,y: Jarvis.stop,
                         on_exit = self.on_exit
                         )
        
    def start_app(self):
        self.open_controler()
        print("start icon")
        self.icon.run()

    def open_controler(self):
        self.controler_thread = threading.Thread(target=self.controler.run)
        self.controler_thread.start()

    def exit_controler(self):
        self.controler_event.set()

    def on_exit(self):
        self.jarvis.stop()
        self.exit_controler()
        self.icon.stop()

if __name__ == '__main__':
    app = App()
    app.start_app()
    print("done")