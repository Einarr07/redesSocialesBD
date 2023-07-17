def myCapitalize(text):
    if not isinstance(text, str):
        return ""
    if text:
        return " ".join([h.capitalize() for h in text.split()])
    return ""
