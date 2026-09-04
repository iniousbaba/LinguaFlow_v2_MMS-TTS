# IMPORTING PROGRAM DEPENDENCIES
import speech_recognition as sr
from speech_recognition import WaitTimeoutError, UnknownValueError, RequestError
from utils.languages import get_language_code, LANGUAGE_CODES


#==========================================================================================================================================
#=============================================LINGUAFLOW SPEECH RECOGNITION CLASS DEFINITION================================================
#==========================================================================================================================================
class LinguaFlowSpeechRecognition:
    def __init__(self, language="multi", method="google") -> None:
        """
            Speech Recognition class to take in audio input via the default microphone, convert it text
            and return the text output.
            :param language: The language for speech recognition. Default is "multi" for multiple languages.
            :param method: The speech recognition method to be used. Default is "google".

            Supported methods:
            - google: Uses Google Speech Recognition API.

            Supported languages:
            - multi: For English, Yoruba, Igbo, and Hausa recognition.
            - english: For English recognition only.
            - yoruba: For Yoruba recognition only.
            - igbo: For Igbo recognition only.
            - hausa: For Hausa recognition only.
        """

        assert language in LANGUAGE_CODES.keys(), f"Unsupported language: {language}. Supported languages are: {list(LANGUAGE_CODES.keys())}"

        self.__language = language # Recognition Language
        self.__language_code = get_language_code(language) # Recognition Language Code
        self.__language_codes = LANGUAGE_CODES
        self.__method = method # Recognition Method

        self.__recognizer = sr.Recognizer()

        self.__speech_recognition_methods = {
            "google" : self.__recognize_speech_with_google,
        }
    #======================================================================================================================================

    def __repr__(self):
        """
            String representation of LinguaFlowSpeechRecognition class displaying 
        """
        return f"LinguaFlowSpeechRecognition(language={self.__language}, method={self.__method})"
    #======================================================================================================================================

    def __call__(self):
        """
            This is executed if class instance is called as a function. 
        """
        return self.recognize_speech()

    def __record_audio(self):
        """
            Captures audio via the default microphone and returns the audio data
        """

        with sr.Microphone() as audio_source:
            self.__recognizer.adjust_for_ambient_noise(audio_source, duration=1) # Adjusting for ambient noise levels to improve accuracy
            try:
                print(f"\nLinguaFlow is Listening ... ")
                audio_data = self.__recognizer.listen(audio_source) # Listening for audio input
            except WaitTimeoutError:
                print(f"\nSpeech Recognition Timeout Error: No speech detected within the timeout period.")
                audio_data = None

        return audio_data
    #======================================================================================================================================

    def __recognize_speech_with_google(self, language) -> str :
        """
            Recognizes speech using Google Speech Recognition API and returns the text output
        """

        audio_data = self.__record_audio() # Recording audio input

        recognized_text = ""

        if audio_data is not None:
            recognized_text = self.__recognizer.recognize_google(audio_data, language=language)

        return recognized_text
    #======================================================================================================================================
    
    def recognize_speech(self) -> tuple[str, str]:
        """
            Public method to recognize speech based on the specified lanuguage setting and speech recognition method

            If language is set to "multi", it will attempt to recognize speech in multiple languages (English, Yoruba, Igbo, Hausa)
            and return the recognized text along with the detected language.

            :return: A tuple containing the detected language code and the recognized text.
        """

        speech_recognition_function = self.__speech_recognition_methods.get(self.__method, self.__recognize_speech_with_google)

        recognized_language_code, recognized_text = "", ""

        if self.__language == "multi":

            for language_name, language_code in self.__language_codes.items():

                if language_name == list(self.__language_codes.keys())[-1]: # Last language on the list, multi
                    print(f"LinguaFlow could not understand the audio input.")
                    break

                try: 
                    recognized_text = speech_recognition_function(language=language_code)

                    if recognized_text:
                        print(f"Recognized Language: {language_name.capitalize()}")
                        recognized_language_code = language_code
                        break

                except UnknownValueError:
                    continue

        else: 
            try: 
                recognized_text = speech_recognition_function(self.__language_code)
                recognized_language_code = self.__language_code
            except UnknownValueError:
                recognized_text = ""
                recognized_language_code = ""
                print(f"\nLinguaFlow could not understand the audio input.")

        return recognized_language_code, recognized_text
    #======================================================================================================================================
