import speech_recognition as sr  #for online speech recognizer
import webbrowser 
import pyttsx3
import musicLibrary 
import requests # for handling api requests
from dotenv import load_dotenv
import os
from openai import OpenAI # for handling voice search through openai
from gtts import gTTS # converts text into spoken audio using Google Translate’s TTS and saves it as MP3.
import pygame   # for playing music 

# importing for offline speech recognition by vosk
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import queue

# for stopping in hindi - keyword
STOP_KEYWORDS = {
    "बंद करो", "रुको", "रुक जाओ", "रुकना", "रुक",
    "बन्द करो", "रुकिये", "रुकिए"
}

# for stopping in hindi - function
def is_stop(text: str) -> bool:
    if not text:
        return False
    t = text.strip().lower()
    # simple substring match over multiword phrases and single tokens
    return any(kw in t for kw in STOP_KEYWORDS)

# install pocketsphinx too or use recognize google as online recognition engine


# create a recognizer object for input voice
'''recognizer = sr.Recognizer() # for online speech recognition '''
engine = pyttsx3.init() #for producing speech
# engine.setProperty("rate",150) # for decreasing the rate of speaking the words per minute 

#for storing api keys in env file
load_dotenv()
newsapi = os.getenv("NEWSAPI_KEY")
openaikey = os.getenv("OPENAI_KEY")


# loading vosk model
# model = Model("vosk-model-small-en-in-0.4") # model downloaded in home path
model = Model("vosk-model-small-hi-0.22") # model downloaded in home path
rec = KaldiRecognizer(model, 16000) # recognizer at 16 KHz

# it will take text and speak
def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    " Uses gTTS + pygame for speech output"
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
    client = OpenAI(api_key=f"{openaikey}") # Send command to OpenAI API

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
    # ask to play <<artist_name>> and a song on ytube will open 
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

# for vosk 
def listen_vosk():
    q = queue.Queue()

    def audio_callback(indata, frames, time, status):
        if status:
            print("Sounddevice status:", status)
        # indata is a bytes-like object for RawInputStream; ensure bytes
        q.put(bytes(indata))

    # Use device default input sample rate if available
    try:
        device_info = sd.query_devices(sd.default.device, 'input')
        samplerate = int(device_info['default_samplerate'])
    except Exception:
        samplerate = 16000  # fallback

    rec = KaldiRecognizer(model, samplerate)

    with sd.RawInputStream(samplerate=samplerate,
                           blocksize=8000,
                           dtype='int16',
                           channels=1,
                           callback=audio_callback):
        # Collect until a full utterance is accepted
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())
                return res.get("text", "").lower()
            # Optionally handle partials:
            # else:
            #     partial = json.loads(rec.PartialResult()).get("partial", "")
                




if __name__ == "__main__":
        # Listen for the wake word "Jarvis"
    speak("मैथिली आवाज सँ पाठ वाणी पहचान प्रणाली मे अपनेक स्वागत अछि")

    # for online speech recognition, use recognize google
    '''
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
    '''
    # for offline speech recognition, use vosk
    while True:
        try:
            word = listen_vosk()
            print("Heard: ", word)

            if word == "":
                continue # skip empty
            if is_stop(word):
                speak("अलविदा, बंद भ' रहल छी...")
                break
            if "jarvis" in word:
                speak("Ya")
                command = listen_vosk()
                if is_stop(word):
                    speak("अलविदा, बंद भ' रहल छी...")
                    break
                else:
                    processCommand(command)
        except Exception as e:
            print("Error: {0}".format(e))