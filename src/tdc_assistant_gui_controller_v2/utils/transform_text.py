originals_and_replacements_before = {"`": "", " ": "{VK_SPACE}"}

originals_and_replacements_after = {
    "\n": "{VK_RETURN}{HOME}{HOME}{BACKSPACE}{VK_RETURN}"
}


def transform_text(text: str):
    transformed_text = "\n\n// Adam added this:\n"
    for ch in text:
        if ch in "{}()+_%":
            transformed_text += "{" + ch + "}"
        else:
            transformed_text += ch

    for original, replacement in originals_and_replacements_before.items():
        transformed_text = transformed_text.replace(original, replacement)

    for original, replacement in originals_and_replacements_after.items():
        transformed_text = transformed_text.replace(original, replacement)

    transformed_text += "{VK_RETURN}"

    return transformed_text
