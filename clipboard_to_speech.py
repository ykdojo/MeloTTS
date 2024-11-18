import pyperclip
from pynput import keyboard
from melo.api import TTS
import time
from playsound import playsound
from janome.tokenizer import Tokenizer
from text_conversions import (
    expand_acronyms,
    convert_text_to_japanese_phonetic,
    convert_fullwidth_to_halfwidth,
    convert_single_numbers_to_kanji,
    convert_kanji_to_katakana
)

# Set up TTS models and configurations
speed = 1.3
device = 'cpu'  # Will automatically use GPU if available
english_model = TTS(language='EN', device=device)
japanese_model = TTS(language='JP', device=device)
english_speaker_ids = english_model.hps.data.spk2id
japanese_speaker_ids = japanese_model.hps.data.spk2id
output_path_en = 'clipboard_audio_en.wav'
output_path_jp = 'clipboard_audio_jp.wav'

def segment_japanese_text(text):
    tokenizer = Tokenizer()
    sentences = []
    sentence = ''
    # Define a set of characters that can indicate the end of a sentence or segment
    sentence_endings = '。！？】』」』）〉》】〕〗〙〛'
    for token in tokenizer.tokenize(text, wakati=True):
        sentence += token
        if token in sentence_endings:
            sentences.append(sentence)
            sentence = ''
    if sentence:
        sentences.append(sentence)
    return sentences

def on_activate_english():
    current_text = pyperclip.paste()
    print("Selected text:", current_text)
    
    expanded_text = expand_acronyms(current_text)
    print("Expanded text:", expanded_text)
    
    start_time = time.time()
    english_model.tts_to_file(expanded_text, english_speaker_ids['EN-BR'], output_path_en, speed=speed)
    execution_time = time.time() - start_time
    print(f"Audio generation took {execution_time:.2f} seconds")
    
    playsound(output_path_en)

def on_activate_japanese():
    current_text = pyperclip.paste()
    print("Selected text:", current_text)
    
    # Segment text into sentences
    sentences = segment_japanese_text(current_text)
    print("Segmented sentences:", sentences)
    
    for sentence in sentences:
        # Convert full-width numbers to half-width numbers
        halfwidth_text = convert_fullwidth_to_halfwidth(sentence)
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
        
        playsound(output_path_jp)
    
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
