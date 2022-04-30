

from nlp.analyse import _all_str, is_close_match
from nlp.setup import _get_french_tokenizer as _tokenizer, _download


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


def score_wordchain(tokenized_string, wordchain, allow_fragmentation=7):
    # allow fragmentation allows for the number of words we can skip ahead to find what we want
    # Assuming both are List[PunktToken]
    score = 0
    str_wordchain = _all_str(wordchain)
    for i in range(0, len(tokenized_string) - len(wordchain) + 1):
        # Allow minor differences
        wordchain_index = 0
        offset_search_index = 0
        while wordchain_index < len(wordchain) and offset_search_index < allow_fragmentation + 1 and i + offset_search_index < len(tokenized_string):
            # While in valid regions
            if is_close_match(str(tokenized_string[i+offset_search_index]), str_wordchain[wordchain_index]):
                # print(f"!! Strayed {offset_search_index} from {i} to find {str_wordchain[wordchain_index]} of {str_wordchain}. Found {str(tokenized_string[i+offset_search_index])}")
                # Score lower if strayed far
                score += 1 if offset_search_index == 0 else 1/offset_search_index
                wordchain_index += 1
                if wordchain_index == len(str_wordchain):
                    # This worchain has made it to the end of testing
                    return score
            # else:
            #     print(f"Straying {offset_search_index} from {i} to find {str_wordchain[wordchain_index]} of {str_wordchain}. Found {str(tokenized_string[i+offset_search_index])}")
            offset_search_index += 1
    
    # Was not a match, score 0
    return 0


def calculate_score_list(tokenized_string, word_chain_list):
    results = []
    for wordchain in word_chain_list:
        score = score_wordchain(tokenized_string, wordchain)
        if score > 0:
            results.append((wordchain, score))

    return results