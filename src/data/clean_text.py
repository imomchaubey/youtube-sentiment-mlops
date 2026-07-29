"""
Text cleaning utilities for sentiment analysis.
Cleans raw text while preserving negation words critical to sentiment meaning.
"""

import re
import nltk
from nltk.corpus import stopwords

# Load NLTK's default English stopwords
_stop_words = set(stopwords.words("english"))

# Negation words we must NEVER remove — they flip sentiment meaning
NEGATION_WORDS = {
    "no", "not", "nor", "never", "none", "nobody", "nothing",
    "neither", "nowhere", "cannot", "cant", "don", "dont",
    "doesn", "doesnt", "didn", "didnt", "won", "wont",
    "wouldn", "wouldnt", "couldn", "couldnt", "shouldn", "shouldnt",
    "isn", "isnt", "aren", "arent", "wasn", "wasnt", "weren", "werent"
}

# Final stopword set: default list minus our protected negation words
SAFE_STOPWORDS = _stop_words - NEGATION_WORDS


def clean_text(text: str) -> str:
    """
    Clean a single piece of text:
    - Lowercase
    - Remove URLs, mentions, punctuation, numbers, extra whitespace
    - Remove stopwords EXCEPT negation words
    """
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)      # remove URLs
    text = re.sub(r"@\w+", "", text)                 # remove @mentions
    text = re.sub(r"[^a-z\s]", "", text)              # keep only letters and spaces
    text = re.sub(r"\s+", " ", text).strip()          # collapse extra whitespace

    tokens = text.split()
    tokens = [word for word in tokens if word not in SAFE_STOPWORDS]

    return " ".join(tokens)


if __name__ == "__main__":
    # Quick manual test cases
    samples = [
        "This movie is NOT good at all!!",
        "I don't think this was a bad decision.",
        "Check this out: https://example.com @someone",
        "This is absolutely amazing and wonderful",
    ]
    for s in samples:
        print(f"Original: {s}")
        print(f"Cleaned:  {clean_text(s)}\n")