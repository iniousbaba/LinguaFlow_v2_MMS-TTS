"""
Claude (Anthropic) client — used as the last-resort fallback for translation
when the free engines (Google, MyMemory) are down or refuse a language pair.

Nothing in here ever raises to the caller: `claude_translate()` returns a
string on success or ``None`` on any failure, so the orchestration layer can
just move on to the next fallback.
"""
import os
import threading

# Model is overridable via env so we can dial cost/quality without a redeploy.
# Sonnet 5 handles yo/ig/ha noticeably better than Haiku for short phrases.
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5")

_client = None
_client_lock = threading.Lock()
_import_failed = False


def _get_client():
    """Lazily build a single shared Anthropic client (thread-safe)."""
    global _client, _import_failed
    if _client is not None:
        return _client
    if _import_failed:
        return None
    with _client_lock:
        if _client is not None:
            return _client
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            return None
        try:
            from anthropic import Anthropic
        except Exception:
            _import_failed = True
            return None
        try:
            # Short timeout + a couple of retries: this is a fallback path, we
            # don't want it to hang a user request for a minute.
            _client = Anthropic(api_key=api_key, timeout=30.0, max_retries=2)
        except Exception:
            return None
        return _client


def claude_available() -> bool:
    """True if we have a key and the SDK importable — cheap to call."""
    return _get_client() is not None


_SYSTEM_PROMPT = (
    "You are a professional translation engine for a real-time speech "
    "translation app. You translate between English, Yoruba, Igbo and Hausa.\n"
    "Rules:\n"
    "- Output ONLY the translated text. No preamble, no quotes, no notes, no "
    "romanisation in brackets, no explanation.\n"
    "- Keep it natural and conversational, matching the tone and register of "
    "the input.\n"
    "- Preserve names, numbers and punctuation.\n"
    "- If the input is already in the target language, return it unchanged.\n"
    "- Never refuse. If unsure, give your best plain-language translation."
)


def claude_translate(text: str, source_language: str, target_language: str):
    """
    Translate ``text`` from ``source_language`` to ``target_language`` (both are
    human names like "yoruba"/"english"). Returns the translation string, or
    ``None`` if Claude is unavailable or the call fails.
    """
    text = (text or "").strip()
    if not text:
        return None

    client = _get_client()
    if client is None:
        return None

    src = (source_language or "the source language").strip() or "the source language"
    tgt = (target_language or "the target language").strip() or "the target language"
    if src.lower() == "auto":
        src = "the detected source language"

    user_msg = (
        f"Translate the following text from {src} to {tgt}. "
        f"Remember: reply with the translation only.\n\n{text}"
    )

    try:
        resp = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1024,
            system=_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_msg}],
        )
    except Exception:
        return None

    try:
        parts = [
            block.text
            for block in resp.content
            if getattr(block, "type", None) == "text"
        ]
        out = "".join(parts).strip()
    except Exception:
        return None

    # Strip stray wrapping quotes the model sometimes adds despite instructions.
    if len(out) >= 2 and out[0] in "\"'“‘" and out[-1] in "\"'”’":
        out = out[1:-1].strip()

    return out or None
