from re import L
from nlp.setup import _get_french_tokenizer as _tokenizer, _download
import difflib

_positive_word_chains = [
    'oui',
    'oé',
    'ouais',
    'ouep',
    'oue',
    'bien-sûr',
    'bien-sur',
    'biensûr',
    'biensur',
    'bien sûr',
    'bien sur',
    'd\'acc',
    'd\'accord',
    'pas une mauvaise idée'
]

_negative_word_chains = [
    'non',
    'no',
    'pas d\'accord',
    'contre',
    'pas d\'acc',
    'une mauvaise idée',
]

_download()
tokenizer = _tokenizer()

# prepare word chains for analysis comparison
positive_word_chains = [*map(lambda wc: [*tokenizer._tokenize_words(wc)], _positive_word_chains)]
negative_word_chains = [*map(lambda wc: [*tokenizer._tokenize_words(wc)], _negative_word_chains)]

def _all_str(punkt_tokens):
    return list(map(str, punkt_tokens))

def is_close_match(word1, word2, cutoff=0.8):
    s = difflib.SequenceMatcher()
    s.set_seq1(word1)
    s.set_seq2(word2)
    # Pretty much copied from difflib.get_close_matches but for a single entity
    return s.real_quick_ratio() >= cutoff and \
        s.quick_ratio() >= cutoff and \
        s.ratio() >= cutoff


def contains_wordchain(tokenized_string, wordchain, allow_fragmentation=7):
    # allow fragmentation allows for the number of words we can skip ahead to find what we want
    # Assuming both are List[PunktToken]
    str_wordchain = _all_str(wordchain)
    for i in range(0, len(tokenized_string) - len(wordchain) + 1):
        # Allow minor differences
        wordchain_index = 0
        offset_search_index = 0
        while wordchain_index < len(wordchain) and offset_search_index < allow_fragmentation + 1 and i + offset_search_index < len(tokenized_string):
            # While in valid regions
            if is_close_match(str(tokenized_string[i+offset_search_index]), str_wordchain[wordchain_index]):
                # print(f"!! Strayed {offset_search_index} from {i} to find {str_wordchain[wordchain_index]} of {str_wordchain}. Found {str(tokenized_string[i+offset_search_index])}")
                wordchain_index += 1
                if wordchain_index == len(str_wordchain):
                    # This worchain has made it to the end of testing
                    return True
            # else:
            #     print(f"Straying {offset_search_index} from {i} to find {str_wordchain[wordchain_index]} of {str_wordchain}. Found {str(tokenized_string[i+offset_search_index])}")
            offset_search_index += 1
    
    return False


def contains_wordchains(tokenized_string, word_chain_list):
    total = 0
    for wordchain in word_chain_list:
        if contains_wordchain(tokenized_string, wordchain):
            total += 1
            print(wordchain, "triggered", tokenized_string)
    
    return total

def positive_negative_count(string):
    string = [*tokenizer._tokenize_words(string)]
    return (contains_wordchains(string, positive_word_chains), contains_wordchains(string, negative_word_chains))
