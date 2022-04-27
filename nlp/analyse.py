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
    'd\'accord'
]

_negative_word_chains = [
    'non',
    'no',
    'pas d\'accord',
    'contre',
    'pas d\'acc',
    'pas'
]

_download()
tokenizer = _tokenizer()

# prepare word chains for analysis comparison
positive_word_chains = [*map(lambda wc: [*tokenizer._tokenize_words(wc)], _positive_word_chains)]
negative_word_chains = [*map(lambda wc: [*tokenizer._tokenize_words(wc)], _negative_word_chains)]

def _all_str(punkt_tokens):
    return list(map(str, punkt_tokens))


def contains_wordchain(tokenized_string, wordchain):
    # Assuming both are List[PunktToken]
    str_wordchain = _all_str(wordchain)
    for i in range(0, len(tokenized_string) - len(wordchain) + 1):
        print(i, str_wordchain, _all_str(tokenized_string[i:i+len(wordchain)]) )
        if _all_str(tokenized_string[i:i+len(wordchain)]) == str_wordchain:
            return True
    
    return False

def contains_wordchains(tokenized_string, word_chain_list):
    total = 0
    for wordchain in word_chain_list:
        if contains_wordchain(tokenized_string, wordchain):
            total += 1
    
    return total

def positive_negative_count(string):
    string = [*tokenizer._tokenize_words(string)]
    return (contains_wordchains(string, positive_word_chains), contains_wordchains(string, negative_word_chains))
