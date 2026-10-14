import re

def preprocess_text(text):

    #lower case 
    text = text.lower()

    #remove extra whitespace
    text = re.sub(r'\s+',' ',text)

    text = text.strip()

    return text

