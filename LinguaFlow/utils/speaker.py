import io, os, base64
import requests as http_requests
import sounddevice as sd
import soundfile as sf
import tempfile
from os import remove
from utils.languages import get_language_code

# ── Paste your ngrok URL here each time you start Colab ──────────────────────
YARNGPT_COLAB_URL = "https://secluded-joyride-wispy.ngrok-free.dev"

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
    """Call the Colab YarnGPT API and return WAV bytes."""
    lang_str = _LANG_STRING.get(lang_code, "yoruba")
    speaker  = VOICE_MAP.get(lang_code, "yoruba_female1")
    try:
        resp = http_requests.post(
            f"{YARNGPT_COLAB_URL}/tts",
            json={"text": text, "language": lang_str, "speaker": speaker},
            timeout=300,  # generation can take up to 60s on CPU Colab
        )
        data = resp.json()
        if data.get("success"):
            return base64.b64decode(data["audio"])
        else:
            raise Exception(f"Colab API error: {data.get('error')}")
    except Exception as e:
        raise Exception(f"YarnGPT Colab unreachable: {str(e)}")


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
        from gtts import gTTS
        buf = io.BytesIO()
        tts = gTTS(text=text, lang=self.__lang_code)
        tts.write_to_fp(buf)
        return buf.getvalue()

    def generate_audio_bytes(self, text: str) -> tuple:
        if self.__method == "yarngpt_colab":
            audio_bytes = _yarngpt_colab(text, self.__lang_code)
            return audio_bytes, "audio/wav"
        elif self.__method == "mms_tts":
            audio_bytes = _mms_tts(text, self.__lang_code)
            return audio_bytes, "audio/wav"
        else:
            audio_bytes = self.__tts_gtts(text)
            return audio_bytes, "audio/mpeg"

    def speak(self, text: str) -> None:
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