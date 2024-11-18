import pyperclip
from pynput import keyboard
from melo.api import TTS
import time
from playsound import playsound
from text_conversions import *
from pydub import AudioSegment

# Set up TTS models and configurations
speed = 1.3
device = 'cpu'  # Will automatically use GPU if available
english_model = TTS(language='EN', device=device)
japanese_model = TTS(language='JP', device=device)
english_speaker_ids = english_model.hps.data.spk2id
japanese_speaker_ids = japanese_model.hps.data.spk2id
output_path_en = 'clipboard_audio_en.wav'
output_path_jp = 'clipboard_audio_jp.wav'

def play_sound_with_volume_adjustment(file_path, increase_by_db=7):
    # Increase volume by the specified dB
    audio = AudioSegment.from_file(file_path)
    louder_audio = audio + increase_by_db
    louder_audio.export(file_path, format="wav")
    
    # Play the sound
    playsound(file_path)

def on_activate_english():
    current_text = pyperclip.paste()
    print("Selected text:", current_text)
    
    expanded_text = expand_acronyms(current_text)
    print("Expanded text:", expanded_text)
    
    start_time = time.time()
    english_model.tts_to_file(expanded_text, english_speaker_ids['EN-BR'], output_path_en, speed=speed)
    execution_time = time.time() - start_time
    print(f"Audio generation took {execution_time:.2f} seconds")
    
    play_sound_with_volume_adjustment(output_path_en)

def on_activate_japanese():
    current_text = pyperclip.paste()
    print("Selected text:", current_text)
    
    # Add maru before closing kagikakko
    modified_text = add_maru_before_closing_kagikakko(current_text)
    print("Modified text:", modified_text)
    
    # Convert full-width numbers to half-width numbers
    halfwidth_text = convert_fullwidth_to_halfwidth(modified_text)
    print("Half-width text:", halfwidth_text)

    # Convert single numbers to Kanji
    kanji_text = convert_single_numbers_to_kanji(halfwidth_text)
    print("Kanji text:", kanji_text)

    # Convert Kanji to Katakana
    katakana_text = convert_kanji_to_katakana(kanji_text)
    print("Katakana text:", katakana_text)

    # Convert text to Japanese phonetic form
    phonetic_text = convert_text_to_japanese_phonetic(katakana_text)
    print("Phonetic text:", phonetic_text)

    start_time = time.time()
    japanese_model.tts_to_file(phonetic_text, japanese_speaker_ids['JP'], output_path_jp, speed=speed)
    execution_time = time.time() - start_time
    print(f"Audio generation took {execution_time:.2f} seconds")

    play_sound_with_volume_adjustment(output_path_jp)
    
def for_canonical(f):
    return lambda k: f(l.canonical(k))

# Define the hotkey for <shift>+<alt>+d
hotkey_english = keyboard.HotKey(
    keyboard.HotKey.parse('<shift>+<alt>+v'),
    on_activate_english
)

hotkey_japanese = keyboard.HotKey(
    keyboard.HotKey.parse('<shift>+<alt>+d'),
    on_activate_japanese
)

def on_press(key):
    try:
        if key.char == '◊':
            on_activate_english()
        if key.char == 'Î':
            on_activate_japanese()
    except AttributeError:
        pass

# Set up the listener with both the hotkeys
with keyboard.Listener(
        on_press=lambda k: (on_press(k), for_canonical(hotkey_english.press)(k), for_canonical(hotkey_japanese.press)(k)),
        on_release=lambda k: (for_canonical(hotkey_english.release)(k), for_canonical(hotkey_japanese.release)(k))) as l:
    l.join()
