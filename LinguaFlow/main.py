"""
    LinguaFlow Program Entry Module - main.py
    ----------------------------------------
    Main entry point for the LinguaFlow CLI application.
"""

from utils.listener import LinguaFlowSpeechRecognition
from utils.translate import LinguaFlowTranslate
from utils.speaker import LinguaFlowTTS
from utils.languages import get_language


def main():
    linguaflow_recognizer = LinguaFlowSpeechRecognition(language="yoruba")
    linguaflow_tts = LinguaFlowTTS(language="hausa", method="yarngpt")

    while True:
        recognized_speech_code, recognized_speech = linguaflow_recognizer.recognize_speech()

        if recognized_speech:
            print(f"Recognized speech: {recognized_speech}")
            recognised_language = get_language(recognized_speech_code)
            linguaflow_translator = LinguaFlowTranslate(
                source_language=recognised_language,
                target_language="hausa"
            )
            translated_text = linguaflow_translator.translate(recognized_speech)
            print(f"Translated Speech: {translated_text}")
            linguaflow_tts.speak(translated_text)


if __name__ == "__main__":
    main()