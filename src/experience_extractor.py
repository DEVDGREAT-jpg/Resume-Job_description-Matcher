import re

def extract_experience(text):

    print("EXPERIENCE TEXT:", text)

    pattern = r'(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)'

    matches = re.findall(pattern, text.lower())

    print("EXPERIENCE MATCHES:", matches)

    if matches:
        experience = [float(match) for match in matches]
        return max(float(match) for match in matches)

    return 0
