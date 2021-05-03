from fuzzywuzzy import fuzz


def check_answer(answer_given, expected_answer):
    given = clean_text(answer_given)
    expected = clean_text(expected_answer)
    return fuzz.partial_ratio(given, expected) >= 80


def clean_text(text):
    text = text.lower()
    text = text.strip()
    return text
