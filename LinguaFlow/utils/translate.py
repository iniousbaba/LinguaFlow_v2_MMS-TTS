import time
from deep_translator import GoogleTranslator
from deep_translator.exceptions import RequestError, TooManyRequests, TranslationNotFound
from utils.decorators import calc_execution_time
from utils.languages import get_language_code
from utils.claude_client import claude_translate, claude_available


class LinguaFlowTranslate:

    def __init__(self, target_language: str, source_language: str = "auto", method: str = "googledeep") -> None:
        """
        Translates text from source to target language.

        Supported methods:
        - googledeep  : deep_translator / Google (default, recommended)
        - mymemory    : deep_translator / MyMemory (free, best-effort fallback)
        - claude      : Anthropic Claude (last-resort fallback)
        - googlecloud : Google Cloud Translation API (requires credentials)
        """
        self.source_language = source_language
        self.target_language = target_language
        self.method = method

        self.__source_language_code = get_language_code(source_language) if source_language != "auto" else "auto"
        self.__target_language_code = get_language_code(target_language)

        self.__translators = {
            "googledeep":  self.__translate_with_googledeep,
            "mymemory":    self.__translate_with_mymemory,
            "claude":      self.__translate_with_claude,
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
                result = translator.translate(text)
                if result and result.strip():
                    return result
                last_error = TranslationNotFound("empty translation")
            except (TranslationNotFound, TooManyRequests, RequestError) as e:
                last_error = e
            if attempt < max_attempts - 1:
                time.sleep(1.5)
        raise last_error if last_error else RuntimeError("googledeep failed")

    def __translate_with_mymemory(self, text: str) -> str:
        """Free secondary engine. Language coverage for yo/ig/ha is spotty, so
        this is wrapped defensively by the caller."""
        from deep_translator import MyMemoryTranslator
        src = self.__source_language_code
        tgt = self.__target_language_code
        # MyMemory wants full locale-ish codes; map the ones we use.
        _loc = {"en": "en-GB", "yo": "yo-NG", "ig": "ig-NG", "ha": "ha-NE"}
        translator = MyMemoryTranslator(
            source=_loc.get(src, src if src != "auto" else "en-GB"),
            target=_loc.get(tgt, tgt),
        )
        result = translator.translate(text)
        if not result or not result.strip():
            raise RuntimeError("mymemory returned empty")
        return result

    def __translate_with_claude(self, text: str) -> str:
        result = claude_translate(text, self.source_language, self.target_language)
        if not result:
            raise RuntimeError("claude translation unavailable")
        return result

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
        """Translate text using the specified method (raises on failure)."""
        translator = self.__translators.get(self.method, self.__translate_with_googledeep)
        return translator(text)


# ── Resilient orchestration ────────────────────────────────────────────────────

# Order matters:
#   1. googledeep — free, best quality when it works
#   2. claude     — high quality; used when Google's endpoint is down/flaky
#   3. mymemory   — free but weak for yo/ig/ha; last resort before giving up
# To make it strictly free-first, use ("googledeep", "mymemory", "claude").
_FALLBACK_CHAIN = ("googledeep", "claude", "mymemory")


def translate_with_fallback(text: str, source_language: str, target_language: str) -> dict:
    """
    Try every translation engine in turn until one works. Never raises.

    Returns a dict:
        {
          "text":   <translation> or None,
          "engine": "google" | "mymemory" | "claude" | None,
          "ok":     bool,
          "tried":  ["googledeep", ...],   # what we attempted, for logging
        }
    """
    text = (text or "").strip()
    if not text:
        return {"text": None, "engine": None, "ok": False, "tried": []}

    # No-op when the languages match — nothing to do, always "succeeds".
    if source_language and source_language == target_language:
        return {"text": text, "engine": "passthrough", "ok": True, "tried": []}

    _engine_label = {"googledeep": "google", "mymemory": "mymemory", "claude": "claude"}
    tried = []

    for method in _FALLBACK_CHAIN:
        if method == "claude" and not claude_available():
            continue
        tried.append(method)
        try:
            translator = LinguaFlowTranslate(
                source_language=source_language,
                target_language=target_language,
                method=method,
            )
            result = translator.translate(text)
            if result and result.strip():
                return {
                    "text": result.strip(),
                    "engine": _engine_label.get(method, method),
                    "ok": True,
                    "tried": tried,
                }
        except Exception as e:  # noqa: BLE001 — deliberately swallow, try next
            print(f"[translate] {method} failed: {e}")
            continue

    return {"text": None, "engine": None, "ok": False, "tried": tried}
