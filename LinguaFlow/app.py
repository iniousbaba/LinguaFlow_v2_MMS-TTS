"""LinguaFlow Flask Web Application"""
from flask import Flask, render_template, request, jsonify
import os, base64, time, traceback
from werkzeug.exceptions import HTTPException
import speech_recognition as sr
import av, numpy as np, soundfile as sf
from utils.translate import translate_with_fallback
from utils.speaker import synthesize_with_fallback, preload_mms_models
from utils.claude_client import claude_available
from utils.languages import SUPPORTED_LANGUAGES, get_language_code

# Resolve paths relative to this file so they work regardless of CWD
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load a local .env (ANTHROPIC_API_KEY, etc.) if present — no hard dependency.
def _load_dotenv():
    path = os.path.join(SCRIPT_DIR, ".env")
    if not os.path.exists(path):
        return
    try:
        with open(path) as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, val = line.partition("=")
                key, val = key.strip(), val.strip().strip('"').strip("'")
                os.environ.setdefault(key, val)
    except Exception as e:  # noqa: BLE001
        print(f"[app] could not read .env: {e}")

_load_dotenv()

app = Flask(__name__, template_folder=os.path.join(SCRIPT_DIR, "templates"))
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
app.config["UPLOAD_FOLDER"] = os.path.join(SCRIPT_DIR, "temp_audio")
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Load MMS-TTS model(s) once at boot (non-fatal if it fails — retried lazily).
preload_mms_models()
print(f"[app] Claude fallback available: {claude_available()}")


# ── Notices shown to the user (blue = info, amber = degraded). Never red. ──────
# `no_audio` intentionally has no notice — the translation still shows, and the
# degraded-audio disclaimer already covers "audio may not be perfect".
NOTICE = {
    "degraded_audio": "Audio is using a fallback voice — pronunciation may be a little off.",
    "no_translation": "Translation service is unavailable right now. Please try again in a moment.",
    "no_speech": "Didn't quite catch that — please speak clearly and try again.",
    "speech_down": "The speech-recognition service is unavailable right now. Please try again shortly.",
    "unavailable": "Translation and audio are both unavailable right now. Please try again shortly.",
}


def webm_to_wav(input_path, output_path):
    """Convert WebM/any browser audio to 16 kHz mono WAV using PyAV."""
    container = None
    try:
        container = av.open(input_path)
        stream = container.streams.audio[0]
        resampler = av.audio.resampler.AudioResampler(format="s16", layout="mono", rate=16000)
        frames = []
        for packet in container.demux(stream):
            for frame in packet.decode():
                resampled = resampler.resample(frame)
                if resampled:
                    for rf in resampled:
                        frames.append(rf.to_ndarray().flatten())
        if not frames:
            raise Exception("No audio data found in file")
        sf.write(output_path, np.concatenate(frames).flatten(), 16000, subtype="PCM_16")
        return True
    except Exception as e:
        raise Exception(f"Audio conversion failed: {str(e)}")
    finally:
        if container is not None:
            container.close()


def _cleanup(*paths):
    for p in paths:
        try:
            if p and os.path.exists(p):
                os.remove(p)
        except Exception:
            pass


def _recognize(wav_path, source_lang):
    """Run Google speech recognition.

    Returns (text, resolved_source_lang, error_kind) where error_kind is one of
    None | "no_speech" | "service_down".
    """
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)

    if source_lang == "auto":
        for lang_name in SUPPORTED_LANGUAGES:
            if lang_name == "multi":
                continue
            try:
                text = recognizer.recognize_google(audio_data, language=get_language_code(lang_name))
                if text:
                    return text, lang_name, None
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                return None, source_lang, "service_down"
        return None, source_lang, "no_speech"

    try:
        text = recognizer.recognize_google(audio_data, language=get_language_code(source_lang))
        return text, source_lang, (None if text else "no_speech")
    except sr.UnknownValueError:
        return None, source_lang, "no_speech"
    except sr.RequestError:
        return None, source_lang, "service_down"


@app.errorhandler(413)
def _too_large(_e):
    return jsonify({
        "status": "no_speech", "success": False,
        "notice": "That recording was too large — keep it under ~30 seconds and try again.",
    }), 200


@app.errorhandler(Exception)
def _catch_all(e):
    # Let normal HTTP errors (404, 405, the 413 handler above, ...) behave.
    if isinstance(e, HTTPException):
        return e
    # Last line of defence: the UI must never receive a raw 500 HTML page.
    print(f"[app] unhandled: {e}\n{traceback.format_exc()}")
    return jsonify({
        "status": "unavailable", "success": False,
        "notice": NOTICE["unavailable"],
    }), 200


@app.route("/")
def index():
    languages = [lang for lang in SUPPORTED_LANGUAGES if lang != "multi"]
    return render_template("index.html", languages=languages)


@app.route("/healthz")
def healthz():
    return jsonify({"ok": True, "claude": claude_available()})


@app.route("/process_audio", methods=["POST"])
def process_audio():
    """
    Always responds 200 with a JSON body. The frontend reads `status`:

        ok             — translation + native audio
        degraded_audio — translation + fallback (English-voice) audio
        no_audio       — translation only, no audio available
        no_translation — could not translate (speech was recognised though)
        no_speech      — couldn't understand the recording (user should retry)
        speech_down    — Google speech recognition is down
        unavailable    — nothing worked / unexpected error
    """
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], "temp_recording.webm")
    wav_filepath = os.path.join(app.config["UPLOAD_FOLDER"], "temp_recording.wav")

    def respond(status, **extra):
        body = {
            "status": status,
            "success": status in ("ok", "degraded_audio", "no_audio"),
            "notice": NOTICE.get(status),
            "recognized_text": None,
            "source_language": None,
            "translated_text": None,
            "target_language": extra.get("target_language"),
            "translation_engine": None,
            "audio": None,
            "audio_mime": None,
            "tts_engine": None,
            "timings": {},
        }
        body.update(extra)
        return jsonify(body), 200

    try:
        if "audio" not in request.files or request.files["audio"].filename == "":
            return respond("no_speech")

        source_lang = request.form.get("source_language", "auto") or "auto"
        target_lang = request.form.get("target_language", "english") or "english"
        request.files["audio"].save(filepath)

        timings = {}
        t_total = time.time()

        # ── Audio conversion ─────────────────────────────────────────────
        t0 = time.time()
        try:
            webm_to_wav(filepath, wav_filepath)
        except Exception as e:
            print(f"[app] audio conversion failed: {e}")
            _cleanup(filepath, wav_filepath)
            return respond("no_speech", target_language=target_lang)
        timings["audio_conversion_ms"] = round((time.time() - t0) * 1000)
        _cleanup(filepath)

        # ── Speech recognition ───────────────────────────────────────────
        t1 = time.time()
        recognized_text, source_lang, rec_err = _recognize(wav_filepath, source_lang)
        timings["speech_recognition_ms"] = round((time.time() - t1) * 1000)
        _cleanup(wav_filepath)

        if rec_err == "service_down":
            return respond("speech_down", target_language=target_lang, timings=timings)
        if rec_err == "no_speech" or not recognized_text:
            return respond("no_speech", target_language=target_lang, timings=timings)

        # ── Translation (with fallbacks) ─────────────────────────────────
        t2 = time.time()
        tr = translate_with_fallback(recognized_text, source_lang, target_lang)
        timings["translation_ms"] = round((time.time() - t2) * 1000)
        translated_text = tr["text"]
        translation_engine = tr["engine"]

        common = dict(
            recognized_text=recognized_text,
            source_language=source_lang,
            target_language=target_lang,
            translated_text=translated_text,
            translation_engine=translation_engine,
        )

        if not tr["ok"] or not translated_text:
            timings["total_ms"] = round((time.time() - t_total) * 1000)
            print(f"[app] NO TRANSLATION  {source_lang}->{target_lang}  tried={tr['tried']}")
            return respond("no_translation", timings=timings, **common)

        # ── TTS (with fallbacks) ────────────────────────────────────────
        t3 = time.time()
        sp = synthesize_with_fallback(translated_text, target_lang)
        timings["tts_generation_ms"] = round((time.time() - t3) * 1000)
        timings["total_ms"] = round((time.time() - t_total) * 1000)
        timings["tts_engine"] = sp["engine"]
        timings["translation_engine"] = translation_engine

        audio_b64 = base64.b64encode(sp["audio"]).decode("utf-8") if sp["ok"] else None

        if sp["ok"] and sp["native"]:
            status = "ok"
        elif sp["ok"]:
            status = "degraded_audio"
        else:
            status = "no_audio"

        print(
            f"\n{'='*50}\n{source_lang} -> {target_lang}\n"
            f"Recognized : {recognized_text}\n"
            f"Translated : {translated_text}  [{translation_engine}]\n"
            f"TTS        : {sp['engine']}  native={sp['native']}  ok={sp['ok']}\n"
            f"Status     : {status}\nTimings    : {timings}\n{'='*50}\n"
        )

        return respond(
            status,
            audio=audio_b64,
            audio_mime=sp["mime"],
            tts_engine=sp["engine"],
            timings=timings,
            **common,
        )

    except Exception as e:  # noqa: BLE001 — never leak a 500 to the UI
        print(f"[app] UNEXPECTED: {e}\n{traceback.format_exc()}")
        _cleanup(filepath, wav_filepath)
        return respond("unavailable")


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
