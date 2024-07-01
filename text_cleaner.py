import re

def clean_description(description):
    cleaned_text = description.lower()
    cleaned_text = re.sub(r'[^A-Za-z0-9]+', ' ', cleaned_text)
    return cleaned_text