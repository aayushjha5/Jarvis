import speech_recognition as sr
import webbrowser 
import pyttsx3
import musicLibrary 
import requests # for handling api requests
from dotenv import load_dotenv
import os
from openai import OpenAI # for handling voice search through openai
from gtts import gTTS # converts text into spoken audio using Google Translate’s TTS and saves it as MP3.
import pygame   # for playing music 


# install pocketsphinx too or use recognize google as recognition engine


# create a recognizer object for input voice
recognizer = sr.Recognizer()
engine = pyttsx3.init() #for producing speech
# engine.setProperty("rate",150) # for decreasing the rate of speaking the words per minute 

#for storing api keys in env file
load_dotenv()
newsapi = os.getenv("NEWSAPI_KEY")
openaikey = os.getenv("OPENAI_KEY")


# it will take text and speak
def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    # initialize pygame mixer
    pygame.mixer.init()

    # load the mp3 file
    pygame.mixer.music.load('temp.mp3')

    # play the mp3 file
    pygame.mixer.music.play()

    #keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    os.remove("temp.mp3")

# for openai
def aiProcess(command):
    client = OpenAI(api_key=f"{openaikey}")

    completion = client.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
        {"role": "user", "content": command}
    ]
)

    return completion.choices[0].message.content

# for processing commands (not the first one i.e Jarvis)
def processCommand(c):
    #use browser methods and use 2 for opening in new tab ; 1 in new window
    if "open google" in c.lower():
        webbrowser.open("https://google.com",2)
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com",2)
    elif "open x" in c.lower():
        webbrowser.open("https://x.com",2)
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com",2)
        speak("Opening Youtube")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com",2)
    # play music 
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link,2)
    # news api integration
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200: #success
            data = r.json() #parse the json response

            # extract the articles
            articles = data.get('articles',[])

            # print the headlines
            for article in articles:
                speak(article['title'])
    else:
        # let openAI handle the request
        output = aiProcess(c)
        speak(output)

                
                




if __name__ == "__main__":
        # Listen for the wake word "Jarvis"
    speak("Initializing Jarvis.....")

    while True:
        # obtain audio from the microphone
        r = sr.Recognizer()

        # recognize speech using Google
        print("recognizing...") # for debugging whether it is working slow 
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)

            # source will be taken from physical microphone
            # timeout of 2 sec means after 2 sec, it will throw error
            # phrase time limit means how much time you can wait to continue again to speak

            word = r.recognize_google(audio)

            # exit check first
            if word.lower() == "stop":
                speak("Goodbye, shutting down...")
                print("Stopped by voice command")
                break   # exit the loop
            
            # if word is 'jarvis' then it will speak 'Ya' in reply
            if(word.lower() == "jarvis"):
                speak("Ya")
                # listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    # stop check again here for commands
                    if "stop" in command.lower():
                        speak("Goodbye, shutting down...")
                        print("Stopped by voice command")
                        break
                    else:
                        processCommand(command) 


        except Exception as e:
            print("Error: {0}".format(e))