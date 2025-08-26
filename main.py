import speech_recognition as sr
import webbrowser 
import pyttsx3
# install pocketsphinx too or use recognize google

# create a recognizer object for input voice
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# it will take text and speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

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
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com",2)

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
            
            # if word is 'jarvis' then it will speak 'Ya' in reply
            if(word.lower() == "jarvis"):
                speak("Ya")
                # listen for command
                with sr.Microphone() as sour:
                    print("Jarvis Active...")
                    audio = r.listen(sour)
                    command = r.recognize_google(audio)

                    processCommand(command) 

        except Exception as e:
            print("Error: {0}".format(e))