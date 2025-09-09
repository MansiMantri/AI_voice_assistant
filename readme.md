
---

# JARVIS - AI Desktop Voice Assistant 🤖
---

## Overview

**JARVIS** is an AI-powered desktop voice assistant built in Python. It integrates speech recognition, text-to-speech, OpenAI GPT-3.5 for advanced command processing, and a modern PyQt5 GUI interface.

Users can interact via voice or GUI to perform tasks like:

* Playing music on YouTube or Spotify
* Searching Wikipedia
* Opening websites or desktop applications
* Sending emails
* Asking the current time

The assistant provides a conversational interface and displays the full conversation in the GUI.

---

## How to Run the Project

### Prerequisites

* Python 3.10+
* pip package manager
* Microphone for voice commands

### Steps to Run

1. **Clone the repository**

```bash
git clone https://github.com/MansiMantri/AI-Voice-assistant.git
cd AI-Voice-assistant
```

2. **Create a virtual environment**

```bash
python -m venv venv
```

3. **Activate the virtual environment**

* Windows:

```bash
.\venv\Scripts\activate
```

* macOS/Linux:

```bash
source venv/bin/activate
```

4. **Install required packages**

```bash
pip install -r requirements.txt
```

5. **Set up `.env` file**

Create a `.env` file in the root directory with your credentials:

```
OPENAI_API_KEY=your_openai_api_key
EMAIL=your_email@gmail.com
EMAIL_PASSWORD=your_email_password
RECIPIENT_EMAIL=recipient_email@gmail.com
```

> **Do not push `.env` to GitHub.**

6. **Run the application**

```bash
python main.py
```

* JARVIS will greet you and start listening for commands.
* You can also use GUI buttons for quick actions.

---

## Features Achieved

* 🎤 **Voice Interaction**: Speak to JARVIS and it responds naturally.
* 📰 **Wikipedia Search**: Get summaries from Wikipedia quickly.
* 🎵 **Play Music**: Play songs on YouTube or Spotify via voice commands.
* 🌐 **Open Websites/Apps**: Launch Chrome, VS Code, or open websites like YouTube, Google, StackOverflow.
* 📧 **Email Sending**: Send emails directly via Gmail (credentials in `.env`).
* 🕒 **Tell Time**: Ask JARVIS for the current time.
* 💡 **AI-Powered Intent Recognition**: GPT-3.5-turbo handles complex commands.
* 🖥 **GUI Interface**: Modern PyQt5 interface with GIF animation and full conversation display.
* 🔘 **Quick Action Buttons**: Buttons for playing music, opening browser, sending email, checking time, and exit.

---

## Technical Achievements

* Integrated **OpenAI GPT-3.5** for intelligent intent recognition.
* Built a responsive **PyQt5 GUI** for a real-time interactive desktop experience.
* Used **pyttsx3** for text-to-speech and **speech\_recognition** for speech-to-text.
* Added **YouTube playback** using **pywhatkit**.
* Handled **email sending** securely through environment variables.
* Designed dynamic conversation display to track all interactions.

---

## Design Achievements

* Modern desktop GUI with **GIF animation**.
* Full conversation display with user queries and Jarvis responses.
* Quick-access buttons for frequently used commands.
* Clean layout with readable fonts and color-coded conversation.

---

## Tech Stack

| Technology           | Usage                         |
| -------------------- | ----------------------------- |
| Python 3.10+         | Core programming language     |
| PyQt5                | GUI interface                 |
| pyttsx3              | Text-to-speech engine         |
| speech\_recognition  | Voice command recognition     |
| OpenAI GPT-3.5-turbo | AI-powered intent recognition |
| pywhatkit            | YouTube music playback        |
| Wikipedia            | Wikipedia summaries           |
| smtplib              | Sending emails via Gmail      |

---

## Screenshots / GIF

* `jarvis.gif` is used for animated assistant in GUI.
* GUI displays the full conversation between user and JARVIS.

---

## Notes

* Keep your API keys and email credentials in `.env`.
* Ensure a working microphone is connected for voice commands.
* Only push code, GIFs, and icons to GitHub; secrets remain local.

---

## License

This project is open-source and free to use.

