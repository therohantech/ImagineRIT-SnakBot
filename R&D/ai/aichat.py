import speech_recognition as sr
import pyttsx3
import ollama

class InteractiveAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        self.tts = pyttsx3.init()
        self.setup_tts()

    def setup_tts(self):
        self.tts.setProperty('rate', 150)  # Adjust speed
        self.tts.setProperty('volume', 1.0)  # Set max volume

    def speak(self, text):
        print(f"Assistant: {text}")
        self.tts.say(text)
        self.tts.runAndWait()

    def listen(self):
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            try:
                audio = self.recognizer.listen(source)
                text = self.recognizer.recognize_google(audio).lower()
                print(f"User: {text}")
                return text
            except sr.UnknownValueError:
                return "I didn't understand that. Can you repeat?"
            except sr.RequestError:
                return "Speech recognition service is unavailable."

    def chat_with_ai(self, user_input):
        response = ollama.chat(model='mistral', messages=[
            {"role": "user", "content": user_input}
        ])
        return response['message']['content']

    def run(self):
        self.speak("Hello! I am your interactive assistant. Ask me anything about the robot.")
        while True:
            user_input = self.listen()
            if "exit" in user_input or "goodbye" in user_input:
                self.speak("Goodbye! Have a great day!")
                break
            response = self.chat_with_ai(user_input)
            self.speak(response)

if __name__ == "__main__":
    assistant = InteractiveAssistant()
    assistant.run()
