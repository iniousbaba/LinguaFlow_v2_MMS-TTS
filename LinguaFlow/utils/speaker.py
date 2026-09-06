import io, os, base64
import requests as http_requests
import soundfile as sf
import tempfile
from os import remove
from utils.languages import get_language_code

# ── Colab YarnGPT endpoint (Igbo voice). Overridable without a code edit. ─────
YARNGPT_COLAB_URL = os.environ.get(
    "YARNGPT_COLAB_URL",
    "https://secluded-joyride-wispy.ngrok-free.dev",
)

# ── Language code → YarnGPT lang string ─────────────────────────────────────
_LANG_STRING = {
    "yo": "yoruba",
    "ig": "igbo",
}

# ── Voice map ────────────────────────────────────────────────────────────────
VOICE_MAP = {
    "yo": "yoruba_female1",
    "ig": "igbo_female1",
}

# ── MMS-TTS language code mapping (only Yoruba has a checkpoint) ────────────
_MMS_LANG_MAP = {
    "yo": "yor",
}

_MMS_MODEL_CACHE = {}

# Reuse one HTTP connection pool for the Colab calls.
_session = http_requests.Session()

# gTTS's supported-language set, computed once (falls back to a static guess).
_GTTS_LANGS = None


def _gtts_supported(lang_code: str) -> bool:
    global _GTTS_LANGS
    if _GTTS_LANGS is None:
        try:
            from gtts.lang import tts_langs
            _GTTS_LANGS = set(tts_langs().keys())
        except Exception:
            _GTTS_LANGS = {"en", "yo", "ha", "fr", "es", "de", "sw"}
    return lang_code in _GTTS_LANGS


def _get_mms_model(lang_code: str):
    """Load and cache the MMS-TTS VITS model + tokenizer for a language.
    Cached so the model only loads once per app run, not once per request."""
    if lang_code not in _MMS_MODEL_CACHE:
        from transformers import VitsModel, AutoTokenizer
        mms_code = _MMS_LANG_MAP.get(lang_code)
        if mms_code is None:
            raise Exception(f"No MMS-TTS checkpoint available for language code '{lang_code}'")
        model = VitsModel.from_pretrained(f"facebook/mms-tts-{mms_code}")
        tokenizer = AutoTokenizer.from_pretrained(f"facebook/mms-tts-{mms_code}")
        model.eval()
        _MMS_MODEL_CACHE[lang_code] = (model, tokenizer)
    return _MMS_MODEL_CACHE[lang_code]


def preload_mms_models():
    """Load all MMS-TTS checkpoints once at process startup, so the slow
    first-time download/load happens during boot instead of blocking a
    live user request. Non-fatal: if HF is unreachable at boot, we log and
    carry on — `_get_mms_model` will retry lazily on the first request."""
    for lang_code in _MMS_LANG_MAP:
        try:
            _get_mms_model(lang_code)
        except Exception as e:  # noqa: BLE001
            print(f"[speaker] preload of MMS '{lang_code}' failed (will retry lazily): {e}")


def _mms_tts(text: str, lang_code: str) -> bytes:
    """Synthesize speech locally using Facebook MMS-TTS. Returns WAV bytes."""
    import torch
    model, tokenizer = _get_mms_model(lang_code)
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        output = model(**inputs).waveform
    buf = io.BytesIO()
    sf.write(buf, output.squeeze().numpy(), model.config.sampling_rate, format="WAV")
    return buf.getvalue()


def _yarngpt_colab(text: str, lang_code: str) -> bytes:
    """Call the Colab YarnGPT API and return WAV bytes.

    Uses a short *connect* timeout so a dead tunnel fails fast (~8s) instead of
    hanging, but a long *read* timeout because generation is slow on CPU Colab.
    """
    lang_str = _LANG_STRING.get(lang_code, "yoruba")
    speaker  = VOICE_MAP.get(lang_code, "yoruba_female1")
    try:
        resp = _session.post(
            f"{YARNGPT_COLAB_URL}/tts",
            json={"text": text, "language": lang_str, "speaker": speaker},
            timeout=(8, 180),  # (connect, read)
            headers={"ngrok-skip-browser-warning": "1"},
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("success") and data.get("audio"):
            return base64.b64decode(data["audio"])
        raise Exception(f"Colab API error: {data.get('error', 'no audio in response')}")
    except Exception as e:
        raise Exception(f"YarnGPT Colab unreachable: {str(e)}")


def _gtts_bytes(text: str, lang_code: str) -> bytes:
    """gTTS MP3 bytes for ``lang_code``. Raises if gTTS rejects the language."""
    from gtts import gTTS
    buf = io.BytesIO()
    gTTS(text=text, lang=lang_code).write_to_fp(buf)
    out = buf.getvalue()
    if not out:
        raise RuntimeError("gTTS produced no audio")
    return out


class LinguaFlowTTS:

    def __init__(self, language: str = "", method: str = "gtts") -> None:
        self.__language  = language
        self.__lang_code = get_language_code(language)
        self.__method    = method

    def __repr__(self):
        return f"LinguaFlowTTS(language={self.__language}, method={self.__method})"

    def __call__(self, text: str):
        return self.speak(text)

    def __tts_gtts(self, text: str) -> bytes:
        return _gtts_bytes(text, self.__lang_code)

    def generate_audio_bytes(self, text: str) -> tuple:
        if self.__method == "yarngpt_colab":
            return _yarngpt_colab(text, self.__lang_code), "audio/wav"
        elif self.__method == "mms_tts":
            return _mms_tts(text, self.__lang_code), "audio/wav"
        else:
            return self.__tts_gtts(text), "audio/mpeg"

    def speak(self, text: str) -> None:
        import sounddevice as sd

        audio_bytes, _ = self.generate_audio_bytes(text)
        suffix = ".wav" if self.__method in ("yarngpt_colab", "mms_tts") else ".mp3"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name
        try:
            data, samplerate = sf.read(tmp_path)
            sd.play(data, samplerate)
            sd.wait()
        finally:
            remove(tmp_path)


# ── Resilient orchestration ────────────────────────────────────────────────────

def synthesize_with_fallback(text: str, target_language: str) -> dict:
    """
    Produce speech audio for ``text`` in ``target_language`` (a human name like
    "yoruba"). Walks a per-language chain of engines until one works. Never
    raises.

    Returns:
        {
          "audio":    <bytes> or None,
          "mime":     "audio/wav" | "audio/mpeg" | None,
          "engine":   "mms_tts" | "yarngpt_colab" | "gtts" | "gtts_en_fallback" | None,
          "ok":       bool,      # any audio at all?
          "native":   bool,      # was it a real voice for this language?
          "tried":    [...],
        }

    "native" is False when we had to read the text with an English voice — the
    caller should tell the user pronunciation may be off.
    """
    text = (text or "").strip()
    lang_code = get_language_code(target_language) or "en"
    tried = []

    def _fail():
        return {"audio": None, "mime": None, "engine": None,
                "ok": False, "native": False, "tried": tried}

    if not text:
        return _fail()

    # Build the ordered plan of (engine_name, callable, mime, native?) per language.
    plan = []
    if lang_code == "yo":
        plan.append(("mms_tts", lambda: _mms_tts(text, "yo"), "audio/wav", True))
        if _gtts_supported("yo"):
            plan.append(("gtts", lambda: _gtts_bytes(text, "yo"), "audio/mpeg", True))
    elif lang_code == "ig":
        plan.append(("yarngpt_colab", lambda: _yarngpt_colab(text, "ig"), "audio/wav", True))
        if _gtts_supported("ig"):
            plan.append(("gtts", lambda: _gtts_bytes(text, "ig"), "audio/mpeg", True))
    elif lang_code == "ha":
        if _gtts_supported("ha"):
            plan.append(("gtts", lambda: _gtts_bytes(text, "ha"), "audio/mpeg", True))
    else:  # english / anything else
        plan.append(("gtts", lambda: _gtts_bytes(text, "en"), "audio/mpeg", True))

    # Universal last resort: read the text aloud with the English voice.
    if lang_code != "en":
        plan.append(("gtts_en_fallback", lambda: _gtts_bytes(text, "en"), "audio/mpeg", False))

    for engine, fn, mime, native in plan:
        tried.append(engine)
        try:
            audio = fn()
            if audio:
                return {"audio": audio, "mime": mime, "engine": engine,
                        "ok": True, "native": native, "tried": tried}
        except Exception as e:  # noqa: BLE001 — try the next engine
            print(f"[speaker] {engine} failed: {e}")
            continue

    return _fail()
