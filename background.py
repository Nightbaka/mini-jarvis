import keyboard
import threading
import SoundHandler

def app():
    print('Recording...')
    SoundHandler.record(5)
    print('Done recording')



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