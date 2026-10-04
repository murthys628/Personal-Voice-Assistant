"""Optional microphone and text-to-speech adapters."""


class SpeechUnavailable(RuntimeError):
    """Raised when a speech dependency or audio device is unavailable."""


class SpeechIO:
    def __init__(self) -> None:
        self._engine = None

    def listen(self) -> str | None:
        try:
            import speech_recognition as sr
        except ImportError as error:
            raise SpeechUnavailable("install the optional 'voice' dependencies") from error

        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.4)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            return recognizer.recognize_google(audio)
        except (sr.UnknownValueError, sr.WaitTimeoutError):
            return None
        except sr.RequestError as error:
            raise SpeechUnavailable("speech recognition service is unavailable") from error
        except (OSError, AttributeError) as error:
            raise SpeechUnavailable("no usable microphone was found") from error

    def speak(self, text: str) -> None:
        try:
            import pyttsx3
            if self._engine is None:
                self._engine = pyttsx3.init()
            self._engine.say(text)
            self._engine.runAndWait()
        except ImportError as error:
            raise SpeechUnavailable("install the optional 'voice' dependencies") from error
        except Exception as error:
            raise SpeechUnavailable("text-to-speech is unavailable") from error