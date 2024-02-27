import re

def object_to_dict(obj: object) -> dict:
    if hasattr(obj, "__dict__"):
        obj_dict = obj.__dict__
        for key, val in obj_dict.items():
            if isinstance(val, list):
                obj_dict[key] = [object_to_dict(v) for v in val]
            else:
                obj_dict[key] = object_to_dict(val)
        return obj_dict
    else:
        return obj

def replace_unicode_characters(text):
    replacements = {
            "\u00a0": " ",   # Non-breaking space
            "\u201c": '"',    # Left double quotation mark
            "\u201d": '"',    # Right double quotation mark
            "\u2018": "'",    # Left single quotation mark
            "\u2019": "'",    # Right single quotation mark
            "\u2022": "*",    # Bullet point
            "\u2013": "-",    # En dash
            "\u2014": "--",   # Em dash
            "\u2026": "...",  # Ellipsis
            "\n": " ",        # Newline
    }

    text = re.sub(r"\s+", " ", text)

    for original, replacement in replacements.items():
        text = text.replace(original, replacement)

    return text
