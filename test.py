import ollama
import os
import time

# os.system("ollama run llama3.2:3b")

# time.sleep(5)

stream = ollama.chat(
    model='llama3.2:3b',
    messages=[{'role': 'user', 'content': 'Why is the sky blue?'}],
    stream=True,
)

for chunk in stream:
  print(chunk['message']['content'], end = '')