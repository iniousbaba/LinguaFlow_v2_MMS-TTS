# LinguaFlow

A real-time multilingual speech translation system for English, Yoruba, Igbo, and Hausa. Built with Python/Flask.

## Project Structure

```
LinguaFlow-master/
├── app.py              # Flask web server — routes, audio processing
├── main.py             # CLI entry point — listen → translate → speak loop
├── utils/
│   ├── listener.py     # LinguaFlowSpeechRecognition — speech capture & recognition
│   ├── translate.py    # LinguaFlowTranslate — multiple translation backends
│   ├── speaker.py      # LinguaFlowTTS — gTTS text-to-speech
│   ├── languages.py    # LANGUAGE_CODES, SUPPORTED_LANGUAGES, helpers
│   └── decorators.py   # calc_execution_time decorator
├── templates/
│   └── index.html      # Web UI — recording, language selectors, results
├── requirements.txt
└── skills/             # Claude Code dev-workflow skills (see below)
```

## Core Flow

**Web:** browser records WebM → `/process_audio` → WebM→WAV (PyAV) → speech recognition (Google) → translation → gTTS MP3 → base64 JSON response

**CLI:** microphone → `LinguaFlowSpeechRecognition` → `LinguaFlowTranslate` → `LinguaFlowTTS` → playback

## Supported Languages

`en` (English), `yo` (Yoruba), `ig` (Igbo), `ha` (Hausa), `multi` (auto-detect)

## Running the App

```bash
# Web interface
python app.py

# CLI
python main.py
```

## Dev Notes

- Audio format: browsers send WebM; Google Speech API needs WAV — conversion via PyAV/FFmpeg
- Translation backends: `deep_translator` (primary), `googletrans` (fallback), `google-cloud-translate` (optional)
- Temp audio files go in `temp_audio/` — cleaned up after each request

---

## Skills

This project uses Claude Code dev-workflow skills from the [superpowers](https://github.com/obra/superpowers) library. Skills live in `skills/` and are invoked by Claude Code when the triggering conditions match.

**Available skills:**

| Skill | When it applies |
|-------|----------------|
| `brainstorming` | Before implementing a new feature — design first |
| `dispatching-parallel-agents` | 2+ independent tasks that can run concurrently |
| `executing-plans` | Following through on a written implementation plan |
| `finishing-a-development-branch` | Implementation complete — tests, merge, cleanup |
| `receiving-code-review` | Responding to code review feedback |
| `requesting-code-review` | Preparing work for review |
| `subagent-driven-development` | Executing plans with independent tasks in-session |
| `systematic-debugging` | Any bug, test failure, or unexpected behavior |
| `test-driven-development` | Any feature or bugfix implementation |
| `using-git-worktrees` | Starting feature work that needs workspace isolation |
| `using-superpowers` | Meta-skill — how to find and invoke the right skill |
| `verification-before-completion` | Before claiming any task is complete |
| `writing-plans` | Creating detailed implementation plans |
| `writing-skills` | Creating or editing skills |
| `code-quality-review` | After implementing a module — assess complexity, maintainability, test coverage, documentation |
| `feature-notes` | Starting any feature or bugfix — create a notes file for session continuity |
| `ui-ux-guidelines` | Designing or reviewing any part of the web UI — accessibility, touch targets, forms, responsive layout |
| `design-tokens` | Adding or changing any color, spacing, or typography in CSS — ensures CSS custom properties, no hardcoded values |
| `animation-polish` | Adding any animation, transition, or interactive feedback — recording button states, results appearing, loading, toasts |

Skills override default behavior. If there is even a 1% chance a skill applies to what you are doing, invoke it.
