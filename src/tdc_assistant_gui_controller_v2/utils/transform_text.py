originals_and_replacements = {
    "`": "",
    "\n": "{VK_RETURN}{VK_SHIFT HOME}{VK_SHIFT HOME}{BACKSPACE}",
}


def transform_text(text: str):
    transformed_text = "\n\n// Adam added this:\n"
    for ch in text:
        if ch in "{}()":
            transformed_text += "{" + ch + "}"
        else:
            transformed_text += ch

    for original, replacement in originals_and_replacements.items():
        transformed_text = transformed_text.replace(original, replacement)

    return "{VK_SPACE}".join(transformed_text.split()) + "{VK_RETURN}"
