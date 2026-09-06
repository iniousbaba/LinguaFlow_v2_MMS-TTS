"""
Endpoint-level tests for /process_audio using Flask's test client.
Monkeypatches recognition / translation / TTS to force every status branch
and asserts the response is ALWAYS HTTP 200 with a sane JSON shape.

Run:  python test_endpoint.py
"""
import io, sys, wave, struct
import app as appmod

PASS, FAIL = "\033[92mPASS\033[0m", "\033[91mFAIL\033[0m"
results = []
client = appmod.app.test_client()


def _wav_bytes(seconds=1, freq=220, rate=16000):
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
        for i in range(int(rate * seconds)):
            w.writeframes(struct.pack("<h", int(3000 * (i % (rate // freq) < (rate // freq) / 2) - 1500)))
    return buf.getvalue()


WAV = _wav_bytes()


def post(**form):
    data = {"audio": (io.BytesIO(WAV), "r.wav")}
    data.update(form)
    return client.post("/process_audio", data=data, content_type="multipart/form-data")


def check(name, cond, detail=""):
    results.append(bool(cond))
    print(f"  [{PASS if cond else FAIL}] {name}" + (f"  — {detail}" if detail else ""))


# ── 1. no audio at all ──────────────────────────────────────────────
r = client.post("/process_audio", data={}, content_type="multipart/form-data")
j = r.get_json()
check("no file -> 200 + no_speech", r.status_code == 200 and j["status"] == "no_speech", str(j.get("notice")))

# ── 2. recognition says "service down" ──────────────────────────────
orig_rec = appmod._recognize
appmod._recognize = lambda *a, **k: (None, "auto", "service_down")
r = post(source_language="auto", target_language="english")
j = r.get_json()
check("speech service down -> 200 + speech_down",
      r.status_code == 200 and j["status"] == "speech_down" and j["notice"], str(j.get("notice")))
appmod._recognize = orig_rec

# ── 3. recognition ok, translation totally fails ────────────────────
appmod._recognize = lambda *a, **k: ("hello there", "english", None)
orig_tr = appmod.translate_with_fallback
appmod.translate_with_fallback = lambda *a, **k: {"text": None, "engine": None, "ok": False, "tried": ["googledeep", "claude", "mymemory"]}
r = post(source_language="english", target_language="yoruba")
j = r.get_json()
check("translation down -> 200 + no_translation, recognised text still returned",
      r.status_code == 200 and j["status"] == "no_translation"
      and j["recognized_text"] == "hello there" and j["translated_text"] is None,
      str(j.get("notice")))
check("no_translation -> success flag is False", j["success"] is False)
appmod.translate_with_fallback = orig_tr

# ── 4. translation ok, all TTS fails -> no_audio ───────────────────
appmod.translate_with_fallback = lambda *a, **k: {"text": "bawo ni", "engine": "claude", "ok": True, "tried": []}
orig_sp = appmod.synthesize_with_fallback
appmod.synthesize_with_fallback = lambda *a, **k: {"audio": None, "mime": None, "engine": None, "ok": False, "native": False, "tried": []}
r = post(source_language="english", target_language="yoruba")
j = r.get_json()
check("TTS down -> 200 + no_audio, translation still returned",
      r.status_code == 200 and j["status"] == "no_audio"
      and j["translated_text"] == "bawo ni" and j["audio"] is None, str(j.get("notice")))
check("no_audio -> success flag is True (still useful)", j["success"] is True)

# ── 5. translation ok, only English-voice fallback -> degraded_audio ─
appmod.synthesize_with_fallback = lambda *a, **k: {"audio": b"RIFFxxxx", "mime": "audio/mpeg", "engine": "gtts_en_fallback", "ok": True, "native": False, "tried": []}
r = post(source_language="english", target_language="igbo")
j = r.get_json()
check("fallback voice -> 200 + degraded_audio + notice + audio present",
      r.status_code == 200 and j["status"] == "degraded_audio" and j["audio"] and j["notice"],
      str(j.get("notice")))

# ── 6. full happy path ────────────────────────────────────────────
appmod.synthesize_with_fallback = lambda *a, **k: {"audio": b"RIFFxxxx", "mime": "audio/wav", "engine": "mms_tts", "ok": True, "native": True, "tried": []}
r = post(source_language="english", target_language="yoruba")
j = r.get_json()
check("happy path -> 200 + ok + no notice + audio", r.status_code == 200 and j["status"] == "ok" and j["notice"] is None and j["audio"])

# ── 7. unexpected exception in the middle -> unavailable, still 200 ──
appmod.synthesize_with_fallback = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("kaboom"))
r = post(source_language="english", target_language="yoruba")
j = r.get_json()
check("mid-pipeline crash -> 200 + unavailable (no 500)", r.status_code == 200 and j["status"] == "unavailable", str(j.get("notice")))

appmod._recognize = orig_rec
appmod.translate_with_fallback = orig_tr
appmod.synthesize_with_fallback = orig_sp

# ── 8. GET / still renders, and has no red error box ───────────────
r = client.get("/")
html = r.get_data(as_text=True)
check("index renders", r.status_code == 200 and "LinguaFlow" in html)
check("no red .error-message class in template", "error-message" not in html)
check("toast component present", "toast-wrap" in html and "showToast" in html)

total, ok = len(results), sum(results)
print(f"\n{ok}/{total} checks passed")
sys.exit(0 if ok == total else 1)
