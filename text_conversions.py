import re
from mappings import phonetic_map, japanese_phonetic_map
from fugashi import Tagger  # Import Fugashi for Kanji conversion

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

def convert_fullwidth_to_halfwidth(text):
    return text.translate(str.maketrans('０１２３４５６７８９', '0123456789'))

def convert_single_numbers_to_kanji(text):
    # Only convert isolated single digits (0-9) to kanji
    return re.sub(r'(?<!\d)(\d)(?!\d)', lambda m: number_to_kanji.get(m.group(1), m.group(1)), text)

def convert_kanji_to_katakana(text):
    tagger = Tagger()
    tokens = tagger(text)
    katakana_text = ''.join(
        token.feature.kana if token.feature.kana and re.match(r'[\u4E00-\u9FFF]', token.surface) else token.surface
        for token in tokens
    )
    return katakana_text
