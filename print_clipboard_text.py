import pyperclip
from pynput import keyboard

def on_activate():
    current_text = pyperclip.paste()
    print("Selected text:", current_text)

def for_canonical(f):
    return lambda k: f(l.canonical(k))

# Define the hotkey for <shift>+<alt>+v
hotkey = keyboard.HotKey(
    keyboard.HotKey.parse('<shift>+<alt>+v'),
    on_activate
)

def on_press(key):
    try:
        # Check if the special character is pressed
        if key.char == '◊':  # Replace '◊' with the actual character if different
            on_activate()
    except AttributeError:
        # Handle special keys that don't have a char attribute
        pass

# Set up the listener with both the hotkey and the special character check
with keyboard.Listener(
        on_press=lambda k: (on_press(k), for_canonical(hotkey.press)(k)),
        on_release=for_canonical(hotkey.release)) as l:
    l.join()
