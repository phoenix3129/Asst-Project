import pyttsx3
import speech_recognition as sr

class SpeechModule:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)  # Set to male voice
        self.recognizer = sr.Recognizer()

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self, max_time=20):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")

            # Loop to listen dynamically based on silence detection
            audio = None
            try:
                audio = self.recognizer.listen(source, timeout=max_time, phrase_time_limit=max_time)
                text = self.recognizer.recognize_google(audio).lower()
                print(f"You said: {text}")
                return text
            except sr.WaitTimeoutError:
                self.speak("I didn't hear anything. Could you please speak again?")
                return None
            except sr.UnknownValueError:
                self.speak("Sorry, I didn't catch that. Please repeat.")
                return None
            except sr.RequestError:
                self.speak("There seems to be a network issue.")
                return None

