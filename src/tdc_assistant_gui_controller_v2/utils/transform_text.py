originals_and_replacements_before = {
    "`": "",
}

originals_and_replacements_after = {
    "\n": "{VK_RETURN}{VK_LSHIFT HOME}{VK_LSHIFT HOME}{BACKSPACE}",
}


def transform_text(text: str):
    transformed_text = "\n\n// Adam added this:\n"
    for ch in text:
        if ch in "{}()":
            transformed_text += "{" + ch + "}"
        else:
            transformed_text += ch

    for original, replacement in originals_and_replacements_before.items():
        transformed_text = transformed_text.replace(original, replacement)

    transformed_text = "{VK_SPACE}".join(transformed_text.split()) + "{VK_RETURN}"

    for original, replacement in originals_and_replacements_after.items():
        transformed_text = transformed_text.replace(original, replacement)

    return transform_text
