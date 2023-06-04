import keyboard, threading, SoundHandler, speech_to_text, gpt_service, text_to_speach


def ask_gpt():
    print('Recording...')
    SoundHandler.record()
    print('Done recording')
    question = speech_to_text.listen('output.wav')
    response = gpt_service.ask_gpt(question)
    print(response)
    text_to_speach.speak(response)

def background():
    # Your background function here
    pass

# Start the background thread
def start_app():
    thread = threading.Thread(target=background)
    thread.start()

    # Wait for the key combination to be pressed
    keyboard.add_hotkey('ctrl+alt+p', ask_gpt)

    # Keep the script running
    keyboard.wait()

if __name__ == '__main__':
    start_app()