import time
from deep_translator import GoogleTranslator
from deep_translator.exceptions import RequestError, TooManyRequests, TranslationNotFound
from utils.decorators import calc_execution_time
from utils.languages import get_language_code


class LinguaFlowTranslate:

    def __init__(self, target_language: str, source_language: str = "auto", method: str = "googledeep") -> None:
        """
        Translates text from source to target language.

        Supported methods:
        - googledeep  : deep_translator (default, recommended)
        - googlecloud : Google Cloud Translation API (requires credentials)
        """
        self.source_language = source_language
        self.target_language = target_language
        self.method = method

        self.__source_language_code = get_language_code(source_language) if source_language != "auto" else "auto"
        self.__target_language_code = get_language_code(target_language)

        self.__translators = {
            "googledeep":  self.__translate_with_googledeep,
            "googlecloud": self.__translate_with_googlecloud,
        }

    def __repr__(self):
        return f"Translate(source={self.source_language}, target={self.target_language}, method={self.method})"

    def __translate_with_googledeep(self, text: str, max_attempts: int = 3) -> str:
        """Translate using deep_translator. Retries on transient scraping
        failures (Google's unofficial translate endpoint occasionally returns
        a page deep_translator can't parse, or rate-limits the request)."""
        translator = GoogleTranslator(
            source=self.__source_language_code,
            target=self.__target_language_code
        )
        last_error = None
        for attempt in range(max_attempts):
            try:
                return translator.translate(text)
            except (TranslationNotFound, TooManyRequests, RequestError) as e:
                last_error = e
                if attempt < max_attempts - 1:
                    time.sleep(1.5)
        raise last_error

    def __translate_with_googlecloud(self, text: str) -> str:
        """Translate using Google Cloud Translation API (lazy import)."""
        from google.cloud import translate_v2 as translate
        client = translate.Client()
        result = client.translate(
            text,
            source_language=self.__source_language_code,
            target_language=self.__target_language_code
        )
        return result["translatedText"]

    @calc_execution_time
    def translate(self, text: str) -> str:
        """Translate text using the specified method."""
        translator = self.__translators.get(self.method, self.__translate_with_googledeep)
        return translator(text)
