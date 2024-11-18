import pyperclip
from pynput import keyboard
from melo.api import TTS
import time
from playsound import playsound  # Import playsound

# Set up TTS model and configurations
speed = 1.3
device = 'cpu'  # Will automatically use GPU if available
model = TTS(language='EN', device=device)
speaker_ids = model.hps.data.spk2id
output_path = 'clipboard_audio.wav'

import re

# Mapping of letters to their phonetic pronunciations
phonetic_map = {
    'A': 'ay', 'B': 'bee', 'C': 'see', 'D': 'dee', 'E': 'ee',
    'F': 'ef', 'G': 'gee', 'H': 'aitch', 'I': 'eye', 'J': 'jay',
    'K': 'kay', 'L': 'el', 'M': 'em', 'N': 'en', 'O': 'oh',
    'P': 'pee', 'Q': 'cue', 'R': 'ar', 'S': 'ess', 'T': 'tee',
    'U': 'you', 'V': 'vee', 'W': 'double-u', 'X': 'ex', 'Y': 'why',
    'Z': 'zee'
}

def expand_acronyms(text):
    # Regular expression to find acronyms (all uppercase words)
    def replace_with_phonetic(match):
        acronym = match.group(1)
        return ' '.join(phonetic_map.get(letter, letter) for letter in acronym)

    return re.sub(r'([A-Z]{2,})', replace_with_phonetic, text)

def on_activate():
    # Get the current text from the clipboard
    current_text = pyperclip.paste()
    print("Selected text:", current_text)
    
    # Expand acronyms in the text
    expanded_text = expand_acronyms(current_text)
    print("Expanded text:", expanded_text)
    
    # Convert the expanded text to audio
    start_time = time.time()
    model.tts_to_file(expanded_text, speaker_ids['EN-BR'], output_path, speed=speed)
    execution_time = time.time() - start_time
    print(f"Audio generation took {execution_time:.2f} seconds")
    
    # Play the generated audio file
    playsound(output_path)

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
