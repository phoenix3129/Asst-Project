import datetime

class TaskManager:
    def __init__(self):
        self.task_file = "tasks.txt"

    def add_task(self, task, speech_module):
        date_entry = datetime.datetime.now().strftime("%Y-%m-%d")
        with open(self.task_file, "a") as f:
            f.write(f"{date_entry}: {task}\n")
        speech_module.speak(f"Task '{task}' added.")

    def fetch_tasks(self, speech_module):
        date_entry = datetime.datetime.now().strftime("%Y-%m-%d")
        with open(self.task_file, "r") as f:
            tasks = [line.strip().split(": ")[1] for line in f.readlines() if line.startswith(date_entry)]
        if tasks:
            speech_module.speak(f"You have {len(tasks)} tasks left.")
            speech_module.speak(f"Your next task is: {tasks[0]}")
        else:
            speech_module.speak("No task in queue brother, just chill.")
