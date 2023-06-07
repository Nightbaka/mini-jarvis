from SoundHandler import SoundHandler
from SpeechModels import SpeechModels
from gpt_service import QuestionHandler
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    sound_input = os.getenv("SOUND_INPUT")
    sound_output = os.getenv("SOUND_OUTPUT")
    
    print("recording")
    SoundHandler.record(sound_input)
    print("done recording")

    question = SpeechModels.to_text(sound_input)
    print(question)

    print("asking")
    handler = QuestionHandler()
    response = handler.ask(question)
    
    SpeechModels.to_speech(response, filename=  sound_output )
    print("playing")
    SoundHandler.play(sound_output) 
    print("done playing")

if __name__ == '__main__':
    main()

