"""LinguaFlow Flask Web Application"""
from flask import Flask, render_template, request, jsonify
import os, base64, time
import speech_recognition as sr
import av, numpy as np, soundfile as sf
from utils.translate import LinguaFlowTranslate
from utils.speaker import LinguaFlowTTS
from utils.languages import get_language, SUPPORTED_LANGUAGES, get_language_code

# Resolve paths relative to this file so they work regardless of CWD
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder=os.path.join(SCRIPT_DIR, "templates"))
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
app.config["UPLOAD_FOLDER"] = os.path.join(SCRIPT_DIR, "temp_audio")
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


def webm_to_wav(input_path, output_path):
    """Convert WebM audio to WAV using PyAV."""
    container = None
    try:
        container = av.open(input_path)
        stream = container.streams.audio[0]
        resampler = av.audio.resampler.AudioResampler(format="s16", layout="mono", rate=16000)
        frames = []
        for packet in container.demux(stream):
            for frame in packet.decode():
                resampled_frames = resampler.resample(frame)
                if resampled_frames:
                    for rf in resampled_frames:
                        frames.append(rf.to_ndarray().flatten())
        if frames:
            sf.write(output_path, np.concatenate(frames).flatten(), 16000, subtype="PCM_16")
        else:
            raise Exception("No audio data found in file")
        return True
    except Exception as e:
        raise Exception(f"Audio conversion failed: {str(e)}")
    finally:
        if container is not None:
            container.close()


def get_tts_method(lang_code: str) -> str:
    """Route Yoruba to local MMS-TTS, Igbo to Colab YarnGPT, everything else to gTTS."""
    if lang_code == "yo":
        return "mms_tts"
    if lang_code == "ig":
        return "yarngpt_colab"
    return "gtts"

@app.route("/")
def index():
    languages = [lang for lang in SUPPORTED_LANGUAGES if lang != "multi"]
    return render_template("index.html", languages=languages)


@app.route("/process_audio", methods=["POST"])
def process_audio():
    try:
        if "audio" not in request.files:
            return jsonify({"error": "No audio file provided"}), 400

        audio_file = request.files["audio"]
        source_lang = request.form.get("source_language", "auto")
        target_lang = request.form.get("target_language", "english")

        if audio_file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], "temp_recording.webm")
        wav_filepath = os.path.join(app.config["UPLOAD_FOLDER"], "temp_recording.wav")
        audio_file.save(filepath)

        # ── Timing dictionary ─────────────────────────────────────────────
        timings = {}
        t_total_start = time.time()

        # ── Audio conversion ──────────────────────────────────────────────
        t0 = time.time()
        try:
            webm_to_wav(filepath, wav_filepath)
        except Exception as e:
            if os.path.exists(filepath):
                try: os.remove(filepath)
                except: pass
            return jsonify({"error": f"Audio conversion error: {str(e)}"}), 500
        timings["audio_conversion_ms"] = round((time.time() - t0) * 1000)

        time.sleep(0.1)
        try:
            if os.path.exists(filepath): os.remove(filepath)
        except Exception:
            pass

        # ── Speech recognition ────────────────────────────────────────────
        t1 = time.time()
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_filepath) as source:
            audio_data = recognizer.record(source)
            if source_lang == "auto":
                recognized_text, detected_lang = None, None
                for lang_name in SUPPORTED_LANGUAGES:
                    if lang_name == "multi":
                        continue
                    try:
                        recognized_text = recognizer.recognize_google(
                            audio_data, language=get_language_code(lang_name)
                        )
                        detected_lang = lang_name
                        break
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError as e:
                        return jsonify({"error": f"Recognition service error: {str(e)}"}), 500
                if not recognized_text:
                    return jsonify({"error": "Could not understand audio. Please speak more clearly."}), 400
                source_lang = detected_lang
            else:
                try:
                    recognized_text = recognizer.recognize_google(
                        audio_data, language=get_language_code(source_lang)
                    )
                except sr.UnknownValueError:
                    return jsonify({"error": "Could not understand audio. Please speak more clearly."}), 400
                except sr.RequestError as e:
                    return jsonify({"error": f"Recognition service error: {str(e)}"}), 500
        timings["speech_recognition_ms"] = round((time.time() - t1) * 1000)

        try:
            if os.path.exists(wav_filepath): os.remove(wav_filepath)
        except Exception:
            pass

        # ── Translation ───────────────────────────────────────────────────
        t2 = time.time()
        if source_lang == target_lang:
            translated_text = recognized_text
        else:
            translator = LinguaFlowTranslate(
                source_language=source_lang,
                target_language=target_lang,
                method="googledeep"
            )
            translated_text = translator.translate(recognized_text)
        timings["translation_ms"] = round((time.time() - t2) * 1000)

        # ── TTS generation ────────────────────────────────────────────────
        t3 = time.time()
        tts_method = get_tts_method(get_language_code(target_lang))
        tts = LinguaFlowTTS(language=target_lang, method=tts_method)
        audio_bytes, _ = tts.generate_audio_bytes(translated_text)
        timings["tts_generation_ms"] = round((time.time() - t3) * 1000)

        # ── Total ─────────────────────────────────────────────────────────
        timings["total_ms"] = round((time.time() - t_total_start) * 1000)
        timings["tts_engine"] = tts_method

        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

        # ── Log to console for recording ──────────────────────────────────
        print(f"\n{'='*50}")
        print(f"Source: {source_lang} → Target: {target_lang}")
        print(f"Recognized : {recognized_text}")
        print(f"Translated : {translated_text}")
        print(f"TTS Engine : {tts_method}")
        print(f"Timings    : {timings}")
        print(f"{'='*50}\n")

        return jsonify({
            "success": True,
            "recognized_text": recognized_text,
            "source_language": source_lang,
            "translated_text": translated_text,
            "target_language": target_lang,
            "audio": audio_base64,
            "timings": timings,
        })

    except Exception as e:
        for temp_file in ["temp_recording.webm", "temp_recording.wav", "output.mp3"]:
            temp_path = os.path.join(app.config["UPLOAD_FOLDER"], temp_file)
            if os.path.exists(temp_path):
                try: os.remove(temp_path)
                except: pass
        return jsonify({"error": f"Processing error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)