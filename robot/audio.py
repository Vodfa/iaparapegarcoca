from dataclasses import dataclass
from typing import Optional

import pyttsx3
import speech_recognition as sr


@dataclass
class AudioConfig:
    input_device_index: Optional[int]
    output_voice: Optional[str]
    language: str


class AudioInterface:
    def __init__(self, config: AudioConfig) -> None:
        self._recognizer = sr.Recognizer()
        self._microphone = sr.Microphone(device_index=config.input_device_index)
        self._tts_engine = pyttsx3.init()
        if config.output_voice:
            for voice in self._tts_engine.getProperty("voices"):
                if config.output_voice in voice.name:
                    self._tts_engine.setProperty("voice", voice.id)
                    break
        self._language = config.language

    def listen(self, timeout_s: float = 5.0) -> Optional[str]:
        with self._microphone as source:
            self._recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self._recognizer.listen(source, timeout=timeout_s)
            except sr.WaitTimeoutError:
                return None
        try:
            return self._recognizer.recognize_google(audio, language=self._language)
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return None

    def speak(self, text: str) -> None:
        self._tts_engine.say(text)
        self._tts_engine.runAndWait()
