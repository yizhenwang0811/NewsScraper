DELETE_WORDS = ['\n', '\t', '\xa0']


def remove_words(text_string, delete_words=DELETE_WORDS):
    for word in delete_words:
        text_string = text_string.replace(word, '')
    return text_string


def clean_text(text):
    return ' '.join(text.split()).lower()
