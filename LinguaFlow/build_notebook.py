"""
Build LinguaFlow_Colab.ipynb from the actual source files.
Run this script once to regenerate the notebook cleanly.
"""
import json, os, base64

BASE = os.path.dirname(os.path.abspath(__file__))

def read(rel_path):
    with open(os.path.join(BASE, rel_path), "r", encoding="utf-8") as f:
        return f.read()

def code_cell(source_str):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source_str,
    }

def md_cell(source_str):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source_str,
    }

def embed_file(rel_path, content):
    """Return Python statements that write content to rel_path inside /content/LinguaFlow_app/."""
    # Use base64 to avoid any escaping issues with file content
    b64 = base64.b64encode(content.encode("utf-8")).decode("ascii")
    lines = []
    lines.append(f"# --- {rel_path} ---\n")
    lines.append(f"_b64 = '{b64}'\n")
    lines.append(f"_path = os.path.join(APP_DIR, '{rel_path.replace(os.sep, '/')}')\n")
    lines.append("os.makedirs(os.path.dirname(_path) if os.path.dirname(_path) else APP_DIR, exist_ok=True)\n")
    lines.append("with open(_path, 'w', encoding='utf-8') as _f:\n")
    lines.append("    _f.write(base64.b64decode(_b64).decode('utf-8'))\n")
    lines.append(f"print('  Written: {rel_path}')\n")
    return lines


# ─── Cell 1: Markdown header ───────────────────────────────────────────────────
cell1 = md_cell(
    "# LinguaFlow - Google Colab\n"
    "Real-time multilingual speech translation: English, Yoruba, Igbo, Hausa.\n\n"
    "**Run all cells in order** (Runtime > Run all). "
    "A public ngrok URL will appear after Cell 3 — click it to open the app."
)

# ─── Cell 2: Install dependencies ──────────────────────────────────────────────
cell2_src = (
    "# Cell 1 - Install Dependencies\n"
    "import subprocess, sys\n\n"
    "packages = [\n"
    "    'flask',\n"
    "    'pyngrok',\n"
    "    'SpeechRecognition',\n"
    "    'deep-translator',\n"
    "    'gTTS',\n"
    "    'av',\n"
    "    'soundfile',\n"
    "    'numpy',\n"
    "]\n\n"
    "print('Installing packages...')\n"
    "subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q'] + packages)\n"
    "print('All packages installed.')\n"
)
cell2 = code_cell(cell2_src)

# ─── Cell 3: Write source files inline ─────────────────────────────────────────
files = {
    "utils/__init__.py":  "",
    "utils/languages.py": read("utils/languages.py"),
    "utils/decorators.py": read("utils/decorators.py"),
    "utils/translate.py": read("utils/translate.py"),
    "utils/listener.py":  read("utils/listener.py"),
    "utils/speaker.py":   read("utils/speaker.py"),
    "app.py":             read("app.py"),
    "templates/index.html": read("templates/index.html"),
}

cell3_lines = [
    "# Cell 2 - Write Source Files\n",
    "import os, base64\n",
    "\n",
    "APP_DIR = '/content/LinguaFlow_app'\n",
    "os.makedirs(APP_DIR, exist_ok=True)\n",
    "\n",
    "print('Writing source files...')\n",
]
for rel_path, content in files.items():
    cell3_lines.extend(embed_file(rel_path, content))
    cell3_lines.append("\n")

cell3_lines.extend([
    "os.makedirs(os.path.join(APP_DIR, 'temp_audio'), exist_ok=True)\n",
    "print('Done. App directory:', APP_DIR)\n",
])
cell3 = code_cell("".join(cell3_lines))

# ─── Cell 4: Launch Flask + ngrok ──────────────────────────────────────────────
cell4_src = (
    "# Cell 3 - Launch Flask + ngrok\n"
    "import subprocess, sys, time, threading\n"
    "from pyngrok import ngrok, conf\n\n"
    "NGROK_AUTH_TOKEN = 'YOUR_NGROK_TOKEN_HERE'\n"
    "APP_DIR = '/content/LinguaFlow_app'\n\n"
    "conf.get_default().auth_token = NGROK_AUTH_TOKEN\n\n"
    "flask_proc = subprocess.Popen(\n"
    "    [sys.executable, 'app.py'],\n"
    "    cwd=APP_DIR,\n"
    "    stdout=subprocess.PIPE,\n"
    "    stderr=subprocess.STDOUT,\n"
    "    bufsize=0,\n"
    ")\n\n"
    "time.sleep(3)\n\n"
    "tunnel = ngrok.connect(5000)\n"
    "print('LinguaFlow is live at:', tunnel.public_url)\n\n"
    "# Stream Flask logs (runs until interrupted)\n"
    "print('--- Flask logs (Ctrl+C or interrupt kernel to stop) ---')\n"
    "try:\n"
    "    for raw_line in iter(flask_proc.stdout.readline, b''):\n"
    "        print(raw_line.decode('utf-8', errors='replace').rstrip())\n"
    "except KeyboardInterrupt:\n"
    "    pass\n"
    "finally:\n"
    "    print('--- Log stream stopped ---')\n"
)
cell4 = code_cell(cell4_src)

# ─── Cell 5: Stop server ────────────────────────────────────────────────────────
cell5_src = (
    "# Cell 4 - Stop Server (run this to shut down)\n"
    "from pyngrok import ngrok as _ngrok\n"
    "import signal, os\n\n"
    "try:\n"
    "    _ngrok.kill()\n"
    "    print('ngrok stopped.')\n"
    "except Exception as e:\n"
    "    print('ngrok already stopped:', e)\n\n"
    "try:\n"
    "    flask_proc.terminate()\n"
    "    flask_proc.wait(timeout=5)\n"
    "    print('Flask server stopped.')\n"
    "except Exception as e:\n"
    "    print('Flask already stopped:', e)\n"
)
cell5 = code_cell(cell5_src)

# ─── Assemble notebook ─────────────────────────────────────────────────────────
notebook = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
            "version": "3.10.0",
        },
        "colab": {
            "provenance": [],
            "name": "LinguaFlow_Colab.ipynb",
        },
    },
    "cells": [cell1, cell2, cell3, cell4, cell5],
}

out_path = os.path.join(BASE, "LinguaFlow_Colab.ipynb")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print(f"Notebook written to: {out_path}")
