"""
Utility functions for language code retrieval and management.
"""

LANGUAGE_CODES = {
    "english": "en",
    "yoruba": "yo",
    "igbo": "ig",
    "hausa": "ha",
    "multi" : "multi"
}

SUPPORTED_LANGUAGES = list(LANGUAGE_CODES.keys())

def is_language_supported(language: str) -> bool:
    """
    Checks if a given language is supported.

    :param language: The name of the language.
    :return: True if supported, False otherwise.
    """
    
    return language.lower() in SUPPORTED_LANGUAGES

def get_language_code(language: str) -> str:
    """
    Retrieves the language code for a given language name.

    :param language: The name of the language.
    :return: The corresponding language code, or an empty string if not found.
    """
    
    return LANGUAGE_CODES.get(language.lower(), "")

def get_language(language_code: str) -> str:
    """
    Retrieves the language name for a given language code.

    :param language_code: The language code.
    :return: The corresponding language name, or an empty string if not found.
    """
    for name, code in LANGUAGE_CODES.items():
        if code == language_code.lower():
            return name
    return ""