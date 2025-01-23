import ollama

class VirtualBrowser:
    def browse(self, search_query):
        prompt = f"Search the web for: {search_query}"
        stream = ollama.chat(model='llama3.2:3b', messages=[{'role': 'user', 'content': prompt}], stream=True)
        result = ""
        for chunk in stream:
            result += chunk['message']['content']
        return result
