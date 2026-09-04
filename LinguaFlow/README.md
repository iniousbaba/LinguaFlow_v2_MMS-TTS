# LinguaFlow

A real-time speech translation system that enables seamless multilingual conversations by converting speech input from one language to another and playing the translated output.

## Overview

LinguaFlow captures speech in multiple languages, translates it to a target language, and outputs the translation as synthesized speech. The system is designed to facilitate natural conversation flow between speakers of different languages.

## Features

- **Multi-language Speech Recognition**: Automatically detects and recognizes speech in English, Yoruba, Igbo, and Hausa
- **Real-time Translation**: Translates recognized speech to target language using multiple translation engines
- **Text-to-Speech Output**: Converts translated text to natural-sounding speech
- **Modular Architecture**: Clean separation of codes for easy maintenance and extension
- **Multiple Translation Methods**: Support for Google Translate (via googletrans, deep_translator, and Google Cloud API)
- **Performance Monitoring**: Built-in execution time tracking for optimization

## Supported Languages

- English
- Yoruba
- Igbo
- Hausa

## Project Structure
```
LinguaFlow/
├── utils/
│   ├── __init__.py
│   ├── decorators.py      # Utility decorators (execution time tracking)
│   ├── languages.py       # Language code management and validation
│   ├── listener.py        # Speech recognition module
│   ├── speaker.py         # Text-to-speech module
│   └── translate.py       # Translation module
├── main.py                # Application entry point
└── requirements.txt       # Project dependencies
```

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Git installed on your system
- Microphone for speech input
- Speaker/headphones for audio output

### Setup Instructions

1. **Clone the Repository**
```bash
git clone https://github.com/YOUR_USERNAME/LinguaFlow.git
cd LinguaFlow
```

2. **Create a Virtual Environment** (Recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

**Note**: On Linux, you may need to install additional system dependencies:
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
```

4. **Verify Installation**

Test that all modules import correctly:
```bash
python -c "from utils.listener import LinguaFlowSpeechRecognition; print('Setup successful!')"
```

5. **Run the Application**
```bash
python main.py
```

## Usage

### Basic Usage

Run the main application:
```bash
python main.py
```

The system will:
1. Listen for speech input via your microphone
2. Automatically detect the language spoken
3. Translate to the configured target language(in this case Hausa)
4. Play the translated speech through your speakers

### Customizing Languages

Edit `main.py` to configure source and target languages:
```python
# Configure speech recognition language
linguaflow_recognizer = LinguaFlowSpeechRecognition(language="multi")  # or "english", "yoruba", "igbo", "hausa"

# Configure output language
linguaflow_tts = LinguaFlowTTS(language="hausa")  # Target language for translation
```

### Translation Methods

LinguaFlow supports multiple translation backends:
```python
linguaflow_translator = LinguaFlowTranslate(
    source_language="english",
    target_language="yoruba",
    method="googledeep"  # Options: "googledeep", "googletrans", "googlecloud"
)
```

**Available Methods:**
- `googledeep` (default): Uses deep_translator with GoogleTranslator
- `googletrans`: Uses the googletrans library
- `googlecloud`: Uses Google Cloud Translation API (requires API credentials)

## Module Documentation

### LinguaFlowSpeechRecognition (listener.py)

**Purpose**: Captures audio from the microphone and converts it to text using speech recognition.

**Class Definition:**
```python
class LinguaFlowSpeechRecognition:
    def __init__(self, language="multi", method="google") -> None:
        """
        Initialize speech recognition.
        
        Args:
            language (str): Recognition language ("multi", "english", "yoruba", "igbo", "hausa")
            method (str): Recognition method (currently supports "google")
        """
```

**Key Methods:**
- `recognize_speech()`: Captures audio and returns tuple of (language_code, recognized_text)

**Usage Examples:**
```python
from utils.listener import LinguaFlowSpeechRecognition

# Example 1: Multi-language recognition (auto-detect)
recognizer = LinguaFlowSpeechRecognition(language="multi", method="google")
language_code, text = recognizer.recognize_speech()
print(f"Detected Language: {language_code}")
print(f"Recognized Text: {text}")

# Example 2: Single language recognition
recognizer = LinguaFlowSpeechRecognition(language="yoruba")
language_code, text = recognizer.recognize_speech()

# Example 3: Using the class as a callable
recognizer = LinguaFlowSpeechRecognition(language="english")
language_code, text = recognizer()  # Calls recognize_speech() automatically
```

**Return Values:**
- Returns `("en", "Hello world")` for English
- Returns `("yo", "Bawo ni")` for Yoruba
- Returns `("", "")` if no speech detected

---

### LinguaFlowTranslate (translate.py)

**Purpose**: Translates text from one language to another using various translation services.

**Class Definition:**
```python
class LinguaFlowTranslate:
    def __init__(self, target_language: str, source_language: str = "auto", method: str = "googledeep") -> None:
        """
        Initialize translator.
        
        Args:
            source_language (str): Source language name or "auto" for detection
            target_language (str): Target language name
            method (str): Translation service ("googledeep", "googletrans", "googlecloud")
        """
```

**Key Methods:**
- `translate(text: str)`: Translates text and returns translated string

**Usage Examples:**
```python
from utils.translate import LinguaFlowTranslate

# Example 1: Basic translation with auto-detection
translator = LinguaFlowTranslate(
    source_language="auto",
    target_language="yoruba",
    method="googledeep"
)
result = translator.translate("Hello, how are you?")
print(result)  # Output: "Pẹlẹ o, bawo ni o ṣe wa?"

# Example 2: Explicit source language
translator = LinguaFlowTranslate(
    source_language="english",
    target_language="hausa"
)
result = translator.translate("Good morning")
print(result)  # Output: "Barka da safe"

# Example 3: Using different translation methods
translator_deep = LinguaFlowTranslate(target_language="igbo", method="googledeep")
translator_trans = LinguaFlowTranslate(target_language="igbo", method="googletrans")

text = "Thank you very much"
result_deep = translator_deep.translate(text)
result_trans = translator_trans.translate(text)

# Example 4: Chain translations
translator_en_to_yo = LinguaFlowTranslate(source_language="english", target_language="yoruba")
translator_yo_to_ha = LinguaFlowTranslate(source_language="yoruba", target_language="hausa")

english_text = "Welcome to Nigeria"
yoruba_text = translator_en_to_yo.translate(english_text)
hausa_text = translator_yo_to_ha.translate(yoruba_text)
print(f"English: {english_text}")
print(f"Yoruba: {yoruba_text}")
print(f"Hausa: {hausa_text}")
```

**Translation Execution Time:**
The `@calc_execution_time` decorator automatically prints execution time for each translation.

---

### LinguaFlowTTS (speaker.py)

**Purpose**: Converts text to speech and plays the audio output.

**Class Definition:**
```python
class LinguaFlowTTS:
    def __init__(self, language: str = "", method: str = "gTTS") -> None:
        """
        Initialize text-to-speech engine.
        
        Args:
            language (str): Output language for speech synthesis
            method (str): TTS engine ("gTTS", "pyttsx3")
        """
```

**Key Methods:**
- `speak(text: str)`: Converts text to speech and plays it

**Usage Examples:**
```python
from utils.speaker import LinguaFlowTTS

# Example 1: Basic text-to-speech
tts = LinguaFlowTTS(language="english", method="gTTS")
tts.speak("Hello, welcome to LinguaFlow!")

# Example 2: Different languages
tts_yoruba = LinguaFlowTTS(language="yoruba")
tts_yoruba.speak("Ẹ káàbọ̀ sí LinguaFlow")

tts_hausa = LinguaFlowTTS(language="hausa")
tts_hausa.speak("Barka da zuwa LinguaFlow")

tts_igbo = LinguaFlowTTS(language="igbo")
tts_igbo.speak("Nnọọ na LinguaFlow")

# Example 3: Using the class as a callable
tts = LinguaFlowTTS(language="english")
tts("This is a test")  # Calls speak() automatically

# Example 4: Multiple sequential announcements
tts = LinguaFlowTTS(language="english")
messages = [
    "Starting translation service",
    "Please speak into the microphone",
    "Translation complete"
]
for message in messages:
    tts.speak(message)
```

---

### Utility Functions (languages.py)

**Purpose**: Manage language codes and validate language support.

**Available Functions:**
```python
from utils.languages import is_language_supported, get_language_code, get_language

# Check if language is supported
if is_language_supported("yoruba"):
    print("Yoruba is supported!")

# Get language code from name
code = get_language_code("english")  # Returns "en"
code = get_language_code("yoruba")   # Returns "yo"

# Get language name from code
name = get_language("en")  # Returns "english"
name = get_language("yo")  # Returns "yoruba"

# Handle unsupported languages
code = get_language_code("french")  # Returns ""
```

**Available Language Constants:**
```python
from utils.languages import LANGUAGE_CODES, SUPPORTED_LANGUAGES

# All language codes
print(LANGUAGE_CODES)
# Output: {'english': 'en', 'yoruba': 'yo', 'igbo': 'ig', 'hausa': 'ha', 'multi': 'multi'}

# List of supported languages
print(SUPPORTED_LANGUAGES)
# Output: ['english', 'yoruba', 'igbo', 'hausa', 'multi']
```

---

### Performance Monitoring (decorators.py)

**Purpose**: Track execution time of functions for optimization.

**Usage:**
```python
from utils.decorators import calc_execution_time

@calc_execution_time
def my_slow_function():
    # Some time-consuming operation
    pass

my_slow_function()
# Output: Execution time of my_slow_function: 2.345678 seconds
```

## Complete Application Examples

### Example 1: Basic Translation Flow
```python
from utils.listener import LinguaFlowSpeechRecognition
from utils.translate import LinguaFlowTranslate
from utils.speaker import LinguaFlowTTS
from utils.languages import get_language

def simple_translator():
    """Simple one-time translation"""
    
    # Initialize components
    recognizer = LinguaFlowSpeechRecognition(language="multi")
    tts = LinguaFlowTTS(language="english")
    
    # Listen for speech
    print("Speak now...")
    lang_code, text = recognizer.recognize_speech()
    
    if text:
        print(f"You said: {text}")
        
        # Translate to English
        source_lang = get_language(lang_code)
        translator = LinguaFlowTranslate(
            source_language=source_lang,
            target_language="english"
        )
        
        translated = translator.translate(text)
        print(f"Translation: {translated}")
        
        # Speak translation
        tts.speak(translated)

if __name__ == "__main__":
    simple_translator()
```

### Example 2: Continuous Translation Loop
```python
from utils.listener import LinguaFlowSpeechRecognition
from utils.translate import LinguaFlowTranslate
from utils.speaker import LinguaFlowTTS
from utils.languages import get_language

def continuous_translator(target_language="english"):
    """Continuously listen and translate"""
    
    recognizer = LinguaFlowSpeechRecognition(language="multi")
    tts = LinguaFlowTTS(language=target_language)
    
    print(f"Continuous translation mode: Any → {target_language.capitalize()}")
    print("Press Ctrl+C to stop\n")
    
    while True:
        lang_code, text = recognizer.recognize_speech()
        
        if text:
            source_lang = get_language(lang_code)
            print(f"[{source_lang.upper()}]: {text}")
            
            # Skip if already in target language
            if source_lang == target_language:
                print("Already in target language!")
                tts.speak(text)
                continue
            
            # Translate
            translator = LinguaFlowTranslate(
                source_language=source_lang,
                target_language=target_language
            )
            
            translated = translator.translate(text)
            print(f"[{target_language.upper()}]: {translated}\n")
            
            tts.speak(translated)

if __name__ == "__main__":
    continuous_translator(target_language="yoruba")
```

### Example 3: Bidirectional Conversation Assistant
```python
from utils.listener import LinguaFlowSpeechRecognition
from utils.translate import LinguaFlowTranslate
from utils.speaker import LinguaFlowTTS
from utils.languages import get_language

def bidirectional_translator(lang_a="english", lang_b="yoruba"):
    """
    Translate between two languages bidirectionally.
    Detects which language is spoken and translates to the other.
    """
    
    recognizer = LinguaFlowSpeechRecognition(language="multi")
    tts_a = LinguaFlowTTS(language=lang_a)
    tts_b = LinguaFlowTTS(language=lang_b)
    
    print(f"Bidirectional translation: {lang_a.upper()} ↔ {lang_b.upper()}")
    print("Speak in either language\n")
    
    while True:
        lang_code, text = recognizer.recognize_speech()
        
        if not text:
            continue
        
        source_lang = get_language(lang_code)
        print(f"Heard [{source_lang}]: {text}")
        
        # Determine target language
        if source_lang == lang_a:
            target_lang = lang_b
            tts = tts_b
        elif source_lang == lang_b:
            target_lang = lang_a
            tts = tts_a
        else:
            print(f"Unsupported language: {source_lang}")
            continue
        
        # Translate and speak
        translator = LinguaFlowTranslate(
            source_language=source_lang,
            target_language=target_lang
        )
        
        translated = translator.translate(text)
        print(f"Translation [{target_lang}]: {translated}\n")
        
        tts.speak(translated)

if __name__ == "__main__":
    bidirectional_translator(lang_a="english", lang_b="hausa")
```

### Example 4: Multi-Target Translation
```python
from utils.listener import LinguaFlowSpeechRecognition
from utils.translate import LinguaFlowTranslate
from utils.speaker import LinguaFlowTTS
from utils.languages import get_language, SUPPORTED_LANGUAGES

def multi_target_translator():
    """Translate input to multiple target languages"""
    
    recognizer = LinguaFlowSpeechRecognition(language="multi")
    
    # Target languages (excluding 'multi')
    targets = [lang for lang in SUPPORTED_LANGUAGES if lang != "multi"]
    
    print("Multi-target translation mode")
    print(f"Will translate to: {', '.join(targets)}\n")
    
    lang_code, text = recognizer.recognize_speech()
    
    if text:
        source_lang = get_language(lang_code)
        print(f"Source [{source_lang}]: {text}\n")
        
        for target in targets:
            if target == source_lang:
                continue
            
            translator = LinguaFlowTranslate(
                source_language=source_lang,
                target_language=target
            )
            
            translated = translator.translate(text)
            print(f"[{target.upper()}]: {translated}")
            
            # Optionally speak each translation
            tts = LinguaFlowTTS(language=target)
            tts.speak(translated)
            
            print()  # Blank line for readability

if __name__ == "__main__":
    multi_target_translator()
```

### Example 5: Custom Application with User Input
```python
from utils.listener import LinguaFlowSpeechRecognition
from utils.translate import LinguaFlowTranslate
from utils.speaker import LinguaFlowTTS
from utils.languages import get_language, SUPPORTED_LANGUAGES

def interactive_translator():
    """Interactive translation with user configuration"""
    
    print("=" * 60)
    print("LinguaFlow Interactive Translator")
    print("=" * 60)
    
    # Get user preferences
    print("\nAvailable languages:", ", ".join([lang for lang in SUPPORTED_LANGUAGES if lang != "multi"]))
    
    source = input("Enter source language (or 'auto' for detection): ").strip().lower()
    target = input("Enter target language: ").strip().lower()
    
    if source == "auto":
        source = "multi"
    
    # Initialize components
    recognizer = LinguaFlowSpeechRecognition(language=source)
    tts = LinguaFlowTTS(language=target)
    
    print(f"\nMode: {source} → {target}")
    print("=" * 60)
    
    session_count = 0
    
    while True:
        input("\nPress Enter to speak (or Ctrl+C to quit)...")
        
        lang_code, text = recognizer.recognize_speech()
        
        if not text:
            print("No speech detected. Try again.")
            continue
        
        session_count += 1
        detected_lang = get_language(lang_code)
        
        print(f"\n--- Translation #{session_count} ---")
        print(f"Input [{detected_lang}]: {text}")
        
        # Translate
        translator = LinguaFlowTranslate(
            source_language=detected_lang if source == "multi" else source,
            target_language=target
        )
        
        translated = translator.translate(text)
        print(f"Output [{target}]: {translated}")
        
        # Ask if user wants to hear it
        speak = input("Speak translation? (y/n): ").strip().lower()
        if speak == 'y':
            tts.speak(translated)

if __name__ == "__main__":
    try:
        interactive_translator()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
```

## Configuration

### Language Codes

Language mappings are defined in `utils/languages.py`:
```python
LANGUAGE_CODES = {
    "english": "en",
    "yoruba": "yo",
    "igbo": "ig",
    "hausa": "ha",
    "multi": "multi"
}
```

## Web Interface

LinguaFlow includes a web-based interface for easy access through your browser, eliminating the need for command-line interaction.

### Features

- **Browser-based Interface**: Access LinguaFlow through any modern web browser
- **Click-to-Record**: Simple microphone button to start/stop recording
- **Language Selection**: Dropdown menus for source and target language selection
- **Real-time Processing**: Immediate translation and audio playback
- **Visual Feedback**: Clear status indicators and results display
- **Responsive Design**: Works on desktop and mobile devices

### Setup and Running

1. **Install Additional Dependencies**

The web interface requires additional packages:
```bash
pip install Flask av numpy soundfile
```

**Note**: These packages include all necessary audio processing libraries. No external software (like FFmpeg) needs to be installed.

2. **Run the Web Application**
```bash
python app.py
```

3. **Access the Interface**

Open your browser and navigate to:
```
http://localhost:5000
```

Or from another device on the same network:
```
http://YOUR_IP_ADDRESS:5000
```

To find your IP address:
- **Windows**: `ipconfig` in Command Prompt
- **Mac/Linux**: `ifconfig` or `ip addr` in Terminal

### Using the Web Interface

1. **Select Languages**
   - Choose source language (or "Auto-detect")
   - Choose target language

2. **Record Audio**
   - Click the blue microphone button
   - **Allow microphone access** when your browser prompts you
   - Speak clearly into your microphone
   - Click the button again (now red) to stop recording

3. **View Results**
   - The recognized text in the source language
   - The translated text in the target language
   - An audio player to hear the translation

### Browser Microphone Access

When you first click the microphone button, your browser will ask for permission to use your microphone:

**Chrome/Edge**: Click "Allow" in the popup at the top of the page

**Firefox**: Click "Allow" in the address bar popup

**Safari**: Click "OK" in the dialog box

**If you accidentally blocked access:**
1. Click the lock/info icon in your browser's address bar
2. Find "Microphone" in the permissions list
3. Change to "Allow"
4. Refresh the page

### Troubleshooting Web Interface

**"Microphone access denied" error:**
- Check browser permissions (see above)
- Ensure your microphone is connected and working
- Try a different browser
- Check system microphone permissions:
  - **Windows**: Settings → Privacy → Microphone
  - **Mac**: System Preferences → Security & Privacy → Microphone
  - **Linux**: Check audio settings

**"Could not understand audio" error:**
- Speak more clearly and at a moderate pace
- Reduce background noise
- Move closer to the microphone
- Check microphone input volume in system settings

**Audio conversion errors:**
- Ensure all dependencies are installed: `pip install Flask av numpy soundfile`
- Try recording a shorter audio clip
- Restart the Flask application

**Connection errors:**
- Ensure Flask is running: `python app.py`
- Check the correct port (default is 5000)
- Disable VPN if using
- Check firewall settings if accessing from another device

### File Structure for Web Interface
```
LinguaFlow/
├── app.py                 # Flask web application
├── templates/
│   └── index.html        # Web interface
├── temp_audio/           # Temporary audio files (auto-created)
├── utils/
│   └── ...               # Core modules
└── requirements.txt
```

### Deployment Notes

The web interface is designed for local or internal network use. For production deployment:

- Use a production WSGI server (e.g., Gunicorn, uWSGI)
- Enable HTTPS for secure microphone access
- Consider cloud deployment (Heroku, AWS, Google Cloud)
- Implement user authentication if needed
- Add rate limiting for API endpoints

### Dependencies for Web Interface

Add these to your `requirements.txt`:
```txt
Flask==3.0.0
av==11.0.0
numpy==1.24.3
soundfile==0.12.1
```

**Why these libraries?**
- **Flask**: Web framework for the interface
- **av (PyAV)**: Audio format conversion (includes FFmpeg libraries)
- **numpy**: Numerical operations for audio processing
- **soundfile**: Writing WAV files

These packages handle all audio processing without requiring users to install external software like FFmpeg.

## Future Development

### Hardware Implementation

LinguaFlow is designed to be deployed on embedded hardware:

- **Target Platform**: ESP32 microcontroller
- **Programming Language**: MicroPython
- **Hardware Components**:
  - Microphone for audio input
  - Speaker for audio output
  - ESP32 for processing and connectivity

The Python codebase will be adapted for MicroPython with considerations for:
- Memory constraints
- Limited library availability
- Real-time audio streaming
- Power efficiency

## Troubleshooting

### Microphone Not Working

- Ensure your microphone is properly connected and set as default input device
- On Linux, check that you have proper permissions for audio device access
- Verify PyAudio installation: `python -c "import pyaudio"`

### Translation Errors

- Check your internet connection (all translation methods require internet)
- For `googlecloud` method, ensure API credentials are properly configured
- Try switching to a different translation method if one fails

### Audio Playback Issues

- Verify speaker/headphone connection
- Check system audio settings and volume levels
- Ensure `playsound` library is properly installed

### Git Issues

**Merge Conflicts:**
```bash
# Update your branch with latest main
git checkout main
git pull origin main
git checkout your-branch
git merge main
# Resolve conflicts in your editor, then:
git add .
git commit -m "Resolve merge conflicts"
```

**Push Update**
```bash
# Push your update to main repo
git push origin main:main # Note that the first main is the name of your local repo and the second main is the name of remote repo you want to push to. You may replace the names with the respective names
```

## Contributing

For contributions from project members, please follow these guidelines to ensure a smooth collaboration process.

### Branching Strategy

1. **Clone the Repository**

If you haven't already, clone the repository:
```bash
git clone https://github.com/REPOSITORY_OWNER/LinguaFlow.git
cd LinguaFlow
```

2. **Create a Feature Branch**

Always create a new branch for your work. Never work directly on `main`.
```bash
# Update your local main branch first
git checkout main
git pull origin main

# Create and switch to a new feature branch
git checkout -b feature/your-feature-name
```

**Branch Naming Convention:**
- `feature/feature-name` - For new features
- `fix/bug-name` - For bug fixes
- `docs/description` - For documentation updates
- `refactor/description` - For code refactoring

Examples:
- `feature/add-french-support`
- `fix/microphone-timeout-error`
- `docs/update-readme`

### Making Changes

1. **Make Your Changes**

Write your code following the existing code style and structure.

2. **Test Your Changes**

Ensure your changes work correctly:
```bash
python main.py
```

3. **Commit Your Changes**

Write clear, descriptive commit messages:
```bash
git add .
git commit -m "Add: Brief description of what you added/changed"
```

**Commit Message Format:**
- `Add: Description` - For new features
- `Fix: Description` - For bug fixes
- `Update: Description` - For updates to existing features
- `Refactor: Description` - For code refactoring
- `Docs: Description` - For documentation changes

Examples:
```bash
git commit -m "Add: Support for French language translation"
git commit -m "Fix: Microphone timeout error in listener module"
git commit -m "Update: Improved error messages in translate.py"
```

### Submitting Your Contribution

1. **Push to the Repository**
```bash
git push origin feature/your-feature-name
```

2. **Create a Pull Request**

- Go to the repository on GitHub
- Click "Pull Request" button
- Select your feature branch
- Fill in the PR template with:
  - **Description**: What changes you made and why
  - **Testing**: How you tested your changes
  - **Related Issues**: Link any related issues

3. **Wait for Review**

- The project maintainer will review your PR
- Address any requested changes by pushing new commits to your branch
- Once approved, your changes will be merged

### Keeping Your Branch Updated

Regularly sync your branch with the main branch:
```bash
# Fetch latest changes
git fetch origin

# Switch to main branch
git checkout main

# Pull latest changes
git pull origin main

# Switch back to your feature branch
git checkout your-feature-branch

# Merge main into your feature branch
git merge main
```

### Code Style Guidelines

- Follow existing code structure and naming conventions
- Use descriptive variable and function names
- Add docstrings to new functions and classes
- Keep functions focused on a single responsibility
- Comment complex logic

### Before Submitting

- [ ] Code runs without errors
- [ ] Tested with multiple languages (if applicable)
- [ ] No unnecessary files included (e.g., `__pycache__`, `.pyc` files)
- [ ] You can create a ```.gitignore``` file in your root folder and input the following code in it: 
    ```bash
    .gitignore
    *__pycache___/
    *.pyc
    <your_virtual_env_folder_name>/ # Remove angular brackets
    ```
---
- [ ] Update documentation if needed
- [ ] Commit messages are clear and descriptive

**Note**: This project is currently in active development. The codebase will undergo further optimization and feature additions before hardware deployment.