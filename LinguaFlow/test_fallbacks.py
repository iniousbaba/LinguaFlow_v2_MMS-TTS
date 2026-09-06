"""
Fallback-path tests for LinguaFlow's resilient translation + TTS.

Run:  python test_fallbacks.py
Exercises every branch of translate_with_fallback() and
synthesize_with_fallback(), including forced failures of each engine.
"""
import sys
from utils import translate as T
from utils import speaker as S
from utils.claude_client import claude_available

PASS, FAIL = "\033[92mPASS\033[0m", "\033[91mFAIL\033[0m"
results = []


def check(name, cond, detail=""):
    results.append(cond)
    print(f"  [{PASS if cond else FAIL}] {name}" + (f"  — {detail}" if detail else ""))


print(f"\nClaude available: {claude_available()}\n")

# ── Translation ───────────────────────────────────────────────────────────────
print("translate_with_fallback")

r = T.translate_with_fallback("Good morning, how are you?", "english", "yoruba")
check("english->yoruba via free engine", r["ok"] and bool(r["text"]),
      f"engine={r['engine']} text={r['text']!r}")

r = T.translate_with_fallback("kedu", "igbo", "igbo")
check("same-language passthrough", r["ok"] and r["engine"] == "passthrough")

r = T.translate_with_fallback("", "english", "hausa")
check("empty input -> not ok, no crash", (not r["ok"]) and r["text"] is None)

# Force every free engine to fail -> Claude must catch it (if key present).
_orig_google = T.LinguaFlowTranslate._LinguaFlowTranslate__translate_with_googledeep
_orig_mymem = T.LinguaFlowTranslate._LinguaFlowTranslate__translate_with_mymemory


def _boom(self, *a, **k):
    raise RuntimeError("simulated outage")


T.LinguaFlowTranslate._LinguaFlowTranslate__translate_with_googledeep = _boom
T.LinguaFlowTranslate._LinguaFlowTranslate__translate_with_mymemory = _boom
try:
    r = T.translate_with_fallback("The market is open today.", "english", "igbo")
    if claude_available():
        check("free engines down -> Claude fallback", r["ok"] and r["engine"] == "claude",
              f"engine={r['engine']} text={r['text']!r}")
    else:
        check("free engines down + no Claude -> clean no_translation",
              (not r["ok"]) and r["text"] is None and "claude" not in r["tried"])

    # Now also disable Claude -> total translation failure, still no crash.
    _orig_claude = T.LinguaFlowTranslate._LinguaFlowTranslate__translate_with_claude
    T.LinguaFlowTranslate._LinguaFlowTranslate__translate_with_claude = _boom
    T.claude_available = lambda: True  # force it to be attempted
    r = T.translate_with_fallback("Hello there.", "english", "yoruba")
    check("all engines down -> ok=False, text=None, no exception",
          (not r["ok"]) and r["text"] is None, f"tried={r['tried']}")
    T.LinguaFlowTranslate._LinguaFlowTranslate__translate_with_claude = _orig_claude
finally:
    T.LinguaFlowTranslate._LinguaFlowTranslate__translate_with_googledeep = _orig_google
    T.LinguaFlowTranslate._LinguaFlowTranslate__translate_with_mymemory = _orig_mymem

# ── TTS ───────────────────────────────────────────────────────────────────────
print("\nsynthesize_with_fallback")

try:
    import torch  # noqa: F401
    _has_torch = True
except Exception:
    _has_torch = False

r = S.synthesize_with_fallback("E kaaro", "yoruba")
if _has_torch:
    check("yoruba -> native MMS audio", r["ok"] and r["native"] and r["engine"] == "mms_tts",
          f"engine={r['engine']} bytes={len(r['audio'] or b'')}")
else:
    check("yoruba -> audio (no torch here; en-voice fallback expected)", r["ok"],
          f"engine={r['engine']} native={r['native']}  [install torch for native]")

r = S.synthesize_with_fallback("Hello world", "english")
check("english -> gtts audio", r["ok"] and r["native"] and r["engine"] == "gtts",
      f"bytes={len(r['audio'] or b'')}")

r = S.synthesize_with_fallback("Sannu da zuwa", "hausa")
check("hausa -> some audio (native or en fallback)", r["ok"],
      f"engine={r['engine']} native={r['native']}")

r = S.synthesize_with_fallback("Kedu ka i mere", "igbo")
check("igbo -> some audio (colab, gtts, or en fallback)", r["ok"],
      f"engine={r['engine']} native={r['native']}")

r = S.synthesize_with_fallback("", "yoruba")
check("empty text -> not ok, no crash", (not r["ok"]) and r["audio"] is None)

# Force MMS to fail -> yoruba must fall through to a gtts path.
_orig_mms = S._mms_tts
S._mms_tts = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("mms down"))
try:
    r = S.synthesize_with_fallback("E kaaro o", "yoruba")
    check("yoruba w/ MMS down -> gtts fallback still produces audio", r["ok"],
          f"engine={r['engine']} native={r['native']}")
finally:
    S._mms_tts = _orig_mms

# Force every gtts + colab + mms to fail -> total TTS failure, no crash.
_o1, _o2, _o3 = S._mms_tts, S._gtts_bytes, S._yarngpt_colab
S._mms_tts = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("x"))
S._gtts_bytes = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("x"))
S._yarngpt_colab = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("x"))
try:
    r = S.synthesize_with_fallback("anything", "igbo")
    check("all TTS engines down -> ok=False, audio=None, no exception",
          (not r["ok"]) and r["audio"] is None, f"tried={r['tried']}")
finally:
    S._mms_tts, S._gtts_bytes, S._yarngpt_colab = _o1, _o2, _o3

# ── Summary ──────────────────────────────────────────────────────────────────
total, ok = len(results), sum(results)
print(f"\n{ok}/{total} checks passed")
sys.exit(0 if ok == total else 1)
