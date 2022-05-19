from pynput.keyboard import Controller, Key, Listener
from pynput.keyboard._win32 import KeyCode
from threading import Thread, Lock, Condition


stopScript = False
# variables that ensure thread communications
notification = Condition()
writing = Lock()

keyboardController = Controller()
keyPressed = None
mapping = {
    'a' : 'i',
}

# listen keyboard
# if esc is pressed exit script
# if key pressed is a char
# send a notification to writer_thread only if writer_thread is not writing
def on_press(key):
    global keyPressed
    global stopScript
    print(type(key))
    if key == Key.esc:
        stopScript = True
        return False
    if writing.locked() == False:
        keyPressed = key
        notification.acquire()
        notification.notify()
        notification.release()

# wait for a notification from listener_thread then write
def thread_function():
    global keyPressed
    while(True):
        notification.acquire()
        notification.wait()
        writing.acquire()
        try:
            if isinstance(keyPressed, KeyCode):
                key = mapping[keyPressed.char]
                keyboardController.press(Key.backspace)
            else:
                key = mapping[keyPressed]
            keyboardController.type(key)
        except:
            print('no assigned key')
        writing.release()

# writing thread
writer = Thread(target=thread_function, args=(), daemon=True)

# listening thread
listener = Listener(on_press=on_press)

try:
    writer.start()
    listener.start()
    listener.join()
except:
    print('error')
