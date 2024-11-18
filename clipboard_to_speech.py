import pyperclip
from pynput import keyboard
from melo.api import TTS
import time
from playsound import playsound
import re
from fugashi import Tagger  # Import Fugashi for Kanji conversion

# Set up TTS models and configurations
speed = 1.3
device = 'cpu'  # Will automatically use GPU if available
english_model = TTS(language='EN', device=device)
japanese_model = TTS(language='JP', device=device)
english_speaker_ids = english_model.hps.data.spk2id
japanese_speaker_ids = japanese_model.hps.data.spk2id
output_path_en = 'clipboard_audio_en.wav'
output_path_jp = 'clipboard_audio_jp.wav'

# Mapping of letters to their phonetic pronunciations
phonetic_map = {
    'A': 'ay', 'B': 'bee', 'C': 'see', 'D': 'dee', 'E': 'ee',
    'F': 'ef', 'G': 'gee', 'H': 'aitch', 'I': 'eye', 'J': 'jay',
    'K': 'kay', 'L': 'el', 'M': 'em', 'N': 'en', 'O': 'oh',
    'P': 'pee', 'Q': 'cue', 'R': 'ar', 'S': 'ess', 'T': 'tee',
    'U': 'you', 'V': 'vee', 'W': 'double-u', 'X': 'ex', 'Y': 'why',
    'Z': 'zee'
}

# Mapping of letters to their phonetic pronunciations in Katakana
japanese_phonetic_map = {
    # Half-width characters
    'A': 'エー', 'B': 'ビー', 'C': 'シー', 'D': 'ディー', 'E': 'イー',
    'F': 'エフ', 'G': 'ジー', 'H': 'エイチ', 'I': 'アイ', 'J': 'ジェイ',
    'K': 'ケー', 'L': 'エル', 'M': 'エム', 'N': 'エヌ', 'O': 'オー',
    'P': 'ピー', 'Q': 'キュー', 'R': 'アール', 'S': 'エス', 'T': 'ティー',
    'U': 'ユー', 'V': 'ヴィー', 'W': 'ダブリュー', 'X': 'エックス', 'Y': 'ワイ',
    'Z': 'ゼット',
    'a': 'エー', 'b': 'ビー', 'c': 'シー', 'd': 'ディー', 'e': 'イー',
    'f': 'エフ', 'g': 'ジー', 'h': 'エイチ', 'i': 'アイ', 'j': 'ジェイ',
    'k': 'ケー', 'l': 'エル', 'm': 'エム', 'n': 'エヌ', 'o': 'オー',
    'p': 'ピー', 'q': 'キュー', 'r': 'アール', 's': 'エス', 't': 'ティー',
    'u': 'ユー', 'v': 'ヴィー', 'w': 'ダブリュー', 'x': 'エックス', 'y': 'ワイ',
    'z': 'ゼット',
    # Full-width characters
    'Ａ': 'エー', 'Ｂ': 'ビー', 'Ｃ': 'シー', 'Ｄ': 'ディー', 'Ｅ': 'イー',
    'Ｆ': 'エフ', 'Ｇ': 'ジー', 'Ｈ': 'エイチ', 'Ｉ': 'アイ', 'Ｊ': 'ジェイ',
    'Ｋ': 'ケー', 'Ｌ': 'エル', 'Ｍ': 'エム', 'Ｎ': 'エヌ', 'Ｏ': 'オー',
    'Ｐ': 'ピー', 'Ｑ': 'キュー', 'Ｒ': 'アール', 'Ｓ': 'エス', 'Ｔ': 'ティー',
    'Ｕ': 'ユー', 'Ｖ': 'ヴィー', 'Ｗ': 'ダブリュー', 'Ｘ': 'エックス', 'Ｙ': 'ワイ',
    'Ｚ': 'ゼット',
    'ａ': 'エー', 'ｂ': 'ビー', 'ｃ': 'シー', 'ｄ': 'ディー', 'ｅ': 'イー',
    'ｆ': 'エフ', 'ｇ': 'ジー', 'ｈ': 'エイチ', 'ｉ': 'アイ', 'ｊ': 'ジェイ',
    'ｋ': 'ケー', 'ｌ': 'エル', 'ｍ': 'エム', 'ｎ': 'エヌ', 'ｏ': 'オー',
    'ｐ': 'ピー', 'ｑ': 'キュー', 'ｒ': 'アール', 'ｓ': 'エス', 'ｔ': 'ティー',
    'ｕ': 'ユー', 'ｖ': 'ヴィー', 'ｗ': 'ダブリュー', 'ｘ': 'エックス', 'ｙ': 'ワイ',
    'ｚ': 'ゼット'
}

def expand_acronyms(text):
    def replace_with_phonetic(match):
        acronym = match.group(1)
        return ' '.join(phonetic_map.get(letter, letter) for letter in acronym)

    return re.sub(r'([A-Z]{2,})', replace_with_phonetic, text)

def convert_text_to_japanese_phonetic(text):
    phonetic_text = ''
    for letter in text:
        converted_letter = japanese_phonetic_map.get(letter, letter)
        phonetic_text += converted_letter
    return phonetic_text

def convert_kanji_to_katakana(text):
    tagger = Tagger()
    tokens = tagger(text)
    katakana_text = ''.join(
        token.feature.kana if token.feature.kana and re.match(r'[\u4E00-\u9FFF]', token.surface) else token.surface
        for token in tokens
    )
    return katakana_text

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
    
    # Convert Kanji to Katakana
    katakana_text = convert_kanji_to_katakana(current_text)
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
