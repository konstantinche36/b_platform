from pynput import keyboard
import pyperclip
import datetime

VAL = ['source_%Y_%m_%d_%H_%M_%S', '%Y_%m_%d_%H_%M_%S_result']
KEYS = [keyboard.KeyCode(char='S'), keyboard.KeyCode(char='D')]


def get_text(text_template):
    today = datetime.datetime.today()
    print(type(today))
    return today.strftime(text_template)


# The key combination to check
COMBINATIONS = [
    {keyboard.Key.shift, KEYS[0]},
    {keyboard.Key.shift, KEYS[1]}
]

# The currently active modifiers
current = set()


def execute():
    pyperclip.copy(get_text(VAL[0] if KEYS[0] in current else VAL[1]))
    # pyperclip.copy('The text to be copied to the clipboard.')
    # spam = pyperclip.paste()


def on_press(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            execute()


def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.remove(key)


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
