
from nlp.analyse import positive_negative_count


def _test():
    tests = [
        ("je n'aime pas", False),
        ("je suis tout à fait d'accord", True),
        ("je trouve pas que ce soit une mauvaise idée", True)
    ]
    results = []

    for (string, res) in tests:
        pos, neg = positive_negative_count(string)
        results.append((string, pos, neg, pos > neg, res, 'success' if (pos > neg) == res else 'fail'))

    print(results)

_test()