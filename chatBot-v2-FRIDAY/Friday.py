# Importing the pyttsx3 library for text-to-speech conversion
import pyttsx3
# Importing the datetime module to work with date and time
import datetime
# Importing the speech_recognition library to recognize speech input
import speech_recognition as sr
# Importing the webbrowser module to open web pages
import webbrowser as wb
# Importing the subprocess module to interact with the operating system
import os, sys, subprocess
from datetime import date, datetime

# Initialize the pyttsx3 engine with variable friday
friday = pyttsx3.init()

# Function to convert text to speech
def speak(audio):
    # Display message
    print('F.R.I.D.A.Y.: ' + audio)
    # Read the text
    friday.say(audio)  
    # Wait for the speech to complete
    friday.runAndWait()

# Function to get the current time and speak it
def time():
    # Get the current time and store it in variable now
    now = datetime.now().strftime("%I:%M %p")
    # Speak the current time
    speak(now)

def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])

# Function to take a voice input from the user
def command():
    # Initialize the recognizer
    command = sr.Recognizer()
    # Using the microphone as the audio source
    with sr.Microphone() as mic:
        audio = command.listen(mic)

    try:
        # Recognize the speech in English using Google's speech recognition
        you = command.recognize_google(audio, language='en')
        # Display the recognized command
        print("You: " + you)
    except sr.UnknownValueError:
        # If speech is not recognized, ask for input again
        print("Please type your command")
        # Taking input from the user
        you = str(input('Your order is: '))
    return you  # Returning the recognized command or typed input

# Function to greet the user based on the time of day
def greeting():
    # Get the current hour and store it in variable time
    time = datetime.now().hour
    # Greeting for morning
    if time >= 6 and time <= 12:
        speak("Good morning")
    # Greeting for afternoon
    elif time > 12 and time <= 18:
        speak("Good afternoon")
    # Greeting for night
    elif time > 18 and time <= 24:
        speak("Good night")
    # Asking how to assist the user
    speak("How can I assist you today?")

# Main function
if __name__ == "__main__":
    # Greet the user
    greeting()
    # Use while loop to keep the program running
    while True:
        # Get user's input and convert it to lower case
        you = command().lower()
        # Respond to a message containing the word "google"
        if "google" in you:
            # Prompt user for input
            speak("What would you like to search?")
            # Convert input to lower case and store it in variable search
            search = command().lower()
            # Create the Google search URL
            url = f"https://www.google.com/search?q={search}"
            # Open the URL in the web browser
            wb.get().open(url)
            # Inform the user about the search result
            speak(f'Here is your {search} on Google')
        
        # Respond to a message containing the word "youtube"
        elif "youtube" in you:
            # Prompt user for input
            speak("What would you like to search?")
            # Convert input to lower case and store it in variable search
            search = command().lower()
            # Create the YouTube search URL
            url = f"https://www.youtube.com/search?q={search}"
            # Open the URL in the web browser
            wb.get().open(url)
            # Inform the user about the search result
            speak(f'Here is your {search} on YouTube')
        
        # Respond to a message containing the word "video"
        # elif "video" in you:
            # Path to the video file
            # video = r"LouClip.mp4"
            # Open the video file
            # open_file(video) 
        
        # Respond to a message containing the word "time"
        elif "time" in you:
            # Call function time() to speak the current time
            time()
        
        # Respond to a message containing the word "today"
        elif "today" in you:
            # Get today's date
            today = date.today().strftime("%B %d, %Y")
            speak(today)
        
        # Respond to a message containing the word "bye"
        elif "bye" in you:
            # Say goodbye
            speak("It's my pleasure to assist you today. Bye bye.")
            # Exiting the program
            quit()