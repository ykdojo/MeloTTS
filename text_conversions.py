import re
from mappings import phonetic_map, japanese_phonetic_map
from fugashi import Tagger  # Import Fugashi for Kanji conversion
from janome.tokenizer import Tokenizer

def expand_acronyms(text):
    def replace_with_phonetic(match):
        pattern = match.group(0)
        result = []
        parts = pattern.split('-')
        
        for part in parts:
            # Ensure we don't match numbers with commas
            if re.match(r'^\d{1,3}(?:,\d{3})*', part):
                result.append(part)
                continue

            letter_num_match = re.match(r'([a-zA-Z])(\d+)', part)
            if letter_num_match:
                letter, number = letter_num_match.groups()
                result.append(f"{phonetic_map.get(letter, letter)} {number}")
            elif part.isupper() and len(part) >= 2:
                result.append(' '.join(phonetic_map.get(letter, letter) for letter in part))
            else:
                result.append(part)
        
        return '-'.join(result)

    # First handle percentages
    text = re.sub(r'(\d+)%', r'\1 percent', text)
    
    # Then handle the original acronym patterns
    pattern = r'([A-Z]{2,})|([a-zA-Z]\d+(?:-[a-zA-Z0-9]+)*)'
    return re.sub(pattern, replace_with_phonetic, text)

def add_maru_before_closing_kagikakko(text):
    # Use regular expression to find closing kagikakko not preceded by a maru
    return re.sub(r'(?<!。)(」)', '。\\1', text)

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

def segment_english_text(text):
    # Simple sentence segmentation based on punctuation
    sentence_endings = re.compile(r'(?<=[.!?]) +')
    sentences = sentence_endings.split(text)
    return sentences

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