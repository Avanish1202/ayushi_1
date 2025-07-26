import streamlit as st
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import threading

# Initialize TTS engine
engine = pyttsx3.init()

# Streamlit page setup
st.set_page_config(page_title="Voice Assistant", page_icon="🎙️")
st.title("🎙️ Voice Assistant")
st.write("Say something like: **'time'**, **'open google'**, **'your name'**, or **'stop'**")

# Safe TTS in Streamlit using threading
def speak(text):
    st.text(f"Assistant: {text}")
    thread = threading.Thread(target=run_tts, args=(text,))
    thread.start()

def run_tts(text):
    engine.say(text)
    try:
        engine.runAndWait()
    except RuntimeError:
        pass  # If already running, skip to prevent crash

# Listen to mic input
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎧 Listening... Speak now!")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            st.success(f"🗣️ You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand.")
            return ""
        except sr.RequestError:
            speak("Service unavailable.")
            return ""

# Process voice commands
def process_command(command):
    if "time" in command:
        time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {time}")
    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google")
    elif "your name" in command:
        speak("I am your AI assistant.")
    elif "exit" in command or "stop" in command:
        speak("Goodbye!")
        st.stop()
    else:
        speak("Sorry, I can't help with that yet.")

# Streamlit UI control
if st.button("🎤 Start Listening"):
    speak("Hello Avanish! How can I assist you?")
    command = listen_command()
    if command:
        process_command(command)
