import keyboard
import threading
import record
import speech_to_text

def app():
    print('Recording...')
    record.record(5)
    print('Done recording')
    speech_to_text.listen('output.wav')



def background():
    # Your background function here
    pass

# Start the background thread
def start():
    thread = threading.Thread(target=background)
    thread.start()

    # Wait for the key combination to be pressed
    keyboard.add_hotkey('ctrl+alt+p', app)

    # Keep the script runningw
    keyboard.wait()

if __name__ == '__main__':
    start()