import keyboard
from SoundHandler import SoundHandler
from SpeechModels import SpeechModels
from gpt_service import QuestionHandler
from dotenv import load_dotenv
import os
import threading

class App:
    def __init__(self):
        load_dotenv()
        self.sound_input = os.getenv("SOUND_INPUT")
        self.sound_output = os.getenv("SOUND_OUTPUT")

    def ask_gpt(self):
        print("recording")
        SoundHandler.record(self.sound_input)
        print("done recording")

        question = SpeechModels.to_text(self.sound_input)
        print(question)

        print("asking")
        handler = QuestionHandler()
        response = handler.ask(question)
        
        SpeechModels.to_speech(response, filename = self.sound_output)
        print("playing")
        SoundHandler.play(self.sound_output) 
        print("done playing")

    def background(self):
        # Your background function here
        pass

    # Start the background thread
    def start_app(self):
        thread = threading.Thread(target=self.background)
        thread.start()

        # Wait for the key combination to be pressed
        keyboard.add_hotkey('ctrl+alt+p', self.ask_gpt)
        keyboard.add_hotkey('ctrl+alt+q', lambda: exit(0))

        # Keep the script running
        keyboard.wait()

if __name__ == '__main__':
    app = App()
    print("app created")
    app.start_app()
    print("app started")