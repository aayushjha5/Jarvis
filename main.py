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
    print(c)

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
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command) 

        except Exception as e:
            print("Error: {0}".format(e))