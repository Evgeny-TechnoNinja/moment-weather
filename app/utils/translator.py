from googletrans import Translator  # type: ignore
from app.config import URL_TRANSLATE_API


def translate(word: str, lang: str) -> str:
    """
    Translates words from one language to another
    :param word: words to be translated
    :param lang: language to be translated
    :return: string translation
    """
    return Translator(service_urls=[URL_TRANSLATE_API]).translate(word, dest=lang).text
