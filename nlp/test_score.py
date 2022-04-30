
from nlp.analyse_score import calculate_score_list, tokenizer, positive_word_chains, negative_word_chains
from pprint import pprint

def _test():
    tests = [
        ("je n'aime pas", False),
        ("je suis tout à fait d'accord", True),
        ("je trouve pas que ce soit une mauvaise idée", True)
    ]
    results = []

    for (orig_string, res) in tests:
        string = [*tokenizer._tokenize_words(orig_string)]
        print(orig_string, '->')
        pprint(calculate_score_list(string, positive_word_chains))
        pprint(calculate_score_list(string, negative_word_chains))

    print(results)

_test()