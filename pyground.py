from SoundHandler import SoundHandler
from SpeechModels import SpeechModels
from gpt_service import QuestionHandler

def main():
    SoundHandler.record()
    question = SpeechModels.to_text()
    print(question)
    response = QuestionHandler.ask(question)
    print(response)
    SpeechModels.to_speech(response)
    SoundHandler.play()

if __name__ == '__main__':
    main()

