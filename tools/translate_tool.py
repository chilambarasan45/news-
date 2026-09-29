import re
import requests
from core.tool_registry import tool

LANGUAGE_CODES = {
    "english": "en", "french": "fr", "spanish": "es", "german": "de",
    "hindi": "hi", "tamil": "ta", "telugu": "te", "kannada": "kn",
    "malayalam": "ml", "japanese": "ja", "chinese": "zh", "korean": "ko",
    "arabic": "ar", "russian": "ru", "portuguese": "pt", "italian": "it",
    "bengali": "bn", "marathi": "mr", "gujarati": "gu", "punjabi": "pa",
    "urdu": "ur", "turkish": "tr", "vietnamese": "vi", "thai": "th",
    "dutch": "nl", "polish": "pl", "greek": "el", "hebrew": "he",
    "indonesian": "id",
}


@tool
def translate_text(query: str) -> str:
    """
    Translate text into another language.
    The query should describe the request, e.g. 'translate hello to french'.
    Uses the free MyMemory translation API (no API key required).
    """
    try:
        match = re.search(
            r"translate\s+(.+?)\s+(?:to|into)\s+([A-Za-z]+)$",
            query.strip(),
            re.IGNORECASE,
        )
        if not match:
            return (
                "❌ Could not understand the translation request. "
                "Please use a format like 'translate hello to french'."
            )

        text = match.group(1).strip()
        target_language_name = match.group(2).strip().lower()

        target_code = LANGUAGE_CODES.get(target_language_name)
        if not target_code:
            return f"❌ Sorry, I don't recognize the language '{target_language_name}'."

        url = "https://api.mymemory.translated.net/get"
        params = {"q": text, "langpair": f"en|{target_code}"}
        resp = requests.get(url, params=params, timeout=5)
        data = resp.json()

        translated = data.get("responseData", {}).get("translatedText")
        if not translated:
            return f"❌ Could not translate '{text}' to {target_language_name}."

        return f"'{text}' in {target_language_name.title()}: {translated}"
    except Exception as e:
        return f"❌ Error translating text: {e}"
