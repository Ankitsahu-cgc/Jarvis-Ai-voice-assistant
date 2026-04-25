import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import datetime
import requests
import openai
import os
import threading
import time
from dotenv import load_dotenv
import openai
import os
import pywhatkit as kit
from google.cloud import translate_v2 as translate
import requests
import pkg_resources
import tkinter as tk
from tkinter import * 
import pyttsx3
import requests
import subprocess as sp
from gpt4all import GPT4All









def offline_chat(query):
    model = GPT4All("gpt4all-model")
    response = model.chat(query)
    return response


for package in ["googletrans", "translators", "httpx", "h11", "urllib3-future"]:
    try:
        print(f"{package}: {pkg_resources.get_distribution(package).version}")
    except:
        print(f"{package} is not installed.")

load_dotenv()  # Load environment variables from .env file
#OPENAI Key
if not openai.api_key:
    print("Error: OpenAI API key not found.")
else:
    print("API key loaded successfully!")

# Initialize Text-to-Speech Engine
engine = pyttsx3.init(driverName='sapi5')
engine = pyttsx3.init()
engine.setProperty('rate', 180)  # Speed of voice
engine.setProperty('volume', 1.0)  # Volume level

# Secure API Keys (Set your API keys in environment variables)
openai.api_key = os.getenv("OPENAI_API_KEY")
weather_api_key = os.getenv("WEATHER_API_KEY")

# List to store alarms
alarms = []

import requests
def speaknow():
    engine.say(textv.get())
    engine.runAndWait()
    engine.stop()

root = Tk()
textv = StringVar()
obj = LabelFrame(root, text="Text to Speech", font=20, bd=1)
obj.pack(fill="both", expand="yes", padx=10, pady=10)

lb1 = Label(obj, text="Text", font=30)
lb1.pack(side=tk.LEFT, padx=5)

text = Entry(obj, textvariable=textv, font=30, width=25, bd=5)
text.pack(side=tk.LEFT, padx=10)

btn = Button(obj, text="Speak", font=20, bg="green", fg="white", command=speaknow)
btn.pack(side=tk.LEFT, padx=10)

root.title("Text to Speech")
root.geometry("480x200")
root.resizable(False, False)

# ----------- Core Functions -----------
def speak(text):
    """Converts text to speech."""
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening... Speak now:")
        recognizer.adjust_for_ambient_noise(source)  # Adjusts for background noise
        try:
            audio = recognizer.listen(source, timeout=15)  # Increased timeout
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.WaitTimeoutError:
            print("Listening timed out. Try speaking louder or closer to the mic.")
            return None   
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
            return None
        except sr.RequestError:
            print("Network error. Check your internet connection.")
            return None


def get_time():
    """Returns the current time."""
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {current_time}.")

def get_date():
    """Returns the current date."""
    current_date = datetime.datetime.now().strftime("%A, %d %B %Y")
    speak(f"Today is {current_date}.")

def get_weather(city="Delhi"):
    """Fetches live weather information."""
    if not weather_api_key:
        speak("Weather API key is missing. Please set it in environment variables.")
        return
    
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
    try:
        response = requests.get(base_url).json()
        temperature = response["main"]["temp"]
        description = response["weather"][0]["description"]
        speak(f"The current temperature in {city} is {temperature}°C with {description}.")
    except:
        speak("Unable to fetch the weather details.")

chat_history = [{"role": "system", "content": "You are an AI assistant."}]

def chat_with_ai():
    speak("Chat mode activated. Say 'exit' to stop.")

    while True:
        user_input = recognize_speech()
        if user_input in ["exit", "quit", "stop"]:
            speak("Exiting chat mode.")
            break

        if user_input:
            chat_history.append({"role": "user", "content": user_input})
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",  # Ensure correct model
                    messages=chat_history
                )
                answer = response["choices"][0]["message"]["content"]
                chat_history.append({"role": "assistant", "content": answer})
                speak(answer)
            except openai.error.OpenAIError as e:
                speak(f"AI service error: {e}")
                print(f"Error: {e}")

def extended_speech_to_text():
    """Converts speech to text and saves it as a note."""
    speak("Speech-to-text mode activated. Speak now. Say 'exit' to stop.")
    text_content = []
    
    while True:
        spoken_text = recognize_speech()
        if spoken_text in ["exit", "quit", "stop"]:
            speak("Speech-to-text mode stopped.")
            break
        elif spoken_text:
            text_content.append(spoken_text)
            print("Saved text:", spoken_text)
    
    if text_content:
        with open("speech_notes.txt", "a") as file:
            file.write("\n".join(text_content) + "\n")
        speak("Thanks for Using Speech Text Mode")

# ----------- AI-Powered Alarm System -----------
def set_alarm(alarm_time):
    """Sets an alarm at the specified time."""
    alarms.append(alarm_time)
    speak(f"Alarm set for {alarm_time}.")
  
  
    
def translate_text(text, dest_lang='en'):
    """Robust translation with fallback"""
    try:
        from googletrans import Translator
        translator = Translator()
        translation = translator.translate(text, dest=dest_lang)
        return translation.text
    except:
        try:
            import translators as ts
            return ts.google(text, to_language=dest_lang)
        except Exception as e:
            return f"Could not translate: {str(e)}"

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
    except Exception as e:
        print("Could you please say that again?")
        return "None"
    return query.lower()



def check_alarms():
    """Continuously checks if it's time for an alarm."""
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        if now in alarms:
            speak("Time's up! Your alarm is ringing.")
            os.system("start alarm.mp3")  # Replace with actual alarm sound file
            alarms.remove(now)  # Remove alarm after ringing
        time.sleep(30)  # Check every 30 seconds

# Start Alarm Monitoring Thread
alarm_thread = threading.Thread(target=check_alarms, daemon=True)
alarm_thread.start()

def view_alarms():
    """Lists all active alarms."""
    if not alarms:
        speak("No alarms are currently set.")
    else:
        speak(f"You have the following alarms set: {', '.join(alarms)}.")
        
def analyze_emotion(text):
    """Analyzes emotion from text input."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": "Analyze the mood from this text: " + text}]
        )
        emotion = response["choices"][0]["message"]["content"].lower()
        return emotion
    except:
        return "neutral"

def search_on_wikipedia(query):
    try:
        results = wikipedia.summary(query, sentences=2)  # Fetch summary (2 sentences)
        return results
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found: {e.options[:5]}"  # Return top 5 suggestions
    except wikipedia.exceptions.PageError:
        return "No page found on Wikipedia for this query."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def cancel_alarm(alarm_time):
    """Cancels an alarm if it exists."""
    if alarm_time in alarms:
        alarms.remove(alarm_time)
        speak(f"Alarm for {alarm_time} has been canceled.")
    else:
        speak(f"No alarm found for {alarm_time}.")

# ----------- Command Execution -----------
def execute_command(command):
    """Performs actions based on voice commands."""
    if not command:
        return
    
    
    if "what is the time" in command:
        get_time()
    elif "what is the date" in command:
        get_date()
    elif "weather" in command:
        get_weather()
    elif "chatbot" in command or "talk" in command:
        chat_with_ai()
    elif "speech to text" in command or "dictation" in command:
        extended_speech_to_text()
    elif "shutdown my system" in command:
        speak("Shutting down the system...")
        os.system("shutdown /s /t 5")
    elif "restart my system" in command:
        speak("Restarting the system...")
        os.system("shutdown /r /t 5")
    elif "translate" in command:
        text_to_translate = command.split("translate")[1].strip()
        translated = translate_text(text_to_translate)
        speak(f"Translation: {translated}")
    elif "play " in command:
        query = command.replace("play", "").strip()
        speak(f"Playing {query} on YouTube.")
                
        try:
            kit.playonyt(query)  # Auto-plays the first YouTube result
        except:
            speak("I couldn't play the video. Please try again.")             
            
            
                      
    elif "how r u" in command:
                    speak("I am absolutely fine. What about you")
    elif "i am also fine" in command:
                    speak("Sounds good, What can I do for you")                 
    elif "hello" in command or "hey" in command or "hii" in command:
                    speak("Hello Jarvis here. created by Ankit")
    elif "i am also fine" in command:
                    speak("Sounds good, What can I do for you")                 
    elif "madharchod" in command:
                    speak("arey, madharchod bhosdiwala behen chod bhadwe")      
    
    elif "turn on text to speech function" in command:
        speak("Starting Text-to-Speech mode.")
        root.mainloop()
    elif "open youtube and search for" in command:
        query = command.replace("open youtube and search for", "").strip()
        speak(f"opening youtube and searching for {query}")
        webbrowser.open(f"https://www.youtube.com/search?q={query}")
    elif "open youtube" in command:
        query = command.replace("open youtube", "").strip()
        speak(f"opening youtube")
        webbrowser.open(f"https://www.youtube.com") 
    elif "kya" in command or "kaun" in command or "kaha" in command or "kaise" in command :
        query = command.replace("search google for", "").strip()
        speak(f"Searching on google")
        webbrowser.open(f"https://www.google.com/search?q={query}")    
    elif "ki" in command or "who" in command or "where" in command or "how" in command :
        query = command.replace("search google for", "").strip()
        speak(f"Searching on google")
        webbrowser.open(f"https://www.google.com/search?q={query}")    
    elif "what" in command or "who" in command or "kithe" in command or "kive" in command :
        query = command.replace("search google for", "").strip()
        speak(f"Searching on google")
        webbrowser.open(f"https://www.google.com/search?q={query}")    
    
    elif "search for" in command or "is" in command or "when" in command :
        query = command.replace(" search for", "").strip()
        speak(f"Searching on Google for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")
        
    elif "wikipedia" in command:
                speak("what do you want to search on wikipedia sir?")
                search = take_command().lower()
                results = search_on_wikipedia(search)
                speak(f"According to wikipedia,{results}")
                speak("I am printing in on terminal")
                print(results)
            
    elif "search about" in command:
        query = command.replace("search about", "").strip()
        speak(f"Searching on wikipedia")
        webbrowser.open(f"https://en.wikipedia.org/w/index.php?fulltext=1&search={query}")
        
    elif "open instagram" in command :
        query = command.replace("search instagram for", "").strip()
        speak(f"opening instagram ")
        webbrowser.open(f"https://www.instagram.com") 
        
    elif "open facebook" in command :
        query = command.replace("search facebook for", "").strip()
        speak(f"opening facebook ")
        webbrowser.open(f"(https://www.facebook.com")
       
    elif "open whatsapp" in command :
        query = command.replace("search whatsapp for", "").strip()
        speak(f"opening whatsapp")
        webbrowser.open(f"https://www.whatsapp.com")
        
    elif "open linkedin" in command :
        query = command.replace("search linkedin for", "").strip()
        speak(f"opening linkedin")
        webbrowser.open(f"https://www.linkedin.com")
        
    elif "open twitter" in command :
        query = command.replace("search twitter for", "").strip()
        speak(f"opening twitter")
        webbrowser.open(f"https://www.twitter.com")
        
    elif "open snapchat" in command :
        query = command.replace("search snapchat for", "").strip()
        speak(f"opening snapchat")
        webbrowser.open(f"https://www.snapchat.com")
        
    elif "set alarm for" in command:
        alarm_time = command.replace("set alarm for", "").strip()
        set_alarm(alarm_time)
    elif "view alarm" in command or "list alarms" in command:
        view_alarms()
    elif "open command prompt" in command:
                    speak("Opening command prompt")
                    os.system('start cmd')  
                      
    elif "open camera" in command:
                    speak("Opening camera sir")
                    sp.run('start microsoft.windows.camera:', shell=True)
    elif "cancel alarm for" in command:
        alarm_time = command.replace("cancel alarm for", "").strip()
        cancel_alarm(alarm_time)
    else:
        speak("I didn't understand that. Please try again.")

# ----------- Main Loop -----------
speak("Hello! I am Jarvis. Created by Ankit, How can I Help you?")
while True:
    user_command = recognize_speech()
    execute_command(user_command)
    
