import datetime

class MemoManager:
    def __init__(self):
        self.memo_file = "memo.txt"

    def take_memo(self, speech_module):
        speech_module.speak("Tell me what you want to note down.")
        memo_content = ""
        while True:
            line = speech_module.listen()
            if line and "stop writing" in line:
                speech_module.speak("Memo saved.")
                date_entry = datetime.datetime.now().strftime("%Y-%m-%d")
                with open(self.memo_file, "a") as f:
                    f.write(f"{date_entry}: {memo_content}\n")
                break
            elif line:
                memo_content += line + ". "
                speech_module.speak("Got it. Anything else?")

    def fetch_memo(self, speech_module):
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        with open(self.memo_file, "r") as f:
            memos = [line.strip() for line in f.readlines() if line.startswith(today)]
        if memos:
            speech_module.speak(f"Here is what you told me: {memos[0]}")
        else:
            speech_module.speak("I have no memo for today.")
