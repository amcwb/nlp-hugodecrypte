import nltk
import os

download_path = os.path.join('.', '.download')
punkt_path = os.path.join(download_path, 'tokenizers', 'punkt')

def _download():
    # Override nltk paths
    # nltk.data.path = [download_path]̃
    nltk.download('punkt', download_dir = download_path)

def _get_french_tokenizer():
    if not os.path.exists(punkt_path):
        raise FileNotFoundError(punkt_path)
    tokenizer = nltk.data.load(os.path.join(punkt_path, 'french.pickle'), format="pickle")
    return tokenizer