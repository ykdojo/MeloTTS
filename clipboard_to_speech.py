import pyperclip
from pynput import keyboard
from melo.api import TTS
import time
import os
import platform

# Set up TTS model and configurations
speed = 1.3
device = 'cpu'  # Will automatically use GPU if available
model = TTS(language='EN', device=device)
speaker_ids = model.hps.data.spk2id
output_path = 'clipboard_audio.wav'

def on_activate():
    # Get the current text from the clipboard
    current_text = pyperclip.paste()
    print("Selected text:", current_text)
    
    # Convert the clipboard text to audio
    start_time = time.time()
    model.tts_to_file(current_text, speaker_ids['EN-BR'], output_path, speed=speed)
    execution_time = time.time() - start_time
    print(f"Audio generation took {execution_time:.2f} seconds")
    
    # Open the generated audio file with the default media player
    if platform.system() == 'Darwin':  # macOS
        # os.system(f'open {output_path}')
        os.system(f'qlmanage -p {output_path}')
    elif platform.system() == 'Windows':  # Windows
        os.system(f'start {output_path}')
    elif platform.system() == 'Linux':  # Linux
        os.system(f'xdg-open {output_path}')

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
