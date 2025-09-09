import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QMovie, QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import sys
import subprocess
import pywhatkit
import openai
import json
# from .env import load_dotenv

# # Load .env variables
# load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SENDER_EMAIL = os.getenv("EMAIL")
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")
openai.api_key = OPENAI_API_KEY

# Text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 180)

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# Email sender
def sendEmail(content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, content)
        server.close()
        speak("Email has been sent successfully!")
    except Exception as e:
        speak("Sorry, I was not able to send the email.")
        print("Error:", e)

# Intent recognition
def get_intent_and_entities(query):
    query_lower = query.lower()
    if any(word in query_lower for word in ["play", "song", "music"]):
        song = query_lower.replace("play", "").strip()
        return "play_music", {"song": song, "platform": "youtube"}
    elif "wikipedia" in query_lower:
        search_term = query_lower.replace("wikipedia", "").strip()
        return "search_wikipedia", {"search_query": search_term}
    elif any(word in query_lower for word in ["open", "launch", "start"]):
        if "chrome" in query_lower: return "open_application", {"application_name": "chrome"}
        if "vscode" in query_lower or "code" in query_lower: return "open_application", {"application_name": "vscode"}
        if any(site in query_lower for site in ["youtube", "google", "stackoverflow"]):
            return "open_website", {"website": query_lower.split()[-1]}
    elif "time" in query_lower: return "tell_time", {}
    elif "email" in query_lower or "mail" in query_lower: return "send_email", {}
    elif any(word in query_lower for word in ["exit", "quit", "goodbye"]): return "exit", {}
    
    # Fallback: OpenAI
    try:
        prompt = f"""
Analyze this command and identify the intent and key information:
Command: "{query}"
Possible intents: play_music, open_website, search_wikipedia, send_email, tell_time, open_application, exit, google_search
Respond with JSON format like this:
{{
  "intent": "intent_name",
  "entities": {{"key1": "value1"}}
}}
"""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a command analyzer."},
                      {"role": "user", "content": prompt}],
            temperature=0.3
        )
        data = json.loads(response['choices'][0]['message']['content'])
        return data['intent'], data.get('entities', {})
    except Exception as e:
        print("OpenAI error:", e)
        return "google_search", {"search_query": query}

# ------------------- Thread -------------------
class JarvisThread(QThread):
    signal = pyqtSignal(str)          # For user input
    response_signal = pyqtSignal(str) # For Jarvis responses

    def run(self):
        # 1️⃣ Greeting first
        hour = datetime.datetime.now().hour
        if hour < 12: greeting = "Good Morning!"
        elif hour < 18: greeting = "Good Afternoon!"
        else: greeting = "Good Evening!"

        greeting_text = f"Jarvis: {greeting} I am Jarvis. How are you today?"
        self.signal.emit(greeting_text)
        speak(f"{greeting} I am Jarvis. How are you today?")

        # 2️⃣ Start listening loop
        while True:
            query = self.takeCommand()
            if query:
                self.signal.emit(f"You: {query}")
                self.handleCommand(query)

    def takeCommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source)
            try:
                audio = r.listen(source)
                command = r.recognize_google(audio, language='en-in')
                return command.lower()
            except: return None

    def handleCommand(self, query):
        intent, entities = get_intent_and_entities(query)
        self.response_signal.emit(f"Jarvis: Processing '{intent}' command...")
        try:
            if intent == "search_wikipedia":
                term = entities.get("search_query", query)
                results = wikipedia.summary(term, sentences=2)
                self.response_signal.emit(f"Jarvis: {results}")
                speak(results)
            elif intent == "play_music":
                song = entities.get("song", query)
                self.response_signal.emit(f"Jarvis: Playing {song}")
                speak(f"Playing {song}")
                pywhatkit.playonyt(song)
            elif intent == "open_website":
                site = entities.get("website", "google")
                url_map = {"youtube":"https://youtube.com","google":"https://google.com","stackoverflow":"https://stackoverflow.com"}
                url = url_map.get(site, f"https://{site}.com")
                self.response_signal.emit(f"Jarvis: Opening {site}")
                speak(f"Opening {site}")
                webbrowser.open(url)
            elif intent == "tell_time":
                t = datetime.datetime.now().strftime("%H:%M")
                self.response_signal.emit(f"Jarvis: The time is {t}")
                speak(f"The time is {t}")
            elif intent == "send_email":
                speak("What should I say?")
                content = self.takeCommand()
                if content: sendEmail(content)
            elif intent == "open_application":
                app = entities.get("application_name", "").lower()
                paths = {"vscode":"C:\\Program Files\\Microsoft VS Code\\Code.exe",
                         "chrome":"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"}
                if app in paths: os.startfile(paths[app])
            elif intent == "exit":
                self.response_signal.emit("Jarvis: Goodbye!")
                speak("Goodbye!")
                os._exit(0)
            else:  # Default Google search
                query_str = query.replace(" ", "+")
                self.response_signal.emit(f"Jarvis: Searching for {query}")
                speak(f"Searching for {query}")
                webbrowser.open(f"https://www.google.com/search?q={query_str}")
        except Exception as e:
            print("Command handling error:", e)
            self.response_signal.emit("Jarvis: Error processing command")
            speak("Sorry, error occurred")

        # ---------------- GUI ----------------
class JarvisGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JARVIS AI Assistant")
        self.setGeometry(300, 100, 800, 600)

        # Main widget & layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # GIF
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.movie = QMovie("jarvis.gif")
        self.label.setMovie(self.movie)
        self.movie.start()
        layout.addWidget(self.label)

        # Conversation
        self.conversation = QLabel("Initializing Jarvis...")
        self.conversation.setAlignment(Qt.AlignLeft)
        self.conversation.setWordWrap(True)
        self.conversation.setStyleSheet("color: #00FF00; background-color: #111; padding:10px; border-radius:5px;")
        layout.addWidget(self.conversation)

        # Buttons
        button_layout = QVBoxLayout()
        buttons = [
            ("🎵 Play Music", self.play_music),
            ("🌐 Open Browser", lambda: webbrowser.open("https://google.com")),
            ("📧 Compose Email", self.compose_email),
            ("🕒 Current Time", self.current_time),
            ("❌ Exit", self.close)
        ]
        for text, action in buttons:
            btn = QPushButton(text)
            btn.setStyleSheet("background-color:#1E90FF; color:white; padding:10px; border-radius:5px;")
            btn.clicked.connect(action)
            button_layout.addWidget(btn)
        layout.addLayout(button_layout)

        # Start Jarvis thread
        self.thread = JarvisThread()
        self.thread.signal.connect(self.update_conversation)
        self.thread.response_signal.connect(self.update_conversation)
        self.thread.start()

    def update_conversation(self, text):
        current = self.conversation.text()
        self.conversation.setText(current + "\n" + text)

    def play_music(self):
        self.update_conversation("You clicked: Play Music")
        speak("What song would you like me to play?")

    def compose_email(self):
        self.update_conversation("You clicked: Compose Email")
        speak("Who should I send the email to?")

    def current_time(self):
        t = datetime.datetime.now().strftime("%H:%M")
        self.update_conversation(f"Jarvis: The current time is {t}")
        speak(f"The current time is {t}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = JarvisGUI()
    window.show()
    sys.exit(app.exec_())
