# First, let's start with refactoring the `main.py` to handle the core VoiceAssistant class and integrate other modules.
import ollama
import sys
import time
from speech_module import SpeechModule  # Import speech handling functions
from browser import VirtualBrowser  # Import browsing module
from memo_manager import MemoManager  # Import memo management functions
from task_manager import TaskManager  # Import task management functions
import eel 

class VoiceAssistant:
    def __init__(self):
        self.speech = SpeechModule()  # Voice speaking and listening handled in the SpeechModule
        self.browser = VirtualBrowser()  # Browsing functionality managed by VirtualBrowser
        self.memo_manager = MemoManager()  # Memo handling by MemoManager
        self.task_manager = TaskManager()  # Task handling by TaskManager
        self.is_active = False
        self.keyword = 'jarvis'
        # eel.init('web')  # Initialize Eel with the 'web' folder for HTML/CSS/JS

    # Wait for the activation keyword
    def wait_for_keyword(self):
        while True:
            text = self.speech.listen()
            if text and self.keyword.lower() in text:
                self.speech.speak(f"Hello! How can I help you?")
                self.is_active = True
                eel.setState('speaking')  # Update blob to speaking state in the GUI
                return

    # Handle browsing tasks through LLaMA 3.2
    def handle_browsing(self, query):
        self.speech.speak("Let me find that for you.")
        eel.setState('speaking')  # Set GUI state to speaking
        response = self.browser.browse(query)  # Browse via LLaMA 3.2
        self.speech.speak(response)

    # Handle incoming commands
    def handle_command(self, text):
        eel.setState('listening')  # Update blob to listening state in the GUI

        if "browse" in text:
            query = text.replace("browse", "").strip()
            self.handle_browsing(query)
        elif "memo" in text or "take a note" in text:
            self.memo_manager.take_memo(self.speech)
        elif "what did i tell you" in text and "today" in text:
            self.memo_manager.fetch_memo(self.speech)
        elif "add task" in text:
            task = text.replace("add task", "").strip()
            self.task_manager.add_task(task, self.speech)
        elif "what is left for today" in text:
            self.task_manager.fetch_tasks(self.speech)
        elif "time" in text:
            current_time = time.strftime('%H:%M')
            self.speech.speak(f"The current time is {current_time}.")
        elif "stop listening" in text:
            self.speech.speak("Okay, I will stop listening now. Say 'Kanha' to wake me up again.")
            self.is_active = False
            # eel.setState('idle')  # Set GUI state to idle
        elif "exit" in text:
            self.speech.speak("Goodbye, take care!")
            # eel.setState('idle')  # Reset the GUI state before exiting
            sys.exit()
        else:
            # Use the streaming feature for unrecognized commands
            self.speech.speak("Let me think about that...")
            # eel.setState('speaking')  # Set GUI state to thinking
            try:
                stream = ollama.chat(
                    model='llama3.2',
                    messages=[{'role': 'user', 'content': f"very briefly(under 60 words):{text}"}],
                    stream=True
                )
                buffer = ""
                sentence_endings = ['.', '!', '?']
                for chunk in stream:
                    buffer += chunk['message']['content']
                    # Check if a complete sentence or phrase is in the buffer
                    if any(buffer.endswith(end) for end in sentence_endings):
                        self.speech.speak(buffer.strip())  # Speak the complete sentence
                        buffer = ""  # Clear buffer for the next sentence
                # Speak any remaining content in the buffer after streaming ends
                if buffer.strip():
                    self.speech.speak(buffer.strip())
            except ollama.ResponseError as e:
                self.speech.speak(f"An error occurred: {e}")
            # finally:
            #     eel.setState('idle')  # Reset to idle after responding


    # Start the assistant and wait for keyword
    def start(self):
        # eel.start('index.html', mode='brave', block=False)  # Start the GUI in a non-blocking way
        retry_count = 0
        while True:
            if self.is_active:
                text = self.speech.listen()
                if text:
                    self.handle_command(text)
                    retry_count = 0
                else:
                    retry_count += 1
                    if retry_count >= 3:
                        self.speech.speak("I will wait for you to say 'Jarvis' again.")
                        # eel.setState('idle')  # Set GUI state to idle
                        self.is_active = False
                    else:
                        self.speech.speak("I'm still listening, please say your command.")
            else:
                # eel.setState('idle')  # Reset to idle while waiting for the keyword
                self.wait_for_keyword()


# Instantiate and run the assistant
if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.start()
