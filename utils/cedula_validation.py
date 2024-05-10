import re

def process_text(text):
    # Remove spaces
    text = text.replace(" ", "")
    # Remove special characters using regex
    text = re.sub(r'\W+', '', text)
    return text

def cedula_validation(text):
    for character in text:
        if character.isdigit():
            return True
    return False

