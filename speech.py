import os
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import smtplib
from dotenv import load_dotenv
import openai
import pywhatkit
import subprocess
import json

# Load secrets from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SENDER_EMAIL = os.getenv("EMAIL")
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")
openai.api_key = OPENAI_API_KEY

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 180)

def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        command = r.recognize_google(audio, language='en-in')
        print(f"You said: {command}")
        return command.lower()
    except Exception as e:
        print("Recognition error:", e)
        return None

def send_email(content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, content)
        server.close()
        speak("Email has been sent successfully!")
    except Exception as e:
        print("Email error:", e)
        speak("Sorry, I was not able to send the email.")

def greet_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        greeting = "Good Morning!"
    elif hour < 18:
        greeting = "Good Afternoon!"
    else:
        greeting = "Good Evening!"
    speak(f"{greeting} I am Jarvis. How can I assist you today?")

def handle_command(query):
    if not query:
        return

    # Wikipedia search
    if 'wikipedia' in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)
        except:
            speak("Sorry, I couldn't find Wikipedia results.")

    # YouTube
    elif 'play' in query and 'youtube' in query:
        song = query.replace("play", "").replace("on youtube", "").strip()
        speak(f"Playing {song} on YouTube")
        try:
            pywhatkit.playonyt(song)
        except:
            webbrowser.open(f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}")

    # Open website
    elif 'open' in query:
        if 'youtube' in query:
            webbrowser.open("https://youtube.com")
        elif 'google' in query:
            webbrowser.open("https://google.com")
        elif 'stackoverflow' in query:
            webbrowser.open("https://stackoverflow.com")
        else:
            speak("Which website should I open?")
    
    # Time
    elif 'time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M")
        speak(f"The time is {strTime}")

    # Send email
    elif 'email' in query or 'mail' in query:
        speak("What should I say?")
        content = take_command()
        if content:
            send_email(content)
        else:
            speak("I didn't catch the message content.") 

    # Exit
    elif 'exit' in query or 'quit' in query or 'goodbye' in query:
        speak("Goodbye! Have a great day.")
        exit()

    # Default: Google search
    else:
        search_query = query.replace(" ", "+")
        speak(f"Searching Google for {query}")
        webbrowser.open(f"https://www.google.com/search?q={search_query}")

if __name__ == "__main__":
    greet_user()
    while True:
        command = take_command()
        handle_command(command)
