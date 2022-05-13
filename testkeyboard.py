from pynput import keyboard
from pynput.keyboard import Controller, Key

# gestionnaire du clavier
# écrit du text avec type()
# génère une simulation d'appuie de touche avec press()
keyboardController = Controller()

# fonction appelé lors de l'appuie d'une touche
# try and catch pour éviter les crashs
# ERREUR : key.char provque des erreurs pour les touches présente dans Key
# car ils ne sont peut être pas considérés comme des 'char'
# exemple: backspace, space
# keyboardController.press(Key.backspace) génère une erreur
# car elle simule l'appuie d'une touche présente dans Key

def on_press(key):
    try:
        if key.char == 'z':
            # simule backspace pour effacer le char 'z'
            keyboardController.press(Key.backspace)

            # écrit le mot souhaité dans le champs actif
            keyboardController.type('caca')
    except AttributeError:
        print('error')

# fonction appelé lors du relachement d'une touche
def on_release(key):
    # Si la touche est esc, met fin au script
    if key == Key.esc:
        return False

# boucle d'écoute d'event
# on_press = <fonction à executé lors de l'appuie d'une touche>
# on_release = <fonction à executé lors du relachement d'une touche>
with keyboard.Listener(
    on_press = on_press,
    on_release = on_release) as listener:
    listener.join()
