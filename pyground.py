from SoundHandler import SoundHandler
from SpeechModels import SpeechModels
from gpt_service import QuestionHandler
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    print("recording")
    sound_input = os.getenv("SOUND_INPUT")
    sound_output = os.getenv("SOUND_OUTPUT")
    #SoundHandler.record(sound_input)
    print("done recording")
    #question = SpeechModels.to_text()
    #print(question)
    print("asking")
    handler = QuestionHandler()
    response = handler.ask("Hey, bing how are you doing today?")
    print(response)
    SpeechModels.to_speech(response, filename=  sound_output )
    print("playing")
    SoundHandler.play(sound_output) 
    print("done playing")

if __name__ == '__main__':
    main()

